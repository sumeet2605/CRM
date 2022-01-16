import logging
from django.utils import timezone
import datetime
from django import contrib
from django.contrib import messages
from django.core.mail import send_mail
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse 
from django.views import generic
from agents.mixin import OraganiserAndLoginRequiredMixin
from .models import Lead, Agent, Category, FollowUp, Sale, Documents
from .forms import (
    
    LeadModelForm,
    CustomUserCreationForm,
    AssignAgentForm,
    LeadCategoryUpdateForm,
    CategoryModelForm,
    FollowUpModelForm,
    DocumentsModelForm

) 

logger = logging.getLogger(__name__)

# CRUD+L - Create, Retrieve, Update and Delete + List

# Create your views here.

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

class DashboardView(OraganiserAndLoginRequiredMixin, generic.TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        user = self.request.user

        # How many leads we have in total
        total_lead_count = Lead.objects.filter(oraganisation=user.userprofile).count()

        # How many new leads in the last 30 days
        thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)

        total_in_past30 = Lead.objects.filter(
            oraganisation=user.userprofile,
            Created_at__gte=thirty_days_ago
        ).count()

        # How many converted leads in the last 30 days
        converted_category = Category.objects.get(name="Converted")
        converted_in_past30 = Lead.objects.filter(
            oraganisation=user.userprofile,
            category=converted_category,
            converted_date__gte=thirty_days_ago
        ).count()

        context.update({
            "total_lead_count": total_lead_count,
            "total_in_past30": total_in_past30,
            "converted_in_past30": converted_in_past30
        })
        return context


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        print(user.agent.oraganisation)
        if user.is_organiser:
            queryset = Lead.objects.filter(
                oraganisation=user.userprofile,
            )
        else:
            queryset = Lead.objects.filter(
                oraganisation=user.agent.oraganisation,
            )
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                oraganisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                "unassigned_leads":queryset
            })
        return context

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        perm = user.usertype
        if user.is_organiser:
            queryset = Lead.objects.filter(oraganisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(oraganisation=user.agent.oraganisation)
            queryset = queryset.filter(agent__user=user)
        return queryset

class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.agent = Agent.objects.get(user_id=self.request.user)
        lead.oraganisation = self.request.user.userprofile

        lead.save()
        messages.success(self.request, "You have successfully created a lead")
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(oraganisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(oraganisation=user.agent.oraganisation)
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(LeadUpdateView, self).form_valid(form)

class LeadDeleteView(OraganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(oraganisation=user.userprofile)
       
        return queryset
    
    def get_success_url(self):
        return reverse("leads:lead-list")

class AssignAgentView(OraganiserAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organiser:
            queryset = Lead.objects.filter(
                oraganisation=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                oraganisation=user.agent.oraganisation
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
            "assigned_lead_count": queryset.filter(category__isnull=False).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.oraganisation
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
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
        category.organisation = self.request.user.userprofile
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
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.oraganisation
            )
        return queryset


class CategoryDeleteView(OraganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.oraganisation
            )
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = Lead.objects.filter(oraganisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(oraganisation=user.agent.oraganisation)
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


class FollowUpCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Lead.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super(FollowUpCreateView, self).form_valid(form)


class FollowUpUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/followup_update.html"
    form_class = FollowUpModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = FollowUp.objects.filter(lead__oraganisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__oraganisation=user.agent.oraganisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().lead.id})


class FollowUpDeleteView(OraganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/followup_delete.html"

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("leads:lead-detail", kwargs={"pk": followup.lead.pk})

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organiser:
            queryset = FollowUp.objects.filter(lead__oraganisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__oraganisation=user.agent.oraganisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

class SaleListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/sale_list.html"
    
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
        context = super(LeadListView, self).get_context_data(**kwargs)
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
    template_name = "leads/sale_detail.html"
    
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
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Sale.objects.filter(oraganisation=user.userprofile)
        else:
            queryset = Sale.objects.filter(oraganisation=user.agent.oraganisation)
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse("leads:sale-list")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(LeadUpdateView, self).form_valid(form)


class LeadJsonView(generic.View):

    def get(self, request, *args, **kwargs):
        
        qs = list(Lead.objects.all().values(
            "first_name", 
            "last_name", 
            "age")
        )

        return JsonResponse({
            "qs": qs,
        })