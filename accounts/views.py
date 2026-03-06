from django.shortcuts import render, redirect
from common.text_utils import errnote_check
from .forms import UserCreateForm
from django.contrib.auth import logout

# アカウント作成
def create(request):
    if request.method == "POST":
        # フォームのデータを取得
        form = UserCreateForm(request.POST)

        if form.is_valid():

            # DBに保存せずユーザーオブジェクトを作成（commit=False）
            user = form.save(commit=False)
            user.is_staff = False                   # 管理画面アクセス権限を無効化（一般ユーザー）
            user.is_superuser = False               # スーパーユーザー権限を無効化
            user.save()                             # ユーザー情報をDBに保存
            return redirect('accounts:login')       # ログインページへ
        
        # エラーの重複を外す
        unique_errors=errnote_check(form)
        return render(request, 'accounts/create.html', {
            'unique_errors': unique_errors,
            'form': form
        })
    
    # GETリクエスト（初回アクセス時）の処理(空のフォームを作成)
    form = UserCreateForm()

    return render(request, 'accounts/create.html', {
        'form': form
    })

# マイページ
def mypage(request):
    return(render(request, 'accounts/mypage.html'))

# ログアウト
def logout_view(request):
    logout(request)
    return redirect('home:index') 

