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

    path('toiduNimed_list/', views.ToiduNimedListView.as_view(), name='toiduNimed_list'),
    path('toiduNimed_create/', views.ToiduNimedCreateView.as_view(), name='toiduNimed_create'),
    path('toiduNimed_update/<int:pk>', views.ToiduNimedUpdateView.as_view(), name='toiduNimed_update'),
    path('toiduNimed_delete/<int:pk>', views.ToiduNimedDeleteView.as_view(), name='toiduNimed_delete')


]