from django.urls import path
from .views import (
    SaleDetailView, SaleListView, SaleUpdateView
)

app_name = "sales"

urlpatterns = [
    path('', SaleListView.as_view(), name='sale-list'),
    path('<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
    path('<int:pk>/update/', SaleUpdateView.as_view(), name='sale-update'),  
    # path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    # path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    # path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    # path('<int:pk>/followups/create/', FollowUpCreateView.as_view(), name='lead-followup-create'),
    # path('followups/<int:pk>/', FollowUpUpdateView.as_view(), name='lead-followup-update'),
    # path('followups/<int:pk>/delete/', FollowUpDeleteView.as_view(), name='lead-followup-delete'),
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    # path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    # path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    # path('create-category/', CategoryCreateView.as_view(), name='category-create'), 
]