import random
from django.shortcuts import render, reverse
from django.db.models import Q
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from leads.models import (
    Sale, 
    Category, 
    SaleCategory, 
    Document, 
    KYCDocument, 
    SalarySlip, 
    BankStatement, 
    C2CDocument,
)
from .forms import (
    SaleModelForm, 
    SaleCategoryModelForm, 
    SaleCategoryUpdateForm, 
    DocumentCreateForm, 
    Card2CardForm, 
    SalariedForm,
    )
from agents.mixin import OraganiserAndLoginRequiredMixin


# Create your views here.
class SaleListView(LoginRequiredMixin, generic.ListView):
    template_name = "sales/sale_list.html"
    
    context_object_name = "sales"

    def get_queryset(self):
        user = self.request.user
        queryset = Sale.objects.all()
        
        if user.is_admin:
            queryset = queryset
        elif user.is_organiser:
            queryset = queryset.filter(
                oraganisation=user.userprofile,
                agent__isnull=False
            )
        else:
            queryset = queryset.filter(
                agent__user=user,
                agent__isnull=False
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SaleListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_admin:
            queryset = Sale.objects.filter(agent__isnull=True)
        elif user.is_organiser:
            queryset = Sale.objects.filter(
                
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
        queryset = Sale.objects.all()
        if user.is_admin:
            queryset = queryset
        elif user.is_organiser:
            queryset = queryset.filter(oraganisation=user.userprofile)
        else:
            
            queryset = queryset.filter(agent__user=user)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SaleDetailView, self).get_context_data(**kwargs)
        
        queryset = Document.objects.filter(sale=self.kwargs["pk"])
        doc = {}
        card ={}
        for d in queryset:
            doc  = KYCDocument.objects.filter(document=d)
            
        for c2c in queryset:
            card = C2CDocument.objects.filter(document=c2c)

        context.update({
            "document": queryset,
            "doc": doc,
            "card": card
        })
        return context


class SaleUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "sales/sale_update.html"
    form_class = SaleModelForm
    
    def get_queryset(self):
        queryset = Sale.objects.all()
        user = self.request.user
        if user.is_admin:
            queryset = queryset
        elif user.is_organiser:
            queryset = queryset.filter(oraganisation=user.userprofile)
        else:
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse("sales:sale-list")

    def form_valid(self, form):
        sale = form.save(commit=False)
        sale.updated_by = Agent.objects.get(user_id=self.request.user)
        sale.save()
        messages.info(self.request, "You have successfully updated this Sale")
        return super(SaleUpdateView, self).form_valid(form)


class SaleCategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "sales/category_list.html"
    context_object_name = "category_list"

    def get_queryset(self):
        queryset = SaleCategory.objects.all()
                
        return queryset

    def get_context_data(self, **kwargs):
        
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
        
        context_category= {}
        
        for c in categories:
            context_category[c] = queryset.filter(category=c).count()
        
        
        # print(queryset.filter([Q(category=category) for category in categories]))
        
        context.update({
                "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
                "context_category": context_category
                              
        })
        return context

    


class SaleCategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "sales/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        queryset = SaleCategory.objects.all()
       
        return queryset


class SaleCategoryCreateView(OraganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "sales/category_create.html"
    form_class = SaleCategoryModelForm

    def get_success_url(self):
        return reverse("sales:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.save()
        return super(SaleCategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OraganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "sales/category_update.html"
    form_class = SaleCategoryModelForm

    def get_success_url(self):
        return reverse("sales:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        queryset = SaleCategory.objects.all()
        return queryset


class SaleCategoryDeleteView(OraganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "sales/category_delete.html"

    def get_success_url(self):
        return reverse("sales:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        queryset = SaleCategory.objects.all()
        
        return queryset


class SaleCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "sales/lead_category_update.html"
    form_class = SaleCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_admin:
            queryset = Sale.objects.all()
        elif user.is_organiser:
            queryset = Sale.objects.filter(organisation=user.userprofile)
        else:
            queryset = Sale.objects.all()
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("sales:sale-detail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        lead_before_update = self.get_object()
        instance = form.save(commit=False)
        converted_category = SaleCategory.objects.get(name="Logged in")
        if form.cleaned_data["category"] == converted_category:
            # update the date at which this lead was converted
            if lead_before_update.category != converted_category:
                # this lead has now been converted
                instance.converted_date = datetime.datetime.now()
        instance.save()
        return super(SaleCategoryUpdateView, self).form_valid(form)


class DocumentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "sales/document_create.html"
    form_class = DocumentCreateForm

    
    def get_success_url(self):
        return reverse("sales:sale-list")

    def get_context_data(self, **kwargs):
        context = super(DocumentCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Sale.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        sale = Sale.objects.get(pk=self.kwargs["pk"])
        documents = form.save(commit=False)
        documents.sale = sale
        files = self.request.FILES.getlist('kyc_documents')
        documents.save()
        doc = Document.objects.get(sale=sale)
        if self.request.FILES:
            for f in files:
               KYCDocument.objects.create(document=doc, kyc_document=f)
            
        return super(DocumentCreateView, self).form_valid(form)

class Card2CardCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "sales/document_create.html"
    form_class = Card2CardForm  

    def get_success_url(self):
        return reverse("sales:sale-list")

    def get_context_data(self, **kwargs):
        context = super(Card2CardCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Sale.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        sale = Sale.objects.get(pk=self.kwargs["pk"])
        documents = form.save(commit=False)
        doc = Document.objects.get(sale=sale)
        documents.document = doc
        documents.save()       
            
        return super(Card2CardCreateView, self).form_valid(form)


class SalariedCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "sales/document_create.html"
    form_class = SalariedForm  

    def get_success_url(self):
        return reverse("sales:sale-list")

    def get_context_data(self, **kwargs):
        context = super(Card2CardCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Sale.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        
        sale = Sale.objects.get(pk=self.kwargs["pk"])
        documents = form.save(commit=False)
        doc = Document.objects.get(sale=sale)
        documents.sale = sale
        files = self.request.FILES.getlist('salary_slips')
        files1 = self.request.FILES.getlist('bank_statements')
        documents.save()
        doc = Document.objects.get(sale=sale)
        if self.request.FILES:
            for f in files:
               SalarySlip.objects.create(document=doc, salary_slip=f)

            for f in files1:
                BankStatement.objects.create(document=doc, bank_statement=f)
            
        return super(SalariedCreateView, self).form_valid(form)