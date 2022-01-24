from django.urls import path
from .views import (
    SaleDetailView, 
    SaleListView, 
    SaleUpdateView, 
    SaleCategoryListView, 
    SaleCategoryDetailView, 
    SaleCategoryCreateView, 
    SaleCategoryUpdateView, 
    CategoryUpdateView, 
    SaleCategoryDeleteView,
    DocumentCreateView,
    
)

app_name = "sales"

urlpatterns = [
    path('', SaleListView.as_view(), name='sale-list'),
    path('<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
    path('<int:pk>/update/', SaleUpdateView.as_view(), name='sale-update'),  
    # path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    # path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/category/', SaleCategoryUpdateView.as_view(), name='lead-category-update'),
    path('categories/', SaleCategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', SaleCategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', SaleCategoryDeleteView.as_view(), name='category-delete'),
    path('create-category/', SaleCategoryCreateView.as_view(), name='category-create'),
    path('<int:pk>/documents/', DocumentCreateView.as_view(),name='documents-update') 
]