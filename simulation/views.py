from django.shortcuts import render, redirect  
from decimal import Decimal, InvalidOperation  
from stocks.models import StockPrice  
from .forms import SimulationForm
from datetime import datetime
import json  

# シュミレーションフォームを作成
def simulation_form(request):
    # フォームを作成（選択できる企業はユーザーがお気に入り企業に登録している企業のみ）
    form = SimulationForm(request.user)
    return render(request, "simulation/simulation_form.html", {"form": form})


# 日本円表記に変換（億・万・円単位）（シュミレーション結果で使用）
def format_currency_jp(value: Decimal) -> str:

    # 負の値かどうかをチェック
    if value < 0:
        negative = True 
    else:
        negative = False 
    value_int = int(abs(round(value)))  # 絶対値を整数に変換

    # 各単位の値を計算
    oku = value_int // 100_000_000              # 億の部分
    man = (value_int % 100_000_000) // 10_000   # 万の部分
    yen = value_int % 10_000                    # 円の部分

    # 表示する単位を配列に格納
    parts = []
    if oku > 0:
        parts.append(f"{oku}億")    # 億が0より大きい場合のみ追加
    if man > 0:
        parts.append(f"{man}万")    # 万が0より大きい場合のみ追加
    if oku == 0 and man == 0:
        parts.append(f"{yen}")      # 億も万もない場合は単位を付与しない

    # 単位を結合して「円」を追加
    result = "".join(parts) + "円"
    # 負の値の場合はマイナス記号を付ける
    if negative:
        return f"-{result}"
    else:
        return result

# 値の確認（シュミレーション結果で使用）
def to_decimal(x):
    if x is not None:       # 値がある時はその値を返す
        return Decimal(x)
    return Decimal(0)       # ない場合は0を返す

# シミュレーション結果
def simulation_result(request):
    
    if request.method != "POST":
        # GETの場合は、フォーム画面へリダイレクト
        return redirect("simulation:simulation_form")

    # フォームのデータを取得
    form = SimulationForm(request.user, request.POST)
    
    if not form.is_valid():
        # エラーの場合、フォームを再表示
        return render(request, "simulation/simulation_form.html", {"form": form})

    # フォームの値を取得
    company = form.cleaned_data["company"]                          # 企業
    start_date = form.cleaned_data["start_date"]                    # 開始日
    end_date = form.cleaned_data.get("end_date")                    # 終了日
    initial_invest = Decimal(form.cleaned_data["initial_invest"])   # 頭金
    monthly_invest = Decimal(form.cleaned_data["monthly_invest"])   # 毎月の積立額

    # 企業名を取得（日本語名優先、なければ英語名）
    company_name = company.name_jp or company.name_en

    # その企業の株価データがそもそも存在するかチェック
    if not StockPrice.objects.filter(company=company).exists():
        return render(
            request,
            "simulation/simulation_result.html",
            {
                "error": f"{company_name}の株価データがありません。"
            },
        )

    # 開始日以降の株価データを取得
    qs = StockPrice.objects.filter(
        company=company,
        date__gte=start_date,  
    )
    # 終了日が指定している場合は終了日以前のデータに絞る
    if end_date:
        qs = qs.filter(date__lte=end_date)

    # 日付順にソート
    qs = qs.order_by("date")

    # リストに変換
    data = list(qs.values("date", "close_price", "dividend"))

    # データが空の場合はエラーを表示
    if not data:
        return render(
            request,
            "simulation/simulation_result.html",
            {
                "error": f"指定された期間における、{company_name}の株価データが見つかりませんでした。"
            },
        )

    # データを処理
    for row in data:
        # 日付をdatetime型に変換（既にdatetimeの場合はそのまま）
        if isinstance(row["date"], str):
            row["date"] = datetime.strptime(row["date"], "%Y-%m-%d")
        
        # 終値をDecimal型に変換
        row["close_price"] = to_decimal(row["close_price"])
        
        # 配当をDecimal型に変換
        row["dividend"] = to_decimal(row["dividend"])
        
        # 年月を追加（YYYY-MM形式の文字列）
        row["month"] = row["date"].strftime("%Y-%m")

    # 各月の最初のデータのみを抽出（月初の株価で購入を想定）
    monthly_data = []
    processed_months = set()

    for row in data:
        current_month = row["month"]
        if current_month not in processed_months:
            monthly_data.append(row)
            processed_months.add(current_month)

    # 初回投資額で購入できる株数を計算
    try:
        shares = initial_invest / monthly_data[0]["close_price"]
    except (InvalidOperation, ZeroDivisionError, IndexError):
        shares = Decimal(0)

    # 総投資額を初回投資額で初期化
    total_invested = initial_invest
    # 受取配当金の累計を0で初期化
    cash_dividend = Decimal(0)

    # グラフ表示用のリスト
    history_dates = []
    history_price = []
    history_value = []
    history_invest = []

    # 月初データの月リストを取得
    months = [row["month"] for row in monthly_data]
    # 次に購入する月のインデックス（2ヶ月目から）
    month_idx = 1

    # 全ての日次データをループ処理
    for row in data:
        price = row["close_price"]
        dividend = row["dividend"]

        # 月初かどうかをチェック（2ヶ月目以降）
        if month_idx < len(months) and row["month"] == months[month_idx]:
            # 月初の場合、積立額で株を追加購入
            if price > 0:
                shares += monthly_invest / price
            total_invested += monthly_invest
            month_idx += 1

        # 配当が支払われた場合
        if dividend > 0:
            cash_dividend += dividend * shares

        # その時点での評価額を計算（株式評価額 + 配当金累計）
        current_value = shares * price + cash_dividend

        # 履歴に記録（Chart.js用）
        history_dates.append(row["date"].strftime("%Y/%m"))
        history_price.append(float(price))
        history_value.append(float(current_value))
        history_invest.append(float(total_invested))

    # 最終的な評価額を計算（最終日の株価 × 保有株数 + 配当金累計）
    final_value = shares * data[-1]["close_price"] + cash_dividend
    # 損益を計算（評価額 - 投資額）
    profit = final_value - total_invested

    context = {
        "company": company,
        "labels": json.dumps(history_dates),
        "prices": json.dumps(history_price),
        "valuation": json.dumps(history_value),
        "invested": json.dumps(history_invest),
        "total_invested": format_currency_jp(total_invested),
        "final_value": format_currency_jp(final_value),
        "profit": format_currency_jp(profit),
        "cash_dividend": format_currency_jp(cash_dividend),
    }

    return render(request, "simulation/simulation_result.html", context)