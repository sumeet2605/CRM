# Generated by Django 4.0 on 2022-01-27 09:51

from django.db import migrations, models
import django.db.models.deletion
import leads.models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_lead_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='bank_statement',
        ),
        migrations.RemoveField(
            model_name='document',
            name='kyc_documents',
        ),
        migrations.RemoveField(
            model_name='document',
            name='salary_slips',
        ),
        migrations.CreateModel(
            name='SalarySlip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_slip', models.FileField(blank=True, null=True, upload_to=leads.models.handle_upload_documents)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.document')),
            ],
        ),
        migrations.CreateModel(
            name='KYCDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kyc_document', models.FileField(blank=True, null=True, upload_to=leads.models.handle_upload_documents)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kyc', to='leads.document')),
            ],
        ),
        migrations.CreateModel(
            name='BankStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_statement', models.FileField(blank=True, null=True, upload_to=leads.models.handle_upload_documents)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.document')),
            ],
        ),
    ]
