from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView) # vaated mida kasutame

from app_admin.forms import MenuHeadlinesCreateForm, ToiduNimedCreateForm, CategoryCreateForm
from app_admin.models import Category, MenuHeadlines, ToiduNimed
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class WriterRequiredMixin(UserPassesTestMixin):
    """ Test: user in group writer create and update """
    def test_func(self):
        return self.request.user.groups.filter(name='Writer').exists()


class EditorRequiredMixin(UserPassesTestMixin):
    """ Test: delete view """

    def __init__(self):
        self.request = None

    def test_func(self):
        return self.request.user.groups.filter(name='Editor').exists()


class HomeView(TemplateView):
    template_name = 'app_admin/index.html'


class CategoryCreateView(CreateView):
    template_name = 'app_admin/category_form_create.html'
    model = Category
    success_url = reverse_lazy('app_admin:category_list')
    form_class = Category


class CategoryUpdateView(UpdateView):
    template_name = 'app_admin/category_update.html'
    model = Category
    fields = ['number', 'name']  # update only this fields
    success_url = reverse_lazy('app_admin:category_list')


class CategoryDeleteView(DeleteView):
    template_name = 'app_admin/category_delete.html'
    model = Category
    success_url = reverse_lazy('app_admin:category_list')


class MenuHeadlinesView(WriterRequiredMixin, CreateView):
    model = MenuHeadlines
    form_class = MenuHeadlinesCreateForm
    success_url = reverse_lazy('app_public:index')


class ToiduNimedCreateView(CreateView):
    template_name = 'app_admin/toiduNimed_create.html'
    model = ToiduNimed
    success_url = reverse_lazy('app_admin:category_list')
    form_class = ToiduNimedCreateForm

class ToiduNimedListView(ListView):
    template_name = 'app_admin/toiduNimed_list.html'
    model = ToiduNimed
    #queryset = ToiduNimed.objects.order_by('food_name')  # Result ordered by name
    context_object_name = 'toiduNimed'  # default object_list now teacher


class ToiduNimedDeleteView(DeleteView):
    template_name = 'app_admin/toiduNimed_delete.html'
    model = ToiduNimed
    success_url = reverse_lazy('app_admin:toiduNimed_list')


class ToiduNimedUpdateView(UpdateView):
    template_name = 'app_admin/toiduNimed_update.html'
    model = ToiduNimed
    fields = ['date', 'category_ID', 'food_name', 'full_price', 'half_price', 'show_menu']  # update only this fields
    success_url = reverse_lazy('app_admin:toiduNimed_list')


class MenuHeadlinesListView(ListView):
    template_name = 'app_admin/menuHeadlines_list.html'
    model = MenuHeadlines
    #queryset = MenuHeadlines.objects.order_by('-date')  # Result ordered by kuupäev
    #queryset = MenuHeadlines.objects.all()  # Result ordered mis on juba modeliga sorteeritud ja sellepärast pole meil nedi ridu vaja

    context_object_name = 'menuHeadlines'  # see tuleb viewst


class MenuHeadlinesUpdateView(UpdateView):
    template_name = 'app_admin/menuHeadlines_update.html'
    model = MenuHeadlines
    fields = ['date', 'teema', 'soovitab', 'valmistas',]  # update only this fields
    success_url = reverse_lazy('app_admin:menuHeadlines_list')


class MenuHeadlinesDeleteView(DeleteView):
    template_name = 'app_admin/menuHeadlines_delete.html'
    model = MenuHeadlines
    success_url = reverse_lazy('app_admin:menuHeadlines_list')


class MenuHeadlinesCreateView(CreateView):
    template_name = 'app_admin/menuHeadlines_create.html'
    model = MenuHeadlines
    #fields = '__all__'  # All fields into form
    success_url = reverse_lazy('app_admin:menuHeadlines_list')
    form_class = MenuHeadlinesCreateForm


