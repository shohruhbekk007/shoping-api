from django.db import models

class Xaridor(models.Model):
    ism = models.CharField(max_length=255)
    telefon = models.CharField(max_length=15)
    manzil = models.CharField(max_length=255)
    ummumiy_savdo = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    qarzdorlik = models.BooleanField(default=False, null=True, blank=True)
    qarz_miqdori = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        return self.ism


class QarzlarniSondirish(models.Model):
    xaridor = models.ForeignKey(Xaridor, on_delete=models.CASCADE)
    tolangan_miqdor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    toliq_tolash = models.BooleanField(default=False)
    sana = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.xaridor.ism} - {self.tolangan_miqdor if self.tolangan_miqdor else 'Toliq qarz'} to'landi"
    


class Maxsulotlar(models.Model):
    maxsulot_nomi = models.CharField(max_length=255)
    sotiladigan_narx = models.DecimalField(max_digits=10, decimal_places=2)
    miqdori = models.PositiveIntegerField()
    rasm = models.ImageField(upload_to='maxsulotlar_rasm/', null=True, blank=True)
    sana = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.maxsulot_nomi

class Partiya(models.Model):
    maxsulot_nomi = models.CharField(max_length=255)
    maxsulot_sotib_olingan_narx = models.DecimalField(max_digits=10, decimal_places=2)
    maxsulot_soni = models.PositiveIntegerField()
    sotilishi_kutulyotgan_narx = models.DecimalField(max_digits=10, decimal_places=2)
    rasm = models.ImageField(upload_to='partiya_rasm/', blank=True, null=True)

    def __str__(self):
        return self.maxsulot_nomi
    
class Sotuv(models.Model):
    xaridor_ismi = models.ForeignKey(Xaridor, on_delete=models.SET_NULL, null=True, blank=True)
    maxsulotlar = models.ForeignKey(Maxsulotlar, on_delete=models.CASCADE)
    maxsulotning_jami_summasi = models.DecimalField(max_digits=10, decimal_places=2)
    qarz_summa = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sana = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sotuv: {self.xaridor_ismi} - {self.sana}" 


class SotuvItem(models.Model):
    sotuv = models.ForeignKey(Sotuv, on_delete=models.CASCADE)
    maxsulot = models.ForeignKey(Maxsulotlar, on_delete=models.CASCADE)
    maxsulot_soni = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.maxsulot} - {self.maxsulot_soni} dona"