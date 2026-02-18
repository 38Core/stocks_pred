from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from common.text_utils import errnote_check
from stocks.models import Company
from .forms import CompanyForm, CompanySearchForm
from django import forms

# 管理者ページ
@login_required
def master_page(request):
    # ログイン中のユーザーが管理者権限を付与されているか確認
    if request.user.is_staff:
        return render(request, 'master/master_page.html')
    return HttpResponse("あなたは管理者権限が付与されていません。")


# 企業を登録
@login_required
def company_create(request):
    # ログイン中のユーザーが管理者権限を付与されているか確認
    if not request.user.has_perm('stocks.add_company'):    
        return HttpResponse("あなたは企業の登録権限が付与されていません。")
    
    # リクエストがPOSTメソッドかどうかをチェック
    if request.method == 'POST':
        # フォームのデータを取得
        form = CompanyForm(request.POST)        
        if form.is_valid():
            # データベースに登録していない場合
            exists = Company.objects.filter(
                name_en=form.cleaned_data['name_en'],
                name_jp=form.cleaned_data['name_jp']
            ).exists()
            if not exists:
                company = form.save()   # データーベースに登録
                return redirect(
                    'master:company_create_result',
                    symbol=company.symbol
                )
            else:
                # エラー内容を設定
                form.add_error(None, "同じ会社が既に登録されています")
        
        # エラーの重複を外す
        unique_errors=errnote_check(form)
        return render(request, 'master/company_create.html', {
            'unique_errors': unique_errors,
            'form': form
            })
    
    # GETリクエスト（初回アクセス時）の処理(空のフォームを作成)
    form = CompanyForm()

    return render(request, 'master/company_create.html', {
        'form': form
    })
    

# 登録した企業データを表示する
@login_required
def company_create_result(request, symbol):
    # ログイン中のユーザーが管理者権限を付与されているか確認
    if not request.user.has_perm('stocks.add_company'):     
        return HttpResponse("あなたは企業の登録権限が付与されていません。")   
    
    # 選択した企業を取得
    company = Company.objects.filter(symbol=symbol).first()
        
    # 会社が見つからないときは、会社の一覧にリダイレクト
    if not company:
        return redirect('master:company_search_list')
    
    # 会社データをフォームに入れる
    form = CompanyForm(instance=company)           
    
    # 出力用フォームの設定
    form=create_form(form)
    
    return render(request, 'master/company_create_result.html', {
        'form': form
    }) 


# 会社を検索する
@login_required
def company_search_list(request):
    
    if not request.user.has_perm('stocks.view_company'):
        return HttpResponse("あなたは企業の削除権限が付与されていません。")

    form = CompanySearchForm(request.GET or None)
    companies = Company.objects.all().select_related('market__country').order_by('name_en')

    if request.method == "GET" and form.is_valid():
        name = form.cleaned_data.get('name')
        industry = form.cleaned_data.get('industry')
        market = form.cleaned_data.get('market')

        filled_fields = sum(bool(v) for v in [name, industry, market])

        # pageパラメータのみの場合（次へ・前へ）はスルー
        is_pagination_only = not any([name, industry, market]) and request.GET.get('page')

        if not is_pagination_only and (filled_fields == 0 or filled_fields > 1):
            messages.error(request, "検索条件は1つだけ指定してください。")
            return redirect('master:company_search_list')

        if name:
            companies = companies.filter(name_en__icontains=name) | companies.filter(name_jp__icontains=name)
        if industry:
            companies = companies.filter(industry=industry)
        if market:
            companies = companies.filter(market=market)

    paginator = Paginator(companies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'master/company_search_list.html', {
        'form': form,
        'companies': page_obj,
        'page_obj': page_obj
    })


# 会社の詳細を表示
@login_required
def company_read(request,symbol):
    # ログイン中のユーザーが管理者権限を付与されているか確認
    if not request.user.has_perm('stocks.view_company'):
        return HttpResponse("あなたは企業の削除権限が付与されていません。")
    
    # リクエストがPOSTメソッドかどうかをチェック
    if request.method == 'POST':
        # 押されたボタンが「編集する」ボタンの場合
        if 'go_update' in request.POST:
            return redirect(
                'master:company_update',
                symbol=symbol
            )       
    
    # 選択した企業を取得
    company = Company.objects.filter(symbol=symbol).first()
    
    # 会社が見つからないときは、会社の一覧にリダイレクト
    if not company:
        return redirect('master:company_search_list')
    
    # 会社データをフォームに入れる
    form = CompanyForm(instance=company)           
    
    # 出力用フォームの設定
    form=create_form(form)
  
    return render(request, 'master/company_read.html', {
        'form': form
    })
    

