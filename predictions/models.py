from django.db import models
from stocks.models import Company, Industry

# 会社単位の株価予測テーブル
class StockPrediction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)                          # 外部キー（企業情報テーブル）
    write_date = models.DateField(auto_now_add=True)                                        # 登録日
    target_date = models.DateField()                                                        # 予測対象日
    prediction_price = models.DecimalField(max_digits=10, decimal_places=2)                 # 予測株価
    coefficient = models.DecimalField(max_digits=8, decimal_places=4)                       # 係数
    delta = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)       # 実績との差分
    notes = models.TextField(blank=True)                                                    # 備考

    # データの重複を回避する
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'target_date'], 
                name='unique_prediction'
            )
        ]
    
    # 出力用（会社名・予測対象日・予測株価・係数）
    def __str__(self):
        return f"{self.company.name} - {self.target_date} - {self.prediction_price} - {self.coefficient}"


# 業界単位の株価予測テーブル
class IndustryPrediction(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)            # 業界コード
    write_date = models.DateField(auto_now_add=True)                            # 登録日
    target_date = models.DateField()                                            # 予測対象日
    prediction_price = models.DecimalField(max_digits=10, decimal_places=2)     # 予測値
    coefficient = models.DecimalField(max_digits=8, decimal_places=4)           # 係数
    notes = models.TextField(blank=True)                                        # 備考
    
    # 重複を回避する
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['industry', 'target_date'], 
                name='unique_industry_prediction'
            )
        ]

    # 出力用（業界名・予測対象日・予測値・係数）
    def __str__(self):
        return f"{self.industry.name} - {self.target_date} - {self.prediction_price} - {self.coefficient}"