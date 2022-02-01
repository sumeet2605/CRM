import imp
from django.urls import path
from .views import DocumentListView, Card2CardCreateView, SalariedCreateView
from sales.views import SaleDetailView

app_name = "docs"

urlpatterns = [
    path('', SaleDetailView.as_view(), name='docs-list'),
    path('<int:pk>/', DocumentListView.as_view(), name='doc-detail'),
    path('<int:pk>/card2card', Card2CardCreateView.as_view(), name='card2card-create'),
    path('<int:pk>/salaried', SalariedCreateView.as_view(), name='salaried-create') 
    # path('<int:pk>/update/', SaleUpdateView.as_view(), name='sale-update'),  
    # path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    # path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    # path('<int:pk>/category/', SaleCategoryUpdateView.as_view(), name='lead-category-update'),
    # path('categories/', SaleCategoryListView.as_view(), name='category-list'),
    # path('categories/<int:pk>/', SaleCategoryDetailView.as_view(), name='category-detail'),
    # path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    # path('categories/<int:pk>/delete/', SaleCategoryDeleteView.as_view(), name='category-delete'),
    # path('create-category/', SaleCategoryCreateView.as_view(), name='category-create'),
    # path('<int:pk>/documents/', DocumentCreateView.as_view(),name='documents-update'),
    # path('<int:pk>/documents/card2card', Card2CardCreateView.as_view(), name='card2card-create'),
    # path('<int:pk>/documents/salaried', SalariedCreateView.as_view(), name='salaried-create') 
]