# 会社の情報を編集
@login_required
def company_update(request,symbol):
    # ログイン中のユーザーが管理者権限を付与されているか確認
    if not request.user.has_perm('stocks.change_company'):
        return HttpResponse("あなたは企業の編集権限が付与されていません。")
    
    # 選択した企業を取得
    company = Company.objects.filter(symbol=symbol).first()
    
    # 会社が見つからないときは、会社の一覧にリダイレクト
    if not company:
        return redirect('master:company_search_list')
    
    # リクエストがPOSTメソッドかどうかをチェック
    if request.method == 'POST':
        # データベースから取得し、変更内容をフォームの値で上書き
        form = CompanyForm(request.POST, instance=company)

        # 入力値が正しいか
        if form.is_valid():
            # データベースに保存
            form.save()
            return redirect(
                'master:company_update_result',
                symbol=symbol
            )
        # エラーの重複を外す
        unique_errors=errnote_check(form)
        return render(request, 'master/company_update.html', {
            'unique_errors': unique_errors,
            'form': form
            })
      
    # 会社データをフォームに入れる
    form = CompanyForm(instance=company)           

    return render(request, 'master/company_update.html', {
        'form': form
    })


# 編集の結果
@login_required
def company_update_result(request,symbol):
    # ログイン中のユーザーが管理者権限を付与されているか確認
    if not request.user.has_perm('stocks.change_company'):
        return HttpResponse("あなたは企業の編集権限が付与されていません。")
    
    # 選択した企業を取得
    company = Company.objects.filter(symbol=symbol).first()
        
    # 会社が見つからないときは、会社の一覧にリダイレクト
    if not company:
        return redirect('master:company_search_list')
    
    # 会社データをフォームに入れる
    form = CompanyForm(instance=company)           
    
    # 出力用フォームの設定
    form=create_form(form)
    
    return render(request, 'master/company_update_result.html', {
        'form': form
    })


# 会社を整理する前の最終確認
@login_required
def company_delete(request, symbol):
    # ログイン中のユーザーが管理者権限を付与されているか確認
    if not request.user.has_perm('stocks.delete_company'):
        return HttpResponse("あなたは企業の削除権限が付与されていません。")

    # 選択した企業を取得
    company = Company.objects.filter(symbol=symbol).first()
        
    # 会社が見つからないときは、会社の一覧にリダイレクト
    if not company:
        return redirect('master:company_search_list')
    
    # リクエストがPOSTメソッドかどうかをチェック
    if request.method == 'POST':
        # 押されたボタンが「決定」ボタンの場合
        if 'go_delete' in request.POST:
            company.delete()
            return redirect('master:company_delete_result')
        
    # 会社データをフォームに入れる
    form = CompanyForm(instance=company)  

    # 出力用フォームの設定
    form=create_form(form)

    return render(request, 'master/company_delete.html', {
        'form': form
    })


# 会社を一覧から外した後の画面
@login_required
def company_delete_result(request):
    # ログイン中のユーザーが管理者権限を付与されているか確認
    if not request.user.has_perm('stocks.delete_company'):
        return HttpResponse("あなたは企業の削除権限が付与されていません。")
    return render(request, 'master/company_delete_result.html')

# 出力用フォームの設定
def create_form(form):
    # フォームからフィールドと名前を取得   
    for name, field in form.fields.items():                  
        # フィールドがModelChoiceFieldかどうか
        if isinstance(field, forms.ModelChoiceField):
            field.widget = forms.TextInput()                # テキスト入力に入れ替え
            instance = getattr(form.instance, name, None)   # nameの値を取得
            if instance:
                form.initial[name] = str(instance)          # __str__()の値を代入
        # フォームを読み取り専用にして入力不可
        field.widget.attrs['readonly'] = True
        # フォームにCSSクラスを追加
        field.widget.attrs['class'] = 'is-readonly'

    return form
