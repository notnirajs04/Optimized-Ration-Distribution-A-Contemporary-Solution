# Generated by Django 3.1.1 on 2020-10-07 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0007_payment_tb'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_tb',
            name='purchase_id',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='Customer.purchase_request_tb'),
        ),
    ]
