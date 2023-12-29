import urllib.parse
from urllib.request import urlopen
import json

from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView, FormView)
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect

from .forms import *
from .models import *
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


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.order_by('number')
    context_object_name = 'categories'  # default object_list now teacher


class CategoryCreateView(CreateView):
    template_name = 'app_admin/category_form_create.html'
    model = Category
    success_url = reverse_lazy('app_admin:category_list')
    # form_class = Category
    fields = '__all__'


class CategoryUpdateView(UpdateView):
    template_name = 'app_admin/category_update.html'
    model = Category
    # fields = ['number', 'name']  # update only this fields
    success_url = reverse_lazy('app_admin:category_list')
    form_class = CategoryUpdateForm


class CategoryDeleteView(DeleteView):
    template_name = 'app_admin/category_delete.html'
    model = Category
    success_url = reverse_lazy('app_admin:category_list')



class MenuHeadlinesView(WriterRequiredMixin, CreateView):
    model = MenuHeadlines
    form_class = MenuHeadlinesCreateForm
    success_url = reverse_lazy('app_public:index')


class MenuHeadlinesListView(ListView):
    template_name = 'app_admin/menuHeadlines_list.html'
    model = MenuHeadlines
    #queryset = MenuHeadlines.objects.order_by('-date')  # Result ordered by kuupäev
    #queryset = MenuHeadlines.objects.all()  # Result ordered mis on juba modeliga sorteeritud ja sellepärast pole meil nedi ridu vaja

    context_object_name = 'menuHeadlines'  # see tuleb viewst


class MenuHeadlinesUpdateView(UpdateView):
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


class MenuHeadlinesDeleteView(DeleteView):
    template_name = 'app_admin/menuHeadlines_delete.html'
    model = MenuHeadlines
    success_url = reverse_lazy('app_admin:menuHeadlines_list')


class MenuHeadlinesCreateView(CreateView):
    template_name = 'app_admin/menuHeadlines_create.html'
    model = MenuHeadlines
    # fields = '__all__'  # All fields into form
    success_url = reverse_lazy('app_admin:menuHeadlines_list')
    form_class = MenuHeadlinesCreateForm


class FoodMenuListView(ListView):
    model = FoodMenu
    template_name = 'app_admin/foodmenu_list.html'


class FoodMenuUpdateView(SingleObjectMixin, FormView):
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


class FoodMenuDetailView(DetailView):
    model = FoodMenu
    template_name = 'app_admin/foodmenu_detail.html'


class FoodMenuDeleteView(DeleteView):
    model = FoodMenu
    template_name = 'app_admin/foodmenu_delete.html'
    success_url = reverse_lazy('app_admin:foodmenu_list')


class FoodMenuCreateView(CreateView):
    model = FoodMenu
    form_class = FoodMenuCreateForm
    template_name = 'app_admin/foodmenu_create.html'
    # fields = ['date', 'category', ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The author has been added'
        )

        return super().form_valid(form)
