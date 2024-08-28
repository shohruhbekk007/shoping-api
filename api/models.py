from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class Mahsulot(models.Model):
    nomi = models.CharField(max_length=255)
    narxi = models.DecimalField(max_digits=10, decimal_places=2)
    olingan_narxi = models.DecimalField(max_digits=10, decimal_places=2)
    dona = models.IntegerField()
    rasm = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.nomi

class Xaridor(models.Model):
    nomi = models.CharField(max_length=255)
    telefon_raqami = models.CharField(max_length=20)
    maxsulot_nomi = models.ForeignKey(to=Mahsulot, on_delete=models.CASCADE)
    oladigan_maxsulot_soni = models.IntegerField()
    umumiy_savdo = models.DecimalField(max_digits=10, decimal_places=2)
    qarzdor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nomi} - {self.maxsulot_nomi.nomi}"

class Partiya(models.Model):
    sana = models.DateField()
    umumiy_summa = models.DecimalField(max_digits=10, decimal_places=2)
    qanchadan_olingani = models.DecimalField(max_digits=10, decimal_places=2)
    nomi = models.ForeignKey(to=Mahsulot, on_delete=models.CASCADE)
    qanchadan_sotiladigani = models.DecimalField(max_digits=10, decimal_places=2)
    keladigan_maxsulot_soni = models.IntegerField()
    rasm = models.ImageField(upload_to='batch_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.nomi:
            sklad, created = Sklad.objects.get_or_create(mahsulot=self.nomi)
            sklad.narxi = self.qanchadan_sotiladigani
            sklad.dona = (sklad.dona or 0) + self.keladigan_maxsulot_soni
            sklad.save()

    def __str__(self):
        return f"Partiya: {self.nomi.nomi} - {self.sana}"

class Sklad(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)
    dona = models.IntegerField(default=0)  # Default value of 0
    narxi = models.DecimalField(max_digits=10, decimal_places=2)
    rasm = models.ImageField(upload_to='warehouse_images/', null=True, blank=True)

    def __str__(self):
        return f"Sklad: {self.mahsulot.nomi} - {self.dona} dona"

class Sotuv(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)
    xaridor = models.ForeignKey(Xaridor, on_delete=models.CASCADE)
    sana = models.DateField(auto_now_add=True)
    sotilgan_dona = models.IntegerField()
    sotilgan_narx = models.DecimalField(max_digits=10, decimal_places=2)
    qarzdor = models.BooleanField(default=False)
    olingan_summa = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.mahsulot:
            sklad = Sklad.objects.filter(mahsulot=self.mahsulot).first()
            if sklad:
                if sklad.dona >= self.sotilgan_dona:
                    sklad.dona -= self.sotilgan_dona
                    sklad.save()
                else:
                    raise ValueError("Skladda yetarli miqdordagi mahsulot yo'q.")

    def __str__(self):
        return f"Sotuv: {self.mahsulot.nomi} - {self.sotilgan_dona} dona"
