from multiprocessing.spawn import import_main_path
from django.urls import path
from .views import Admin_index, CategoryCreateView, baseview, EquipmentCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView, ResponsibleCreateView, ModelCreateView, SearchResultsView

urlpatterns = [
    path('admin-index/', Admin_index, name='admin-index'),
    path('admin-index/category-create', CategoryCreateView.as_view(), name='category-create'),  
    path('admin-index/poka-base/<int:pk>', baseview, name='base-view'),
    path('admin-index/poka-base/<int:pk>/add-equipment', EquipmentCreateView, name='equipment-create'),
    path('admin-index/poka-base/<int:pk>/admin-detail-of-product', ProductDetailView, name='product-detail'),
    path('admin-index/poka-base/<int:pk>/product-update', ProductUpdateView, name='product-update'),
    path('admin-index/poka-base/<int:pk>/product-delete', ProductDeleteView, name='product-delete'),
    path('admin-index/responsible-create', ResponsibleCreateView.as_view(), name='responsible-create'),
    path('admin-index/model-create', ModelCreateView.as_view(), name='model-create'),
    path('admin/search', SearchResultsView.as_view(), name='admin-search'),
]