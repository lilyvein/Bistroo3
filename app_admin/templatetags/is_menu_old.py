from datetime import datetime, date
from django import template

register = template.Library()


@register.filter
def is_menu_old(menu_date):
    # menu_date on kujul # d.m.Y
    #https://stackoverflow.com/questions/64605335/comparing-dates-using-a-comparator-inside-django-template
    date_object = datetime.strptime(menu_date, '%d.%m.%Y').date()
    today = date.today()  # tänane kuupäev
    return date_object < today  # true v false
