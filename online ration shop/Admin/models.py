from django.db import models
from Customer.models import *

# Create your models here.

class admin_tb(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

class admin_stock_tb(models.Model):
    product=models.CharField(max_length=20)
    stock=models.DecimalField(max_digits=8,decimal_places=2)
    yellow_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    pink_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    blue_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    white_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)

class card_category_tb(models.Model):
    category=models.CharField(max_length=20)


class district_tb(models.Model):
    district_name=models.CharField(max_length=20)

class ration_shop_tb(models.Model):
    shop_number=models.CharField(max_length=20)
    district_id=models.ForeignKey(district_tb,on_delete=models.CASCADE,default='1')
    area=models.CharField(max_length=30)
    address=models.CharField(max_length=100,default='no address')
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

class stock_allot_tb(models.Model):
    shop_id=models.ForeignKey(ration_shop_tb,on_delete=models.CASCADE,default='1')
    date=models.CharField(max_length=20,default='no date')
    month=models.CharField(max_length=20,default='no month')
    year=models.CharField(max_length=20,default='no year')
    status=models.CharField(max_length=20,default='allotted')

class allotted_product_tb(models.Model):
    allot_id=models.ForeignKey(stock_allot_tb,on_delete=models.CASCADE,null=True)
    product_id=models.ForeignKey(admin_stock_tb,on_delete=models.CASCADE)
    stock=models.DecimalField(max_digits=8,decimal_places=2)

class reply_tb(models.Model):
    complaint_id=models.ForeignKey(complaint_tb,on_delete=models.CASCADE)
    customer_id=models.ForeignKey(customer_tb,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    reply=models.CharField(max_length=500)
    date=models.CharField(max_length=20)
    status=models.CharField(max_length=20,default='unread')
