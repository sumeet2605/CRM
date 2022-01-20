from datetime import date, datetime
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=30)  # Sales, Recruitment, HR, Admin

    def __str__(self):
        return self.name


class UserType(models.Model):
    name = models.CharField(max_length=30)
    department = models.ForeignKey("Department", related_name="UserType", null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name


 
class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    department = models.ForeignKey("Department", related_name="user", null=True, on_delete=models.SET_NULL)
    user_type = models.ForeignKey("UserType", null=True, on_delete=models.SET_NULL)
    user_role = models.CharField(max_length=20, null=True, choices=(
        ( 'E', 'Executive'),
        ('TL', 'Team Lead'),
        ('AM', 'Assistant Manager'),
        ('M', 'Manager'),
        ('HOD', 'Head Of Department'),
    ))
    manager = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)


class UserProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Agent(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    oraganisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"

class Lead(models.Model):
    SOURCE= (
        ('Telecalling', 'Telecalling'),
        ('Field', 'Field'),
        ('Digital', 'Digital'),
        ('Reference', 'Reference'),
    )
    PRODUCT = (
        ('Credit Card', 'Credit Card'),
        ('Insuarance', 'Insuarance'),
        ('Personal Loan', 'Personal Loan'),
        ('Over Draft', 'Over Draft'),  
    )
    CALLSTATUS = (
        ('Ringing', 'Ringing'),
        ('Switched Off', 'Switched Off'),
        ('Connected and Interested', 'Connected and Interested'),
        ('Connected and Not Interested', 'Connected and Not Interested'),
        ('Hung Up', 'Hung Up'),
    )

    BANKNAME = (
        ('HDFC', 'HDFC BANK'),('Kotak', 'Kotak Bank'),('SBI', 'SBI Bank'),('Yes', 'Yes Bank'),('CITI', 'CITI Bank'), ('TATA', 'Tata Capital'),
    )

    APPLICACTIONTYPE = (('C2C', 'Card 2 Card'),('Salary', 'Salaried'),('ITR', 'ITR'),)
    
    Source = models.CharField(max_length=15, choices=SOURCE)
    Product = models.CharField(max_length=20, choices=PRODUCT)
    First_Name = models.CharField(max_length=20, null=True, blank=True)
    Last_Name = models.CharField(max_length=20, null=True, blank=True)
    Phone_Number = models.CharField(max_length=10, null=True, blank=True, unique=True)
    Call_Status = models.CharField(max_length=30, choices=CALLSTATUS, null=True, blank=True)
    Bank_Name = models.CharField(max_length=20, null=True, choices=BANKNAME, blank=True)
    Application_Type = models.CharField(max_length=30, null=True, choices=APPLICACTIONTYPE, blank=True)
    Remarks = models.CharField(null = True, max_length = 40, blank=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Last_Upated = models.DateTimeField(auto_now=True)
    oraganisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey("Category", related_name="leads", null=True, on_delete=models.SET_NULL)
    converted_date = models.DateTimeField(null=True, blank=True)

    objects = LeadManager()
   

    def __str__(self):
        return f"{self.First_Name} {self.Last_Name}"

def handle_upload_follow_ups(instance, filename):
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"


class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, related_name="followups", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    follow_up_date = models.DateTimeField()

    def __str__(self):
        return f"{self.lead.first_name} {self.lead.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=30)  # New, Contacted, Converted, Unconverted
    
    def __str__(self):
        return self.name

class SaleCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Sale(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, null=True, blank=True)
    First_Name = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=20)
    Fater_Name = models.CharField(max_length=40, null=True)
    Mother_Name = models.CharField(max_length=40, null=True)
    Date_of_Birth = models.DateField(null=True)
    Phone_Number = models.CharField(max_length=10, unique=True)
    PAN_Number = models.CharField(max_length=10, null=True)
    Company_Name = models.CharField(max_length=30, null=True)
    Designation = models.CharField(max_length=20, null=True)
    Office_Address = models.CharField(max_length=500, null=True)
    Current_Residence_Address = models.CharField(max_length=500, null=True)
    Permanent_Residence_Address = models.CharField(max_length=500, null=True)
    Personal_Email = models.EmailField(null=True)
    Alternate_Phone_Number = models.CharField(max_length=10, null=True, blank=True)
    Official_Email = models.EmailField(null=True)
    Bank_Name = models.CharField(max_length=20)
    Remarks = models.CharField(max_length = 40, blank=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Last_Upated = models.DateTimeField(auto_now=True)
    oraganisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey("SaleCategory", related_name="sales", null=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/")
    converted_date = models.DateTimeField(null=True, blank=True)

    objects = LeadManager()
   

    def __str__(self):
        return f"{self.First_Name} {self.Last_Name}"

def handle_upload_documents(instance, filename):
    return f"sale_documents/sale_{instance.sale.pk}/{filename}"


class Documents(Sale):
    Photo = models.ImageField(upload_to='uploads/%Y/%m', null=True, blank=True)
    PAN_Card_Photo = models.FileField(upload_to='uploads/%Y/%m', null=True, blank=True)
    KYC_Documents = models.FileField(upload_to='uploads/%Y/%m', null=True, blank=True)
    Card_Copy = models.ImageField(null=True, upload_to='uploads/%Y/%m', blank=True)
    Card_Statement = models.FileField(upload_to='uploads/%Y/%m', null=True, blank=True)
    Salary_Slips = models.FileField(upload_to='uploads/%Y/%m', null=True, blank=True)
    Company_ID = models.FileField(upload_to='uploads/%Y/%m', null=True, blank=True)
    Bank_Statement = models.FileField(upload_to='uploads/%Y/%m', null=True, blank=True)
    

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    

def post_lead_created_signal(sender, instance, created, **kwargs):
    a = Category.objects.get(name="Converted")
    if instance.category==a:
        if Sale.objects.filter(lead=instance).exists():
            pass
        else:  
            Sale.objects.create(
                lead=instance,
                First_Name=instance.First_Name,
                Last_Name=instance.Last_Name,
                Phone_Number=instance.Phone_Number,
                Fater_Name="",
                Mother_Name="",
                Date_of_Birth=date.today(),
                PAN_Number="",
                Company_Name="",
                Designation="",
                Office_Address="",
                Current_Residence_Address="",
                Permanent_Residence_Address="",
                Personal_Email="",
                Alternate_Phone_Number="",
                Official_Email="",
                Bank_Name=instance.Bank_Name,
                Remarks="",
                oraganisation=instance.oraganisation,
                agent=instance.agent,
                category=Category.objects.get(id=1),
                description = "",
                converted_date=datetime.now(),
            )
            
        
    
        

post_save.connect(post_user_created_signal, sender=User)
post_save.connect(post_lead_created_signal, sender=Lead)