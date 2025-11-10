from django.db import models

# 企業情報テーブル
class Company(models.Model):
    symbol = models.CharField(max_length=17, primary_key=True, editable=False)  # 銘柄コード
    name_en = models.CharField(max_length=255)                                  # 企業名（英名）
    name_jp = models.CharField(max_length=255, null=True, blank=True)           # 企業名（日本語）                         
    industry = models.ForeignKey('Industry', on_delete=models.PROTECT)          # 外部キー（業界情報テーブル）
    market = models.ForeignKey('Market', on_delete=models.PROTECT)              # 外部キー（市場情報テーブル））
    memo = models.TextField(blank=True)                                         # メモ

    # 銘柄コードを採番（業界コード＋数字7桁）
    def save(self, *args, **kwargs):
        if not self.symbol:
            last = Company.objects.filter(industry=self.industry).order_by('-symbol').first()
            if last:
                code_len = len(self.industry.code)
                last_num = int(last.symbol[code_len:])
            else:
                last_num = 0
            self.symbol = f"{self.industry.code}{last_num + 1:07d}"  # 7桁に変更
        super().save(*args, **kwargs)

    
    # 出力用（銘柄コード・会社名）
    def __str__(self):
        return f"{self.symbol} - {self.name_en}"


# 業界情報テーブル
class Industry(models.Model):
    code = models.CharField(max_length=10, primary_key=True)    # 業界コード   
    name_jp = models.CharField(max_length=50)                   # 業界名（日本語）
    name_en = models.CharField(max_length=100)                  # 業界名（英語）
    sector = models.ForeignKey('Sector', on_delete=models.CASCADE, related_name='industries',null=True)
    description = models.TextField(blank=True)                  # 説明
    created_at = models.DateTimeField(auto_now_add=True)        # 登録日時

    # 出力用（業界コード・業界名）
    def __str__(self):
        return f"{self.code} - {self.name_jp}"

# セクターテーブル 
class Sector(models.Model):
    name_jp = models.CharField(max_length=100,unique=True)     # 日本語名unique=True
    name_en = models.CharField(max_length=100,unique=True)     # 英語名

    def __str__(self):
        return self.name_jp 
      

# 国情報テーブル
class Country(models.Model):
    code = models.CharField(max_length=3, primary_key=True)  # コード（英字）
    name = models.CharField(max_length=100)                  # 国名

    # 出力用（コード・国名）
    def __str__(self):
        return f"{self.code} - {self.name}"


# 市場情報テーブル
class Market(models.Model):
    code = models.CharField(max_length=50)                              # 市場コード（通称）
    name = models.CharField(max_length=100)                             # 市場名
    country = models.ForeignKey('Country', on_delete=models.PROTECT)    # 外部キー（国情報テーブル）
    
    # データの重複を回避する
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'country'],
                name='unique_market_per_country'
            )
        ]

    # 出力用（市場コード・市場名）
    def __str__(self):
        return f"{self.code} ({self.name})"
    

# 市場の指数種類テーブル（指数名マスタ）
class MarketIndexType(models.Model):
    code = models.CharField(max_length=20, primary_key=True)    # 種類コード
    name = models.CharField(max_length=100)                     # 名称
    description = models.TextField(blank=True)                  # 備考

    # 出力用（種類コード・名称）
    def __str__(self):
        return self.name


# 市場指数テーブル
class MarketIndex(models.Model):
    market = models.ForeignKey('Market', on_delete=models.CASCADE)                              # 外部キー（市場情報テーブル）
    index_type = models.ForeignKey('MarketIndexType', on_delete=models.CASCADE)                 # 外部キー（指数種類テーブル）
    date = models.DateField()                                                                   # 日付
    index_value = models.DecimalField(max_digits=8, decimal_places=2)                           # 株価指数
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # 金利
    gdp_growth = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)     # GDP成長率
    notes = models.TextField(blank=True)

    # データの重複を回避する
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['market', 'index_type', 'date'],
                name='unique_market_index'
            )
        ]

    # 出力用（市場名・指数名・日付・株価指数）
    def __str__(self):
        return f"{self.market.name} - {self.index_type.name} - {self.date} - {self.index_value}"


# 分次株価テーブル
class StockPrice(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)                                # 外部キー（企業情報テーブル）
    date = models.DateTimeField()                                                                   # 株価の日付
    open_price = models.DecimalField(max_digits=10, decimal_places=2)                               # 始値
    high_price = models.DecimalField(max_digits=10, decimal_places=2)                               # 高値
    low_price = models.DecimalField(max_digits=10, decimal_places=2)                                # 安値
    close_price = models.DecimalField(max_digits=10, decimal_places=2)                              # 終値
    adjusted_close = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)     # 調整後終値
    volume = models.BigIntegerField(blank=True, null=True)                                          # 出来高
    dividend = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)          # 配当額
    split_coefficient = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # 株式分割

    # データの重複を回避する
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'date'], 
                name='unique_company_date'
            )
        ]
        indexes = [
            models.Index(fields=['company', 'date']),
        ]

    # 出力用（会社名・日付・終値）
    def __str__(self):
        return f"{self.company.name_en} - {self.date} - {self.close_price}"


# 業界の日次株価指数
class IndustryIndex(models.Model):
    industry = models.ForeignKey('Industry', on_delete=models.CASCADE)                              # 外部キー（業界情報テーブル）
    date = models.DateField()                                                                       # 日付
    index_value = models.DecimalField(max_digits=8, decimal_places=2)                               # 日次指数
    adjusted_index = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)     # 配当調整等
    volume = models.BigIntegerField(blank=True, null=True)                                          # 出来高
    notes = models.TextField(blank=True)                                                            # 備考

    # データの重複を回避する
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['industry', 'date'], 
                name='unique_industry_date'
            )
        ]
        ordering = ['industry', 'date']  #日付順

    # 出力用（業界名・日付・日次指数）
    def __str__(self):
        return f"{self.industry.name_jp} - {self.date} - {self.index_value}"

