# Generated by Django 3.1.1 on 2020-10-03 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ration_Shop', '0004_product_allot_tb_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_allot_tb',
            name='aatta',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product_allot_tb',
            name='kerosene',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product_allot_tb',
            name='rava',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product_allot_tb',
            name='rice',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product_allot_tb',
            name='sugar',
            field=models.IntegerField(),
        ),
    ]
