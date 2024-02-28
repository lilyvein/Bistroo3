import urllib.parse
from urllib.request import urlopen
import json

from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView, FormView)
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect, Http404
import datetime

from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ManagerRequiredMixin(UserPassesTestMixin):
    """ Test: user in group writer create and update """
    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()


class HomeView(ManagerRequiredMixin, TemplateView):
    template_name = 'app_admin/index.html'


class CategoryListView(ManagerRequiredMixin, ListView):
    model = Category
    queryset = Category.objects.order_by('number')
    context_object_name = 'categories'  # default object_list now teacher


class CategoryCreateView(ManagerRequiredMixin, CreateView):
    template_name = 'app_admin/category_form_create.html'
    model = Category
    success_url = reverse_lazy('app_admin:category_list')
    form_class = CategoryUpdateForm
    #fields = '__all__'


class CategoryUpdateView(ManagerRequiredMixin, UpdateView):
    template_name = 'app_admin/category_update.html'
    model = Category
    # fields = ['number', 'name']  # update only this fields
    success_url = reverse_lazy('app_admin:category_list')
    form_class = CategoryUpdateForm


class CategoryDeleteView(ManagerRequiredMixin, DeleteView):
    template_name = 'app_admin/category_delete.html'
    model = Category
    success_url = reverse_lazy('app_admin:category_list')
    form_class = CategoryUpdateForm


class MenuHeadlinesView(ManagerRequiredMixin, CreateView):
    model = MenuHeadlines
    form_class = MenuHeadlinesForm
    success_url = reverse_lazy('app_public:index')


class MenuHeadlinesListView(ManagerRequiredMixin, ListView):
    template_name = 'app_admin/menuHeadlines_list.html'
    model = MenuHeadlines
    #queryset = MenuHeadlines.objects.order_by('-date')  # Result ordered by kuupäev
    #queryset = MenuHeadlines.objects.all()  # Result ordered mis on juba modeliga sorteeritud ja
    # sellepärast pole meil nedi ridu vaja

    context_object_name = 'menuHeadlines'  # see tuleb viewst
    paginate_by = 10


class MenuHeadlinesUpdateView(ManagerRequiredMixin, UpdateView):

    template_name = 'app_admin/menuHeadlines_update.html'
    model = MenuHeadlines
    # fields = ['date', 'teema', 'soovitab', 'valmistas',]  # update only this fields
    success_url = reverse_lazy('app_admin:menuHeadlines_list')
    form_class = MenuHeadlinesUpdateForm
    context_object_name = 'menuHeadline'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True  # See võimaldab mallis eristada vormi lisamise ja muutmise vahel
        return context

    def form_valid(self, form):
        # Kui vorm on kehtiv, võite teha siin vajalikke toiminguid.
        return super().form_valid(form)


class MenuHeadlinesDeleteView(ManagerRequiredMixin, DeleteView):
    template_name = 'app_admin/menuHeadlines_delete.html'
    model = MenuHeadlines
    success_url = reverse_lazy('app_admin:menuHeadlines_list')


class MenuHeadlinesCreateView(ManagerRequiredMixin, CreateView):
    template_name = 'app_admin/menuHeadlines_create.html'
    model = MenuHeadlines
    # fields = '__all__'  # All fields into form
    success_url = reverse_lazy('app_admin:menuHeadlines_list')
    form_class = MenuHeadlinesForm

    def post(self, request, *args, **kwargs):
        my_data = request.POST
        my_date = my_data['date']
        print(my_date)
        try:
            new_date = datetime.datetime.strptime(my_date, '%d.%m.%Y').strftime('%Y-%m-%d')
            my_data._mutable = True
            my_data['date'] = new_date
            my_data._mutable = False
        except ValueError:
            return super().post(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)


class FoodMenuCreateView(ManagerRequiredMixin, CreateView):
    model = FoodMenu
    form_class = FoodMenuCreateForm
    template_name = 'app_admin/foodmenu_create.html'
    # fields = ['date', 'category', ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The menu has been added'
        )

        return super().form_valid(form)


