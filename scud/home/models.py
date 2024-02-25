from django.db import models
from io import BytesIO
from django.core.files import File


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/images')

    def __str__(self) -> str:
        return self.name

    
class Model(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='static/images')

    def __str__(self) -> str:
        return self.name

class Responsible(models.Model):
    fullname = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        return self.fullname

class Plant(models.Model):
    category_id = models.ForeignKey(Category, related_name='category', on_delete=models.PROTECT, blank=True)
    room_number = models.CharField(max_length=4)
    inventar_number = models.IntegerField(unique=True, blank=True)
    model_id = models.ForeignKey(Model, on_delete=models.PROTECT, blank=True)
    responsible_id = models.ForeignKey(Responsible, on_delete=models.PROTECT)
    processor = models.CharField(max_length=70, blank=True)
    memory = models.CharField(max_length=70, blank=True)
    mac_address = models.CharField(max_length=50, blank=True)
    ip_address = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=40, null=True, default='В сети')

    def __str__(self) -> str:
        return str(self.inventar_number)

  