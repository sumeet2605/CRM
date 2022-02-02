# Generated by Django 4.0 on 2022-02-02 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0006_remove_sale_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='Bank_Name',
            field=models.CharField(blank=True, choices=[('HDFC', 'HDFC BANK'), ('Kotak', 'Kotak Bank'), ('SBI', 'SBI Bank'), ('Yes', 'Yes Bank'), ('CITI', 'CITI Bank'), ('TATA', 'Tata Capital'), ('IndusInd', 'IndusInd Bank')], max_length=20, null=True),
        ),
    ]
