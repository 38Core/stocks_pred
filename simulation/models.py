from django.db import models
from django.contrib.auth.models import User
from stocks.models import Company

#日次シミュレーション結果テーブル
class SimulationDailyResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)                                        #外部キー（ユーザー情報テーブル）
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)         #外部キー（企業情報テーブル）
    strategy_name = models.CharField(max_length=100)                                                #戦略名
    date = models.DateField()                                                                       #日付
    total_value = models.DecimalField(max_digits=15, decimal_places=2)                              #合計資産
    daily_drawdown = models.DecimalField(max_digits=10, decimal_places=4,blank=True, null=True)     #日次ドローダウン

    #重複を回避する
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'company', 'strategy_name', 'date'],
                name='unique_user_company_strategy_date'
            )       
        ]
 

    #出力用（ユーザー名・日付・総資産
    def __str__(self):
        return f"{self.user.username} - {self.date} : {self.total_value}"
