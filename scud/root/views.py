from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from home.models import Category, Model, Plant, Responsible
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CategoryCreateForm, EquipmentCreateForm, ProductUpdateForm, ResponsibleCreateForm, ModelCreateForm, ProductDetailUpdateForm
import random
from django.db.models import Count, Q

def Admin_index(request):
    categories = Category.objects.annotate(count=Count('category'))
    return render(request, 'admin/admin-index.html', {'queryset': categories})

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'admin/category-create.html'
    login_url = 'login'
    success_url = reverse_lazy('category-create')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ResponsibleCreateView(LoginRequiredMixin, CreateView):
    model = Responsible
    form_class = ResponsibleCreateForm
    template_name = 'admin/responsible-create.html'
    login_url = 'login'
    success_url = reverse_lazy('responsible-create')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ModelCreateView(LoginRequiredMixin, CreateView):
    model = Model
    form_class = ModelCreateForm
    template_name = 'admin/model-create.html'
    login_url = 'login'
    success_url = reverse_lazy('model-create')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def baseview(request, pk):
    query = Plant.objects.filter(category_id__id=pk)
    get_cat = Category.objects.filter(id=pk)
    return render(request, 'admin/admin-base.html', {'query': query, 'get_cat': get_cat})

def EquipmentCreateView(request, pk):
    category = Category.objects.get(id=pk)
    form = EquipmentCreateForm()
    if request.method == 'POST':
        form = EquipmentCreateForm(request.POST)
        if form.is_valid():
            # invent = Product.objects.last()
            # try:
            #     inte = int(invent.inventar_number) 
            #     integ = inte + 1
            # except:
            #     integ =  random.randint(1000000000000, 9999999999999999)
            #     uniqe_confirm = Product.objects.filter(inventar_number=integ)
            #     while uniqe_confirm:
            #         integ =  random.randint(1000000000000, 9999999999999999)
            #         if not Product.objects.filter(inventar_number=integ):
            #             break
            # print(type(form.cleaned_data['room_number']))
            equipment = Plant(
                category_id=category,
                room_number=form.cleaned_data['room_number'],
                inventar_number=form.cleaned_data['inventar_number'],
                model_id=form.cleaned_data['model_id'],
                responsible_id=form.cleaned_data['responsible_id'],
                processor=form.cleaned_data['processor'],
                memory=form.cleaned_data['memory'],
                mac_address=form.cleaned_data['mac_address'],
                ip_address=form.cleaned_data['ip_address'],
                description=form.cleaned_data['description'],
            )
            equipment.save()
            red = equipment.category_id.id
            return redirect('base-view', pk=red)
    return render(request, 'admin/equipment-create.html', {'form': form})


def ProductDetailView(request, pk):
    query = Plant.objects.filter(id=pk)
    eq = get_object_or_404(Plant, pk=pk)
    form = ProductDetailUpdateForm(request.POST or None, instance=eq)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('product-detail', pk=eq.pk)
    return render(request, 'admin/admin-detail.html', {'query': query, 'form': form})

def ProductUpdateView(request, pk):
    equipment = get_object_or_404(Plant, pk=pk)
    red = equipment.category_id.id
    form = ProductUpdateForm(request.POST or None, instance=equipment)
    if request.method=='POST' and form.is_valid():
        form.save()
        return redirect('base-view', pk=red)
    return render(request, 'admin/admin-product-update.html', {'form': form})
    
def ProductDeleteView(request, pk):
    query = Plant.objects.get(pk=pk)
    red = query.category_id.id
    if request:
        query.delete()
        return redirect('base-view', pk=red)
    return render(request, 'admin/admin-base.html')

class SearchResultsView(ListView):
    model = Model
    template_name = 'admin/admin-search-results.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        object_list = Plant.objects.filter(
            Q(inventar_number__icontains=query)
        )
        return object_list