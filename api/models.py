from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Products(models.Model):
    name = models.CharField(max_length=250)
    images = models.ImageField(upload_to="Images/party", null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    

class Warehouse(models.Model):
    name = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    number = models.IntegerField()
    money_was_token = models.DecimalField(max_digits=15, decimal_places=2)
    money_to_was = models.DecimalField(max_digits=15, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Partys(models.Model):
    name = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    number = models.IntegerField()
    money_was_token = models.DecimalField(max_digits=15, decimal_places=2)
    money_to_was = models.DecimalField(max_digits=15, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Buyers(models.Model):
    users = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=50, null=True)
    name = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    number = models.IntegerField()
    money_to_was = models.DecimalField(max_digits=15, decimal_places=2)
    debtor = models.BooleanField()

    def __str__(self) -> str:
        return self.users


from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender=Partys)
def update_warehouse_on_partys_save(sender, instance, **kwargs):
    try:
        warehouse = Warehouse.objects.get(name=instance.name)
        warehouse.money_was_token = instance.money_was_token
        warehouse.money_to_was = instance.money_to_was
        warehouse.number += instance.number
        warehouse.save()
    except ObjectDoesNotExist:
        warehouse = Warehouse.objects.create(
            name=instance.name,
            number=instance.number,
            money_was_token=instance.money_was_token,
            money_to_was=instance.money_to_was
        )
        warehouse.save()


@receiver(post_save, sender=Buyers)
def update_warehouse_on_buyers_save(sender, instance, **kwargs):
    warehouse = Warehouse.objects.get(name=instance.name)
    warehouse.number -= instance.number
    warehouse.save()
