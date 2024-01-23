from datetime import datetime

from django.shortcuts import render
from app_admin.models import FoodMenu, MenuHeadlines
from datetime import datetime
import locale


def show_menu(request):
    locale.setlocale(locale.LC_TIME, 'et_EE.utf-8')  # Eesti keele seadistamine
    current_datetime = datetime.now()
    date = current_datetime.date()

    q_result_foodmenu = FoodMenu.objects.filter(date__date=date).values(
        "category__name",
        "food_fooditem__food",
        "food_fooditem__full_price",
        "food_fooditem__half_price"
    ).order_by("category__number")

    q_result_menuheadlines = MenuHeadlines.objects.filter(date=date)
    formatted_date = current_datetime.strftime("%A, %d.%m.%Y")

    for item in q_result_foodmenu:
        if str(item["food_fooditem__full_price"]) > "0.00" and (
                str(item["food_fooditem__half_price"]) > "0.00" and str(item["food_fooditem__half_price"]) != "None"):
            item["food_fooditem__full_price"] = str(item["food_fooditem__full_price"]) + " / " + str(
                item["food_fooditem__half_price"])
        elif ((str(item["food_fooditem__full_price"]) == "0.00" and str(item["food_fooditem__half_price"]) == "0.00") or
              (str(item["food_fooditem__full_price"]) == "0.00" and str(item["food_fooditem__half_price"]) == "None")):
            item["food_fooditem__full_price"] = "Prae hinna sees"

    context = {
        "formatted_date": formatted_date,
        'foodmenu_items': q_result_foodmenu,
        'menuheadlines': q_result_menuheadlines,
    }
    return render(request, 'app_public/index.html', context)
