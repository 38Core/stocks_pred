# views.py
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FavoriteCompany
from stocks.models import Company

# お気に入り企業を登録・解除
@login_required
def favorite(request, symbol):
    # 指定した企業を取得
    company = get_object_or_404(Company, symbol=symbol)
    
    # データベースを確認ない場合は新規作成（レコード・作成の有無）
    fav, created = FavoriteCompany.objects.get_or_create(
        user=request.user,
        company=company
    )

    # 既にあれば削除（＝お気に入り解除）
    if not created:
        fav.delete()

    # 元のページに戻る
    return redirect(request.META.get("HTTP_REFERER", "stocks:company_list"))

# ログインユーザーのお気に入り企業をリスト表示
@login_required
def favorite_companies(request):
    # 登録している企業をアルファベット順に並び替えて取得
    favorite_companies = Company.objects.filter(
        favoritecompany__user=request.user
    ).order_by('name_en')

    # ハートマークをTRUEにするためのデータを格納
    for c in favorite_companies:
        c.is_favorite = True

    return render(request, 'customize/favorite_companies.html', {
        'companies': favorite_companies
    })
