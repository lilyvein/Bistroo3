from django.urls import path
from . import views

app_name = 'app_admin'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),  # homepage
    path('category_list/', views.CategoryListView.as_view(), name='category_list'),
    path('category_create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category_update/<int:pk>', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('menuHeadlines_list/', views.MenuHeadlinesListView.as_view(), name='menuHeadlines_list'),
    path('menuHeadlines_create/', views.MenuHeadlinesCreateView.as_view(), name='menuHeadlines_create'),
    path('menuHeadlines_update/<int:pk>', views.MenuHeadlinesUpdateView.as_view(), name='menuHeadlines_update'),
    path('menuHeadlines_delete/<int:pk>', views.MenuHeadlinesDeleteView.as_view(), name='menuHeadlines_delete'),

    path('foodmenu_list/', views.FoodMenuListView.as_view(), name='foodmenu_list'),
    path('foodmenu_create/', views.FoodMenuCreateView.as_view(), name='foodmenu_create'),
    path('foodmenu_update/<int:pk>/', views.FoodMenuUpdateView.as_view(), name='foodmenu_update'),
    path('foodmenu_detail/<int:pk>/', views.FoodMenuDetailView.as_view(), name='foodmenu_detail'),
    path('foodmenu_delete/<int:pk>/', views.FoodMenuDeleteView.as_view(), name='foodmenu_delete'),

    path('history_list/', views.HistoryListView.as_view(), name='history_list'),
    path('history_search/', views.SearchResultsListView.as_view(), name='history_search'),
    path('history_menu/menu/', views.OldMenuListView.as_view(), name='history_menu'),

]