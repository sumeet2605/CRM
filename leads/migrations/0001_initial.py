# Generated by Django 4.0 on 2021-12-29 18:03

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='leads.user')),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Source', models.CharField(choices=[('Telecalling', 'Telecalling'), ('Field', 'Field'), ('Digital', 'Digital'), ('Reference', 'Reference')], max_length=15)),
                ('Product', models.CharField(choices=[('Credit Card', 'Credit Card'), ('Insuarance', 'Insuarance'), ('Personal Loan', 'Personal Loan'), ('Over Draft', 'Over Draft')], max_length=20)),
                ('Phone_Number', models.CharField(blank=True, max_length=10, null=True)),
                ('Call_Status', models.CharField(blank=True, choices=[('Ringing', 'Ringing'), ('Switched Off', 'Switched Off'), ('Connected and Interested', 'Connected and Interested'), ('Connected and Not Interested', 'Connected and Not Interested'), ('Hung Up', 'Hung Up')], max_length=30, null=True)),
                ('First_Name', models.CharField(blank=True, max_length=20, null=True)),
                ('Last_Name', models.CharField(blank=True, max_length=20, null=True)),
                ('Fater_Name', models.CharField(blank=True, max_length=40, null=True)),
                ('Mother_Name', models.CharField(blank=True, max_length=40, null=True)),
                ('Date_of_Birth', models.DateField(blank=True, null=True)),
                ('Follow_up', models.BooleanField(blank=True, default=False)),
                ('Follow_up_Date_Time', models.DateTimeField(blank=True, null=True)),
                ('PAN_Number', models.CharField(blank=True, max_length=10, null=True)),
                ('Company_Name', models.CharField(blank=True, max_length=30, null=True)),
                ('Designation', models.CharField(blank=True, max_length=20, null=True)),
                ('Office_Address', models.CharField(blank=True, max_length=500, null=True)),
                ('Current_Residence_Address', models.CharField(blank=True, max_length=500, null=True)),
                ('Permanent_Residence_Address', models.CharField(blank=True, max_length=500, null=True)),
                ('Personal_Email', models.EmailField(blank=True, max_length=254, null=True)),
                ('Alternate_Phone_Number', models.IntegerField(blank=True, null=True)),
                ('Official_Email', models.EmailField(blank=True, max_length=254, null=True)),
                ('Bank_Name', models.CharField(blank=True, choices=[('HDFC', 'HDFC BANK'), ('Kotak', 'Kotak Bank'), ('SBI', 'SBI Bank'), ('Yes', 'Yes Bank'), ('CITI', 'CITI Bank'), ('TATA', 'Tata Capital')], max_length=20, null=True)),
                ('Photo', models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m')),
                ('Application_Type', models.CharField(blank=True, choices=[('C2C', 'Card 2 Card'), ('Salary', 'Salaried'), ('ITR', 'ITR')], max_length=30, null=True)),
                ('PAN_Card_Photo', models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m')),
                ('KYC_Documents', models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m')),
                ('Card_Number', models.BigIntegerField(blank=True, null=True)),
                ('Card_Copy', models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m')),
                ('Card_Statement', models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m')),
                ('Salary_Slips', models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m')),
                ('Company_ID', models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m')),
                ('Bank_Statement', models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m')),
                ('Status', models.CharField(blank=True, choices=[('Lead', 'Lead'), ('Sale', 'Sale'), ('Sent to Bank', 'Sent to Bank'), ('In Progress Backend', 'In Progress Backend'), ('Login Completed', 'Login Completed'), ('Bank Return', 'Bank Return'), ('In Progress Bank', 'In Progress Bank'), ('Pending', 'Pending'), ('Documentation', 'Documentation'), ('Card Out', 'Card Out'), ('Declined', 'Declined')], max_length=40, null=True)),
                ('Remarks', models.CharField(blank=True, max_length=40, null=True)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('Last_Upated', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.agent')),
            ],
        ),
        migrations.AddField(
            model_name='agent',
            name='oraganisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
        ),
        migrations.AddField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='leads.user'),
        ),
    ]
