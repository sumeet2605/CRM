from django import forms
from django.forms import ClearableFileInput
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, Agent, Category, FollowUp, Sale, Documents

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model= User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'Source',
            'Product',
            'Phone_Number',
            'Call_Status',
            'First_Name',
            'Last_Name',
            'Bank_Name',
            'Remarks',
        )



class DocumentsModelForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields =[
            'Photo',
            'PAN_Card_Photo',
            'KYC_Documents',
            'Card_Copy',
            'Card_Statement',
            'Salary_Slips',
            'Company_ID',
            'Bank_Statement'
        ]
        widgets = {
            'KYC_Documents' : ClearableFileInput(attrs={'multiple': True}),
            'Card_Statement' : ClearableFileInput(attrs={'multiple': True}),
            'Salary_Slips' : ClearableFileInput(attrs={'multiple': True}),
            'Bank_Statement' : ClearableFileInput(attrs={'multiple': True}),
            }
    
class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(oraganisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
            'organisation'
        )


class FollowUpModelForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = (
            'notes',
            'follow_up_date',

        )