class FoodMenuListView(ManagerRequiredMixin, ListView):
    model = FoodMenu
    template_name = 'app_admin/foodmenu_list.html'
    paginate_by = 10


class FoodMenuUpdateView(ManagerRequiredMixin, SingleObjectMixin, FormView):
    model = FoodMenu
    form_class = FoodMenuUpdateForm
    template_name = 'app_admin/foodmenu_update.html'


    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=FoodMenu.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=FoodMenu.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return FoodMenuFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('app_admin:foodmenu_detail', kwargs={'pk': self.object.pk})


class FoodMenuDetailView(ManagerRequiredMixin, DetailView):
    model = FoodMenu
    template_name = 'app_admin/foodmenu_detail.html'


class FoodMenuDeleteView(ManagerRequiredMixin, DeleteView):
    model = FoodMenu
    template_name = 'app_admin/foodmenu_delete.html'
    success_url = reverse_lazy('app_admin:foodmenu_list')


class HistoryListView(ManagerRequiredMixin, ListView):
    model = MenuHeadlines
    template_name = 'app_admin/history_list.html'

    def get_context_data(self, **kwargs):
        context = super(HistoryListView, self).get_context_data(**kwargs)
        context['unique_dates'] = MenuHeadlines.objects.all()
        return context


class SearchResultsListView(ManagerRequiredMixin, ListView):
    # Kuidas otsida ja ümber suunata https://stackoverflow.com/questions/62094267/redirect-if-query-has-no-result
    model = FoodItem
    template_name = 'app_admin/history_search.html'
    allow_empty = False

    def get_queryset(self):
        query = self.request.GET.get('q')  # info from form
        object_list = None
        #  queri on formi pealt saadud väärtus
        # https: // labpys.com / how - to - implement - join - operations - in -django - orm /
        if len(query) > 2:
            object_list = FoodItem.objects.select_related('menu').filter(food__icontains=query)

        return object_list

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(SearchResultsListView, self).dispatch(request, *args, **kwargs)
        except Http404:
            return redirect('app_admin:history')


class OldMenuListView(ManagerRequiredMixin, ListView):
    model = MenuHeadlines
    template_name = 'app_admin/history_menu.html'

    def get_context_data(self, **kwargs):
        all_data = None
        query = self.request.GET.get('date')
        # Listi vaade lisa argument
        # https://stackoverflow.com/questions/71023649/listview-with-an-extra-argument
        if not query:
            query = self.kwargs['date']

        # teeme kuupäeva sobivaks
        # date_object = datetime.strptime(query, '%d.%m.%Y').date()
        # date_object = datetime.strptime(query, '%d.%m.%Y').date()
        # today_string = date_object.strftime('%Y-%m-%d')
        parts = query.split('.')
        today_string = parts[2] + '-' + parts[1] + '-' + parts[0]
        # estonian_date = datetime.strptime(today_string, '%Y-%m-%d').strftime('%d.%m.%Y')
        estonian_date = query

        try:
            # https://stackoverflow.com/questions/1542878/what-to-do-when-django-query-returns-none-it-gives-me-error
            # Kui tekib error
            today_menu_id = MenuHeadlines.objects.get(date=today_string)  # vastuseks üks kirje või error
            today_menuheadlines = MenuHeadlines.objects.filter(Q(date=today_string)).values('date', 'teema', 'soovitab',
                                                                                            'valmistas')
            today_all_categories = FoodMenu.objects.filter(date_id=today_menu_id)

            # https://stackoverflow.com/questions/3397170/
            all_data = (FoodItem.objects.filter(Q(menu_id__in=today_all_categories))
                        .values('menu_id', 'food', 'full_price', 'half_price', 'show_in_menu',
                                'menu__category__name', 'id', 'menu__category__number')
                        .annotate(dcount=Count('menu_id')).order_by('menu__category__number', 'id'))
            # print(today_all_categories)
        except MenuHeadlines.DoesNotExist:
            today_menuheadlines = None

        context = {
            'object_list': all_data,
            'menuheadlines': today_menuheadlines,
            'estonian_date': estonian_date,
            'today_string': today_string

        }

        return context