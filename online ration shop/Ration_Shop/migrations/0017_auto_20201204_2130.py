# Generated by Django 3.1.1 on 2023-09-07 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0011_auto_20201125_0149'),
        ('Ration_Shop', '0016_product_shortage_tb_allocation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_shortage_tb',
            name='allocation_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Admin.stock_allot_tb'),
        ),
    ]
