import django.forms
from django import forms
from django.forms import inlineformset_factory, TextInput

import bistroo.settings
from .models import *


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['number', 'name']
        widgets = {
            'number': forms.TextInput(attrs={'type': 'text', 'class': 'form-control mb-2'}),
            'name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        }


class MenuHeadlinesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MenuHeadlinesForm, self).__init__(*args, **kwargs)
        # self.fields['date'].widget = forms.widgets.TextInput(attrs={'type': 'date', 'class': 'form-control mb-2'})
        self.fields['date'].label = 'Kuupäev'
        self.fields['teema'].label = 'Päevateema'
        self.fields['soovitab'].label = 'Peakokk'
        self.fields['valmistas'].label = 'Kes valmistas'

    class Meta:
        model = MenuHeadlines
        fields = ['date', 'teema', 'soovitab', 'valmistas']
        widgets = {
            # 'date': django.forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date': TextInput(attrs={'type': 'text',  'id': 'date', 'class': 'form-control',
                                     'placeholder': 'Kliki kuupäeva valimiseks', 'readonly': 'readonly'}),

            'teema': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'soovitab': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'valmistas': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),

        }

    def clean(self):
        super(MenuHeadlinesForm, self).clean()
        teema = self.cleaned_data['teema']
        soovitab = self.cleaned_data['soovitab']

        if (teema is None and soovitab is not None) or (teema is not None and soovitab is None):
            self.add_error('teema', ValidationError('Teemapäev ja soovitab peavad mõlemad olema täidetud!'))


class MenuHeadlinesUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MenuHeadlinesUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['date'].widget = forms.widgets.TextInput(attrs={'type': 'date', 'class': 'form-control mb-2'})
        self.fields['date'].label = 'Kuupäev'
        self.fields['teema'].label = 'Päevateema'
        self.fields['soovitab'].label = 'Peakokk'
        self.fields['valmistas'].label = 'Kes valmistas'

    class Meta:
        model = MenuHeadlines
        fields = ['date', 'teema', 'soovitab', 'valmistas']
        widgets = {
            'date': django.forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'teema': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'soovitab': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'valmistas': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),

        }

    def clean(self):
        # super(MenuHeadlinesUpdateForm, self).clean()
        # soovitab = self.cleaned_data['soovitab']
        # teema = self.cleaned_data['teema']

        cleaned_data = super().clean()
        soovitab = cleaned_data.get('soovitab')
        teema = cleaned_data.get('teema')

        # if (self.teema is None and self.soovitab is not None) or (self.teema is not None and self.soovitab is None):
        #     self.add_error('teema', 'Teemapäev ja soovitab peavad mõlemad olema täidetud!')
        if (teema is None and soovitab is not None) or (teema is not None and soovitab is None):
            self.add_error('teema', 'Teemapäev ja soovitab peavad mõlemad olema täidetud!')


class FoodMenuUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FoodMenuUpdateForm, self).__init__(*args, **kwargs)

        # self.fields['name'].widget = forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control mb-2'})
        self.fields['food'].label = 'Toit'
        self.fields['full_price'].label = 'Täis hind'
        self.fields['half_price'].label = 'Pool hinda'
        self.fields['show_in_menu'].label = 'Näita menüüs'
        # self.fields['DELETE'].label = 'Kustuta'

    class Meta:
        model = FoodItem
        fields = ['food', 'full_price', 'half_price', 'show_in_menu']
        widgets = {
            'food': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'full_price': django.forms.TextInput(attrs={'type': 'number', 'class': 'form-control', 'step': 0.01}),
            'half_price': django.forms.TextInput(attrs={'type': 'number', 'class': 'form-control', 'step': 0.01}),
            'show_in_menu': django.forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # 'DELETE': django.forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FoodMenuCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FoodMenuCreateForm, self).__init__(*args, **kwargs)

        self.fields['date'].label = 'Kuupäev'
        self.fields['category'].label = 'Kategooria'

    class Meta:
        model = FoodMenu
        fields = ['date', 'category']
        widgets = {
            'date': django.forms.Select(attrs={'type': 'date', 'class': 'form-control mb-2 form-select'}),
            'category': django.forms.Select(attrs={'class': 'form-control form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        category = cleaned_data.get('category')

        if FoodMenu.objects.filter(date=date, category=category).exists():
            raise ValidationError(
                f"Uut '{category}' kategooriat ei saa sellele kuupäevale sisestada, kuna see on juba olemas.")

        return cleaned_data


FoodMenuFormset = inlineformset_factory(
    FoodMenu,
    FoodItem,
    extra=5,
    form=FoodMenuUpdateForm,
    fields=('food', 'full_price', 'half_price', 'show_in_menu',))
