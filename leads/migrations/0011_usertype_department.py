# Generated by Django 4.0 on 2022-01-02 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0010_usertype_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertype',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='UserType', to='leads.department'),
        ),
    ]
