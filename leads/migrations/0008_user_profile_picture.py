# Generated by Django 4.0 on 2022-02-04 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0007_alter_lead_bank_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
