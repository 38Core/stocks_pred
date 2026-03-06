from django.shortcuts import render, get_object_or_404  
from django.core.paginator import Paginator  
from .models import StockPrice, Company, Market, Country  
from customize.models import FavoriteCompany  
from django.db.models import Q  
from common.text_utils import checker_text  
import json  


# 銘柄一覧
def company_list(request):

    # 全企業を取得（英語名の昇順でソート）
    companies = Company.objects.all().select_related('market__country').order_by('name_en')
    
    # ユーザーがログインしているかどうか
    if request.user.is_authenticated:
        # ユーザーがお気に入り登録している銘柄コードを取得
        favorite_symbols = set(
            FavoriteCompany.objects.filter(user=request.user)
            .values_list("company__symbol", flat=True)
        )
        # お気に入りしているかどうか調査し、真偽値を追加する
        for c in companies:
            c.is_favorite = c.symbol in favorite_symbols  
    # 未ログインの場合
    else:
        # 全ての企業のお気に入り企業の有無をFalseに設定
        for c in companies:
            c.is_favorite = False

    # ページネーションの設定（Paginatorライブラリを使用）
    paginator = Paginator(companies, 20)        # 1ページあたり20件表示
    page_number = request.GET.get('page')       # 現在のページ数を取得
    page_obj = paginator.get_page(page_number)  # 指定ページのデータを取得
    
    return render(request, 'stocks/company_list.html', {
        'companies': page_obj,                  # 指定ページの企業リスト
        'keyword': '',                          # 検索キーワード（一覧表示では空）
        'page_obj': page_obj                    # ページネーションオブジェクト（ページ番号表示用）
    })


# 企業検索
def search_company(request):

    # 検索キーワードを取得
    word = request.GET.get('company_name', '')
    # テキストを正規化
    keyword = checker_text(word)

    # キーワードが入力されているか
    if keyword:
        # 英語名または日本語名にキーワードが部分一致する企業を検索し、英語名の昇順でソート
        companies = Company.objects.filter(
            Q(name_en__icontains=keyword) |  # 英語名に含まれる
            Q(name_jp__icontains=keyword)    # 日本語名に含まれる
        ).order_by('name_en')  
    
    # キーワードが空の場合
    else:
        companies = Company.objects.none()  # 0件表示


    # ユーザーがログインしているか
    if request.user.is_authenticated:
        # ユーザーがお気に入り登録している銘柄コードを取得
        favorite_symbols = set(
            FavoriteCompany.objects.filter(user=request.user)
            .values_list("company__symbol", flat=True)
        )
        # お気に入りしているかどうか調査し、真偽値を追加する
        for c in companies:
            c.is_favorite = c.symbol in favorite_symbols
    # 未ログインの場合
    else:
        # 全ての企業のお気に入り企業の有無をFalseに設定
        for c in companies:
            c.is_favorite = False

    # ページネーション設定（Paginatorライブラリを使用）
    paginator = Paginator(companies, 20)        # 1ページあたり20件表示
    page_number = request.GET.get('page')       # 現在のページ数を取得
    page_obj = paginator.get_page(page_number)  # 指定ページのデータを取得

    return render(request, 'stocks/company_list.html', {
        'companies': page_obj,  # 指定ページの企業リスト
        'keyword': keyword,     # 検索キーワード（検索ボックスに表示用）
        'page_obj': page_obj    # ページネーションオブジェクト（ページ番号表示用）
    })


# 株価チャート表示
def stock_chart(request, symbol):
    # 選択した企業を取得
    company = get_object_or_404(Company, symbol=symbol)
    # その企業の全株価データを日付順で取得
    prices = StockPrice.objects.filter(company=company).order_by("date")

    # 株価データが存在しない場合
    if not prices.exists():
        # データなしページを表示
        return render(request,'stocks/no_company.html',{
            'company_name': company.name_en or company.name_jp
        })

    # 株価データから日付リストを作成（年のみ抽出）
    labels = [p.date.strftime("%Y") for p in prices]
    # 株価データから終値リストを作成（float型に変換）
    close_prices = [float(p.close_price) for p in prices]

    return render(request, 'stocks/stock_chart.html', {
        'company': company,                     # 選択した企業情報
        'labels': json.dumps(labels),           # グラフ用：日付リスト（JSON文字列）
        'prices': json.dumps(close_prices),     # グラフ用：株価リスト（JSON文字列）
    })