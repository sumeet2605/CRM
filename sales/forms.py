from django import forms
from leads.models import (
    Sale, 
    SaleCategory, 
    Document, 
    C2CDocument,
)

class SaleModelForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = (
            'Application_Type',
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
        )
        widgets = {'Date_of_Birth': forms.widgets.DateInput(attrs={'type': 'date' })}

class SaleCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = (
            'category',
        )


class SaleCategoryModelForm(forms.ModelForm):
    class Meta:
        model = SaleCategory
        fields = [
            'name',
        ]


class DocumentCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kyc_documents'] = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
 
    class Meta:
        model = Document
        fields = [
            'photo',
            'pan_card',
        ]
        
            
class Card2CardForm(forms.ModelForm):
    
    class Meta:
        model = C2CDocument
        fields = [
            'card_copy',
            'card_statement',
        ]        


class SalariedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['salary_slips'] = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        self.fields['bank_statements'] = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    class Meta:
        model = Document
        fields = [
            'company_id',            
        ]