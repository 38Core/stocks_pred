from django.contrib import admin
from .models import Company,Industry,Sector,Country,Market,MarketIndexType,MarketIndex,StockPrice,IndustryIndex

admin.site.register(Company)
admin.site.register(Industry)
admin.site.register(Sector)
admin.site.register(Country)
admin.site.register(Market)
admin.site.register(MarketIndexType)
admin.site.register(MarketIndex)
admin.site.register(StockPrice)
admin.site.register(IndustryIndex)
