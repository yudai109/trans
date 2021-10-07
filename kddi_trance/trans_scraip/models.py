from django.db import models

class Transdata(models.Model):
    date = models.CharField(max_length = 100, verbose_name="日付", null=True, blank=False)
    shop = models.CharField(max_length = 100, verbose_name="店舗名", null=True, blank=False)
    name = models.CharField(max_length = 100, verbose_name="スタッフ名", null=True, blank=False)
    departure = models.CharField(max_length = 100, verbose_name="出発場所", null=True, blank=False)
    destination = models.CharField(max_length = 100, verbose_name="到着場所", null=True, blank=False)
    fast_low = models.CharField(max_length = 100, verbose_name="最安/最落", null=True, blank=False)
    tokyu = models.CharField(max_length = 100, verbose_name="特急", null=True, blank=False)
    # oneway = models.CharField(max_length = 100, verbose_name="片道料金", null=True, blank=False)
    # roundway = models.CharField(max_length = 100, verbose_name="往復料金", null=True, blank=False)
    # sumPrise = models.CharField(max_length = 100, verbose_name="合計料金", null=True, blank=False)
    oneway = models.PositiveIntegerField(verbose_name="片道料金", null=True, blank=True)
    roundway = models.PositiveIntegerField(verbose_name="往復料金", null=True, blank=True)
    sumPrise = models.PositiveIntegerField(verbose_name="合計料金", null=True, blank=True)
    discription = models.TextField(max_length = 500, verbose_name="経路詳細", null=True, blank=True)

    class Meta:
        verbose_name = '交通費履歴'
        verbose_name_plural = '交通費履歴'

    def __str__(self):
        return self.date + "_" + self.shop
