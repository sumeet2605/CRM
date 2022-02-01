from django.shortcuts import render

# Create your views here.
import random
from django.shortcuts import render, reverse
from django.db.models import Q
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from leads.models import (
    Sale,
    Document, 
    KYCDocument, 
    SalarySlip, 
    BankStatement, 
    C2CDocument,
)
from sales.forms import (
     
    DocumentCreateForm, 
    Card2CardForm, 
    SalariedForm,
    )
from agents.mixin import OraganiserAndLoginRequiredMixin


# Create your views here.
class DocumentListView(LoginRequiredMixin, generic.DetailView):
    template_name = "docs/docs_list.html"
    
    context_object_name = "docs"

    def get_queryset(self):
        user = self.request.user
        queryset = Document.objects.filter(pk=self.kwargs["pk"])        
       
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DocumentListView, self).get_context_data(**kwargs)
        
        queryset = Document.objects.filter(pk=self.kwargs["pk"])
        doc = {}
        card ={}
        salary = {}
        bank = {}
        for d in queryset:
            doc  = KYCDocument.objects.filter(document=d)
            card = C2CDocument.objects.filter(document=d)
            salary = SalarySlip.objects.filter(document=d)
            bank = BankStatement.objects.filter(document=d)
        
        context.update({
            "doc": doc,
            "card": card,
            "salary": salary,
            "bank" : bank

        })
        return context


class Card2CardCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "docs/document_create.html"
    form_class = Card2CardForm  

    def get_success_url(self):
        return reverse("sales:sale-list")

    def form_valid(self, form):
        doc = Document.objects.get(pk=self.kwargs["pk"])
        documents = form.save(commit=False)
        documents.document = doc
        documents.save()                   
        return super(Card2CardCreateView, self).form_valid(form)


class SalariedCreateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "docs/document_create.html"
    form_class = SalariedForm  

    def get_success_url(self):
        return reverse("sales:sale-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        queryset = Document.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SalariedCreateView, self).get_context_data(**kwargs)
        context.update({
            "docs": Document.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        documents = form.save(commit=False)
        doc = Document.objects.get(pk=self.kwargs["pk"])
        files = self.request.FILES.getlist('salary_slips')
        files1 = self.request.FILES.getlist('bank_statements')
        documents.save()
        if self.request.FILES:
            for f in files:
               SalarySlip.objects.create(document=doc, salary_slip=f)

            for f in files1:
                BankStatement.objects.create(document=doc, bank_statement=f)
            
        return super(SalariedCreateView, self).form_valid(form)
