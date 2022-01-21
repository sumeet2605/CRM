# Generated by Django 4.0 on 2022-01-21 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0043_alter_followup_follow_up_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='Updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='update', to='leads.agent'),
        ),
        migrations.AddField(
            model_name='sale',
            name='Application_Number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='saleupdate', to='leads.agent'),
        ),
    ]