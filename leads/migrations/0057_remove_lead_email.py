# Generated by Django 4.0 on 2022-01-26 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0056_lead_email_alter_lead_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='Email',
        ),
    ]
