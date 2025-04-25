from django.db import models
from Admin.models import *
from Customer.models import *
# Create your models here.

class time_tb(models.Model):
    shop_id=models.ForeignKey('Admin.ration_shop_tb',on_delete=models.CASCADE)
    opening_time=models.CharField(max_length=20)
    closing_time=models.CharField(max_length=20)
    date=models.CharField(max_length=20,default='no date')

class shop_stock_tb(models.Model):
    shop_id=models.ForeignKey('Admin.ration_shop_tb',on_delete=models.CASCADE,default=1)
    product_id=models.ForeignKey('Admin.admin_stock_tb',on_delete=models.CASCADE,default=1)
    stock=models.DecimalField(max_digits=8,decimal_places=2,default=0)

class product_allot_tb(models.Model):
    purchase_id=models.ForeignKey('Customer.purchase_request_tb',on_delete=models.CASCADE)
    shop_id=models.ForeignKey('Admin.ration_shop_tb',on_delete=models.CASCADE)
    customer_id=models.ForeignKey('Customer.customer_tb',on_delete=models.CASCADE)
    date_of_allocation=models.CharField(max_length=20)
    date_for_collecting=models.CharField(max_length=20)
    time_for_collecting=models.CharField(max_length=20)
    total_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)

class allocation_tb(models.Model):
    allot_id=models.ForeignKey(product_allot_tb,on_delete=models.CASCADE)
    product_id=models.ForeignKey('Admin.admin_stock_tb',on_delete=models.CASCADE)
    stock=models.DecimalField(max_digits=8,decimal_places=2)
    price=models.DecimalField(max_digits=8,decimal_places=2,default=0)

class product_shortage_tb(models.Model):
    shop_id=models.ForeignKey('Admin.ration_shop_tb',on_delete=models.CASCADE)
    month=models.CharField(max_length=20)
    year=models.CharField(max_length=20)
    date=models.CharField(max_length=20)
    status=models.CharField(max_length=20)
    allocation_id=models.ForeignKey('Admin.stock_allot_tb',on_delete=models.CASCADE,null=True)

class product_required_tb(models.Model):
    shortage_id=models.ForeignKey(product_shortage_tb,on_delete=models.CASCADE)
    product_id=models.ForeignKey('Admin.admin_stock_tb',on_delete=models.CASCADE)
    stock=models.DecimalField(max_digits=8,decimal_places=2)

class notification_tb(models.Model):
    request_id=models.ForeignKey('Customer.purchase_request_tb',on_delete=models.CASCADE)
    customer_id=models.ForeignKey('Customer.customer_tb',on_delete=models.CASCADE,default=1)
    datetime=models.CharField(max_length=20,default='no date')
    status=models.CharField(max_length=20,default='unread')
    
