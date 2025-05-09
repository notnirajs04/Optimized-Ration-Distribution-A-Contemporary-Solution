# Generated by Django 3.1.1 on 2020-10-07 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ration_Shop', '0007_auto_20201003_1825'),
        ('Admin', '0005_ration_shop_tb_address'),
        ('Customer', '0006_bank_tb'),
    ]

    operations = [
        migrations.CreateModel(
            name='payment_tb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=20)),
                ('transaction_key', models.CharField(max_length=20)),
                ('date', models.CharField(default='no date', max_length=20)),
                ('allocation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ration_Shop.product_allot_tb')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.customer_tb')),
                ('shop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.ration_shop_tb')),
            ],
        ),
    ]
