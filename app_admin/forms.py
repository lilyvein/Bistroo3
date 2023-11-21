import django.forms
from django import forms
import bistroo.settings
from .models import *


class MenuHeadlinesCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.widgets.TextInput(attrs={'type': 'date', 'class': 'form-control mb-2'})
        self.fields['date'].label = 'Kuupäev'
        """for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2'
            visible.field.widget.attrs['placeholder'] = visible.field.label"""

    class Meta:
        model = MenuHeadlines
        widgets = {
            'date': django.forms.TextInput(attrs={'type':'date', 'class':'form-control'}),
            'teema': django.forms.TextInput(attrs={'type':'text', 'class':'form-control'}),
            'soovitab': django.forms.TextInput(attrs={'type':'text', 'class':'form-control'}),
            'valmistas': django.forms.TextInput(attrs={'type':'text', 'class':'form-control'}),

        }
        fields = ('date', 'teema', 'soovitab', 'valmistas')
        """labels = {
            'date': 'Kuupäev',
            'teema': 'Teemapäev',
            'soovitab': 'Soovitab',
            'valmistas': 'Valmistab',

        }"""


class ToiduNimedCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['date'].widget = forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control mb-2'})
        self.fields['date'].label = 'Kuupäev'
        self.fields['category_ID'].label = 'Kategooria'
        self.fields['food_name'].label = 'Toidu nimi'
        self.fields['full_price'].label = 'Täis hind'
        self.fields['half_price'].label = 'Pool hinda'
        self.fields['show_menu'].label = 'Näitab menüüs'

    class Meta:
        model = ToiduNimed
        fields = ('date', 'category_ID', 'food_name', 'full_price','half_price', 'show_menu')
        widgets = {
            'date': django.forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category_ID': django.forms.Select(attrs={'type': 'category_ID', 'class': 'form-control'}),
            'food_name': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'full_price': django.forms.TextInput(attrs={'type': 'number', 'class': 'form-control'}),
            'half_price': django.forms.TextInput(attrs={'type': 'number', 'class': 'form-control'}),
            'show_menu': django.forms.CheckboxInput(attrs={'class': 'form-control form-check-input'}),
        }


class CategoryCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number'].label = 'Kategooria number'
        self.fields['name'].label = 'Kategooria nimi'

    class Meta:
        model = Category
        fields = ('number', 'name')
        widgets = {
            'number': django.forms.TextInput(attrs={'type': 'number', 'class': 'form-control'}),
            'name': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        }

        fields = ('number', 'name')
