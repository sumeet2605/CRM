import random
from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from leads.models import Sale
from .forms import SaleModelForm
from agents.mixin import OraganiserAndLoginRequiredMixin

# Create your views here.
class SaleListView(LoginRequiredMixin, generic.ListView):
    template_name = "sales/sale_list.html"
    
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Sale.objects.filter(
                oraganisation=user.userprofile,
                agent__isnull=False
            )
        else:
            queryset = Sale.objects.filter(
                oraganisation=user.agent.oraganisation, 
                agent__isnull=False
            )
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SaleListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
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
        if user.is_organiser:
            queryset = Sale.objects.filter(oraganisation=user.userprofile)
        else:
            queryset = Sale.objects.filter(oraganisation=user.agent.oraganisation)
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset


class SaleUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "sales/sale_update.html"
    form_class = SaleModelForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
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
