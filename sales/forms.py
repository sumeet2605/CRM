from django import forms
from leads.models import Sale

class SaleModelForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = (
            'First_Name',
            'Last_Name',
            'Fater_Name',
            'Mother_Name',
            'Date_of_Birth',
            'Phone_Number',
            'PAN_Number',
            'Company_Name',
            'Designation',
            'Office_Address',
            'Current_Residence_Address',
            'Permanent_Residence_Address',
            'Personal_Email',
            'Alternate_Phone_Number',
            'Official_Email',
            'Bank_Name',
            'Remarks',
            'category',
            'converted_date'
        )
