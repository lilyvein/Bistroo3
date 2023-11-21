import datetime
from django.db import models
from django.core.exceptions import ValidationError



class Category(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=255)

    def __str__(self):
        """ Admin page show info """
        return self.name

    class Meta:
        """ Default result ordering """
        ordering = ['number']
        verbose_name_plural = 'categories'


class MenuHeadlines(models.Model):
    date = models.DateField()
    teema = models.CharField(max_length=255, null=True, blank=True)
    soovitab = models.CharField(max_length=255, null=True, blank=True)
    valmistas = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        """ Admin page show info """
        return f'{self.date}, {self.teema}, {self.soovitab}, {self.valmistas}'

    class Meta:
        """ Default result ordering """
        ordering = ['-date']   # - märk annab sorteerimise nii et tuleviku kuupäevad on ennem ja vanemad allpool
        verbose_name_plural = 'menuheadlines'

    def clean(self):
        if (self.teema is not None and self.soovitab is None) or (self.teema is None and self.soovitab is not None):
            raise ValidationError('Teemapäev ja peakokk peavad mõlemad olema täidetud!')


class ToiduNimed(models.Model):
    date = models.DateField()
    category_ID = models.ForeignKey(Category, on_delete=models.CASCADE)   # cascade kustutab kogu info sellel catekoorial
    food_name = models.CharField(max_length=255, null=True, blank=False)
    full_price = models.DecimalField(max_digits=4, decimal_places=2,)   # kogu numbrite arv ja komakohtade arv
    half_price = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)   # väljad võivad olla ka tühjad
    show_menu = models.BooleanField(default=True)
    def __str__(self):
        """ Admin page show info """
        return f'{self.date}, {self.category_ID}, {self.food_name}, {self.full_price}, {self.half_price}, {self.show_menu}'

    class Meta:
        """ Default result ordering """
        ordering = ['-date', 'category_ID']   # - märk annab sorteerimise nii et tuleviku kuupäevad on ennem ja vanemad allpool
