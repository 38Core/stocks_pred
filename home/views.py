from django.shortcuts import render
from stocks.models import StockPrice, Company
from common.text_utils import errnote_check
from django.conf import settings
from .forms import ContactForm
import json
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# 表示対象の銘柄リスト
DISPLAY_SYMBOLS = [
    "CSEL0000001",     
    "AUTM0000062",    
    "AUTM0000099",    
    "BZES0000088", 
    "BZES0000098",    
]

def index(request):
    # GETパラメータから選択された銘柄を取得、なければリストの最初を使用
    symbol = request.GET.get("company", DISPLAY_SYMBOLS[0])

    # 表示対象の銘柄リストに含まれる企業情報を取得
    companies = Company.objects.filter(symbol__in=DISPLAY_SYMBOLS)

    # 選択された銘柄の株価データを日付順で取得
    prices_qs = (
        StockPrice.objects
        .filter(company__symbol=symbol)  
        .order_by("date")                
    )

    # 株価データから日付のリストを作成（年のみ抽出）
    dates = [p.date.strftime("%Y") for p in prices_qs]
    
    # 株価データから終値のリストを作成（float型に変換）
    prices = [float(p.close_price) for p in prices_qs]

    # テンプレートに渡すデータを作成
    context = {
        "companies": companies,         # 企業リスト
        "symbol": symbol,               # 現在選択されている銘柄
        "dates": json.dumps(dates),     # 日付リストをJSON文字列に変換（JavaScript用）
        "prices": json.dumps(prices),   # 株価リストをJSON文字列に変換（JavaScript用）
        "body_class": "home",           # bodyタグに付与するCSSクラス名
    }

    return render(request, 'home/index.html', context)


# メールを送信する
def send_gmail(to, subject, message):

    # 認証情報を作成
    creds = Credentials(
        token=None,
        refresh_token=settings.GMAIL_REFRESH_TOKEN,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=settings.GMAIL_CLIENT_ID,
        client_secret=settings.GMAIL_CLIENT_SECRET,
    )

    # Gmail APIクライアントを作成
    service = build('gmail', 'v1', credentials=creds)

    # メールを作成
    mime = MIMEText(message, 'plain', 'utf-8')
    mime['to']      = to
    mime['from']    = settings.DEFAULT_FROM_EMAIL
    mime['subject'] = subject

    # base64エンコードして送信
    raw = base64.urlsafe_b64encode(mime.as_bytes()).decode()
    service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()


# お問い合わせフォーム
def contact(request):
    # リクエストがPOSTメソッドかどうかをチェック
    if request.method == 'POST':
        # 押されたボタンが「確認画面へ」ボタンの場合
        if 'go_confirm' in request.POST:

            # フォームのデータを取得
            form = ContactForm(request.POST)

            if form.is_valid():
                # セッションに残っている古いデータを削除（新規アクセス時はリセット）
                request.session.pop('contact_data', None)

                # データをセッションに保存（送信処理で使用）
                request.session['contact_data'] = form.cleaned_data

                # 確認画面用のフォームを作成（保存されたデータで初期化）
                confirm_form = ContactForm(initial=form.cleaned_data)

                # 出力用フォームの設定
                for field in confirm_form.fields.values():
                    # フォームを読み取り専用にして入力不可
                    field.widget.attrs['readonly'] = True
                    # フォームの枠線を消す
                    field.widget.attrs['style'] = ' border: none;'

                return render(request, 'home/contact_confirm.html', {
                    'form': confirm_form
                })

            # エラーの重複を外す
            unique_errors = errnote_check(form)
            return render(request, 'home/contact_form.html', {
                'unique_errors': unique_errors,
                'form': form
            })

        # 押されたボタンが「送信する」ボタンの場合
        elif 'go_send' in request.POST:

            # セッションから保存されていた問い合わせデータを取得
            data = request.session.get('contact_data')

            # データが存在するかチェック
            if data:
                # メール送信処理
                try:
                    # ========== 自分宛メール ==========
                    subject_to_me = f"【お問い合わせがありました】{data['subject']}"
                    message_to_me = f"""
お問い合わせがありました。

お名前: {data['name']}
メールアドレス: {data['email']}
件名: {data['subject']}

お問い合わせ内容:
{data['message']}
"""
                    send_gmail(
                        to=settings.DEFAULT_FROM_EMAIL,
                        subject=subject_to_me,
                        message=message_to_me,
                    )

                    # ========== 相手宛メール ==========
                    subject_to_user = f"【お問い合わせ受付完了】{data['subject']}"
                    message_to_user = f"""
{data['name']} 様

お問い合わせありがとうございます。
以下の内容でお問い合わせを受け付けました。

----------------------------------------
件名: {data['subject']}
お名前: {data['name']} 様
お問い合わせ内容:
{data['message']}
----------------------------------------

※このメールはシステムからの自動返信です。
このメールアドレスはポートフォリオ運用専用のため、
直接ご返信いただいても確認が遅れる場合がございます。

内容を確認後、改めて私個人のメールアドレスより速やかご連絡させていただきます。
"""
                    send_gmail(
                        to=data['email'],
                        subject=subject_to_user,
                        message=message_to_user,
                    )

                    # 送信完了後、セッションから問い合わせデータを削除
                    request.session.pop('contact_data', None)
                    return render(request, 'home/contact_complete.html', {
                        'name': data['name']
                    })

                # メール送信でエラーが発生した場合の処理
                except Exception as e:

                    # セッションに保存されていたデータでフォームを再作成
                    form = ContactForm(initial=data)

                    # エラーメッセージを定義
                    error_message = "メール送信に失敗しました。もう一度お試しください。"

                    return render(request, 'home/contact_form.html', {
                        'form': form,
                        'error_message': error_message
                    })

        # go_confirmもgo_sendもない不正なPOSTは初期画面へ
        form = ContactForm()
        return render(request, 'home/contact_form.html', {
            'form': form
        })

    # 初回アクセス時は空のフォームを作成
    else:
        form = ContactForm()
        return render(request, 'home/contact_form.html', {
            'form': form
        })