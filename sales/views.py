import random
from django.shortcuts import render, reverse
from django.db.models import Q
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from leads.models import Sale, Category, SaleCategory
from leads.forms import CategoryModelForm, LeadCategoryUpdateForm
from .forms import SaleModelForm
from agents.mixin import OraganiserAndLoginRequiredMixin

# Create your views here.
class SaleListView(LoginRequiredMixin, generic.ListView):
    template_name = "sales/sale_list.html"
    
    context_object_name = "sales"

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            queryset = Sale.objects.all()
        elif user.is_organiser:
            queryset = Sale.objects.filter(
                oraganisation=user.userprofile,
                agent__isnull=False
            )
        else:
            queryset = Sale.objects.filter(
                oagent__isnull=False
            )
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SaleListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_admin:
            queryset = Sale.objects.filter(agent__isnull=True)
        elif user.is_organiser:
            queryset = Sale.objects.filter(
                oraganisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                "unassigned_sales":queryset
            })
        return context

class SaleDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "sales/sale_detail.html"
    
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            queryset = Sale.objects.all()
        elif user.is_organiser:
            queryset = Sale.objects.filter(oraganisation=user.userprofile)
        else:
            queryset = Sale.objects.all()
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset


class SaleUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "sales/sale_update.html"
    form_class = SaleModelForm

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            queryset = Sale.objects.all()
        elif user.is_organiser:
            queryset = Sale.objects.filter(oraganisation=user.userprofile)
        else:
            queryset = Sale.objects.filter(oraganisation=user.agent.oraganisation)
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse("sales:sale-list")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this Sale")
        return super(SaleUpdateView, self).form_valid(form)


class SaleCategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "sales/category_list.html"
    context_object_name = "category_list"

    def get_queryset(self):
        queryset = SaleCategory.objects.all()
                
        return queryset

    def get_context_data(self, **kwargs):
        print(**kwargs)
        context = super(SaleCategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        categories = SaleCategory.objects.all()
             
        if user.is_admin:
            queryset = Sale.objects.all()
        elif user.is_organiser:
            queryset = Sale.objects.filter(
                oraganisation=user.userprofile
            )
        else:
            queryset = Sale.objects.filter(
                agent__user=user
            )
        
        print(type(queryset))
        context_category= {}
        
        for c in categories:
            context_category[c] = queryset.filter(category=c).count()
        
        print(type(context_category))
        # print(queryset.filter([Q(category=category) for category in categories]))
        
        context.update({
                "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
                "context_category": context_category
                              
        })
        return context

    


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_admin:
            queryset = Category.objects.all()
        elif user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.oraganisation
            )
        return queryset


class CategoryCreateView(OraganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OraganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_admin:
            queryset = Category.objects.all()
        elif user.is_organiser:
            queryset = Category.objects.filter(
                organisation="Lead"
            )
        else:
            queryset = Category.objects.filter(
                organisation="Lead"
            )
        return queryset


class CategoryDeleteView(OraganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_admin:
            queryset = Lead.objects.all()
        elif user.is_organiser:
            queryset = Category.objects.filter(
                organisation="Lead"
            )
        else:
            queryset = Category.objects.filter(
                organisation="Lead"
            )
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_admin:
            queryset = Lead.objects.all()
        elif user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.all()
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        lead_before_update = self.get_object()
        instance = form.save(commit=False)
        converted_category = Category.objects.get(name="Converted")
        if form.cleaned_data["category"] == converted_category:
            # update the date at which this lead was converted
            if lead_before_update.category != converted_category:
                # this lead has now been converted
                instance.converted_date = datetime.datetime.now()
        instance.save()
        return super(LeadCategoryUpdateView, self).form_valid(form)
