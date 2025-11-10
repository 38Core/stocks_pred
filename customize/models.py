from django.db import models
from django.contrib.auth.models import User
from stocks.models import Company

# ユーザーのお気に入り企業
class FavoriteCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)          # 外部キー（ユーザー情報テーブル）
    company = models.ForeignKey(Company, on_delete=models.CASCADE)    # 外部キー（企業情報テーブル）
    added_at = models.DateTimeField(auto_now_add=True)                # 登録日時
    
    # 重複を回避する
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'company'], 
                name='unique_user_company'
            )
        ]

    # 出力用（ユーザー名・銘柄コード）
    def __str__(self):
        return f"{self.user.username} favorites {self.company.symbol}"

