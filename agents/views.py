import random
from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from leads.models import Agent
from .forms import AgentModelForm
from .mixin import OraganiserAndLoginRequiredMixin
# Create your views here.

class AgentListView(OraganiserAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    context_object_name = "agents"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(oraganisation=organisation)

    
class AgentDetailView(OraganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    queryset = Agent.objects.all()
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(oraganisation=organisation)


class AgentCreateView(OraganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f"{random.randint(0, 10000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            oraganisation=self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an agent for Rizvitak Consulting India Pvt. Ltd.",
            message="You were added as an agent on RIZCRM, please login to start working.",
            from_email="admin@rizvitak.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("agents:agent-list")


class AgentUpdateView(OraganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(oraganisation=organisation)

    def get_success_url(self):
        return reverse("agents:agent-list")    

    def form_valid(self, form):
        form.save()
        return super(AgentUpdateView, self).form_valid(form)

    


class AgentDeleteView(OraganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    
    
    def get_success_url(self):
        return reverse("agnets:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(oraganisation=organisation)
