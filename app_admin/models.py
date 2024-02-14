import datetime

from django.urls import reverse
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
        #return f'{self.date}, {self.teema}, {self.soovitab}, {self.valmistas}'
        return f'{self.date.strftime("%d.%m.%Y")}'

    class Meta:
        """ Default result ordering """
        ordering = ['-date']   # - märk annab sorteerimise nii et tuleviku kuupäevad on ennem ja vanemad allpool
        verbose_name_plural = 'menuheadlines'

    def clean(self):
        if (self.teema is None and self.soovitab is not None) or (self.teema is not None and self.soovitab is None):
            raise ValidationError('Teemapäev ja soovitab peavad mõlemad olema täidetud!')


class FoodMenu(models.Model):
    date = models.ForeignKey(MenuHeadlines, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date', 'category_id']

    def get_absolute_url(self):
        return reverse('app_admin:foodmenu_update', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.date} {self.category}'


class FoodItem(models.Model):
    menu = models.ForeignKey(FoodMenu, on_delete=models.CASCADE, related_name='food_fooditem')
    food = models.CharField(max_length=50)
    full_price = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
    half_price = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    show_in_menu = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['menu']

    def __str__(self):
        return f'{self.menu}'




