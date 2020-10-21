from django.db import models

# Create your models here.

class Meta:
    app_label  = 'cars'

class TheCar(models.Model):

    make = models.TextField()
    model = models.TextField()
    rate1 = models.IntegerField(default=0)
    rate2 = models.IntegerField(default=0)
    rate3 = models.IntegerField(default=0)
    rate4 = models.IntegerField(default=0)
    rate5 = models.IntegerField(default=0)
    rates = models.IntegerField(default=0)

    def __str__(self):
        return self.model