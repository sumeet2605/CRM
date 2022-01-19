# Generated by Django 4.0 on 2022-01-16 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0037_user_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='Status',
        ),
        migrations.AddField(
            model_name='sale',
            name='Status',
            field=models.CharField(blank=True, choices=[('Sent to Bank', 'Sent to Bank'), ('In Progress Backend', 'In Progress Backend'), ('Login Completed', 'Login Completed'), ('Bank Return', 'Bank Return'), ('In Progress Bank', 'In Progress Bank'), ('Pending', 'Pending'), ('Documentation', 'Documentation'), ('Card Out', 'Card Out'), ('Declined', 'Declined')], default='Documentation', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='organisation',
            field=models.CharField(blank=True, choices=[('Lead', 'Lead'), ('Sale', 'Sale')], max_length=20, null=True),
        ),
    ]
