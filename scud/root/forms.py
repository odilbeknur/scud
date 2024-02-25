from dataclasses import fields
from django import forms
from home.models import Category, Model, Plant, Responsible
from django.core.exceptions import ValidationError

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
        labels = {
            'name': 'Категория',
            'image': 'Категория (фото)',
        }

class ResponsibleCreateForm(forms.ModelForm):
    class Meta:
        model = Responsible
        fields = ['fullname', 'description']
        labels = {
            'fullname': 'Ф.И.О. ответственного',
            'description': 'Коментарии',
        }

class ModelCreateForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['name', 'description', 'image']
        labels = {
            'name': 'Модель ',
            'image': 'Модель (фото) ',
            'description': 'Коментарии ',
        }

status_choices = (
        ('В сети', 'В сети'),
        ('Не в сети', 'Не в сети'),
        ('Не подключен', 'Не подключен'),
    )

class EquipmentCreateForm(forms.Form): 
    room_number = forms.ChoiceField(choices=((str(x), x) for x in range(150,540)), label='Xona raqami', widget=forms.Select(attrs={'class': "form-control"}))
    inventar_number = forms.IntegerField(required=True, label='Идентификационный номер', widget=forms.NumberInput(attrs={'class': "form-control"}))
    model_id = forms.ModelChoiceField(queryset=Model.objects.all(), label='Модель устройства', widget=forms.Select(attrs={'class': "form-control"}))
    responsible_id = forms.ModelChoiceField(queryset=Responsible.objects.all(), label='Ответственный', widget=forms.Select(attrs={'class': "form-control"}))
    processor = forms.CharField(max_length=70, label='Процессор', required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    memory = forms.CharField(max_length=70, label='Память', required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    mac_address = forms.CharField(max_length=50, label='MAC-адрес', required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    ip_address = forms.CharField(max_length=50, label='IP-адрес', required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    description = forms.CharField(label='Коментарии', widget=forms.Textarea(attrs={'class': "form-control"}))

    def clean_inventar_number(self):
        inventar_number = self.cleaned_data['inventar_number']
        qs = Plant.objects.filter(inventar_number=inventar_number)
        if qs:
            raise ValidationError('Устройство с таким идентификационным номером уже существует')
        return inventar_number

class ProductUpdateForm(forms.ModelForm):
    category_id = forms.ModelChoiceField( queryset=Category.objects.all(), label='Категория', widget=forms.Select(attrs={'class': "form-control"}))
    room_number = forms.ChoiceField(choices=((str(x), x) for x in range(150,540)), label='Объект', widget=forms.Select(attrs={'class': "form-control"}))
    model_id = forms.ModelChoiceField(queryset=Model.objects.all(), label='Модель устройства', widget=forms.Select(attrs={'class': "form-control"}))
    responsible_id = forms.ModelChoiceField(queryset=Responsible.objects.all(), label='Ответственный', widget=forms.Select(attrs={'class': "form-control"}))
    processor = forms.CharField(max_length=70, label='Процессор', required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    memory = forms.CharField(max_length=70, label='Память', required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    mac_address = forms.CharField(max_length=50, label='MAC-адрес', required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    ip_address = forms.CharField(max_length=50, label='IP-адрес', required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    description = forms.CharField(label='Коментарии', widget=forms.Textarea(attrs={'class': "form-control"}))
    status = forms.ChoiceField(choices=status_choices, widget=forms.Select(attrs={'class': "form-control"}))
    class Meta:
            model = Plant
            exclude = ('inventar_number', 'qr_code',)

class ProductDetailUpdateForm(forms.ModelForm):
    status_choices = (
        ('В сети', 'В сети'),
        ('Не в сети', 'Не в сети'),
        ('Не подключен', 'Не подключен'),
    )
    status = forms.ChoiceField(choices=status_choices, label='', widget=forms.Select(attrs={'class': "form-control"}))
    class Meta:
        model = Plant
        fields = ['status']