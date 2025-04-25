from django.db import models
from Admin.models import *
from Ration_Shop.models import *

# Create your models here.

class customer_tb(models.Model):
    card_number=models.CharField(max_length=20)
    card_owner=models.CharField(max_length=30)
    owner_photo=models.FileField(max_length=30)
    house_number=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    district_id=models.ForeignKey('Admin.district_tb',on_delete=models.CASCADE)
    taluk=models.CharField(max_length=20,default='no taluk')
    ward_number=models.IntegerField(default=0)
    member_count=models.CharField(max_length=20)
    adults=models.IntegerField(default=0)
    child=models.IntegerField(default=0)
    units=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    shop_id=models.ForeignKey('Admin.ration_shop_tb',on_delete=models.CASCADE)
    card_category_id=models.ForeignKey('Admin.card_category_tb',on_delete=models.CASCADE)
    monthly_income=models.CharField(max_length=20)
    phone=models.CharField(max_length=20,default='none')
    aadhaar_number=models.CharField(max_length=20,default='none')
    username=models.CharField(max_length=20,default='none')
    password=models.CharField(max_length=20,default='none')
    status=models.CharField(max_length=20,default='pending')

class purchase_request_tb(models.Model):
    shop_id=models.ForeignKey('Admin.ration_shop_tb',on_delete=models.CASCADE)
    customer_id=models.ForeignKey(customer_tb,on_delete=models.CASCADE)
    year=models.CharField(max_length=20,default='no year')
    month=models.CharField(max_length=20)
    date=models.CharField(max_length=20)
    status=models.CharField(max_length=20,default='pending')

class members_tb(models.Model):
    name=models.CharField(max_length=30)
    relationship=models.CharField(max_length=20)
    dob=models.CharField(max_length=20)
    job=models.CharField(max_length=20)
    income=models.CharField(max_length=20)
    customer_id=models.ForeignKey(customer_tb,on_delete=models.CASCADE,default='1')

class complaint_tb(models.Model):
    customer_id=models.ForeignKey(customer_tb,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    complaint=models.CharField(max_length=500)
    date=models.CharField(max_length=20)

class bank_tb(models.Model):
    name=models.CharField(max_length=30)
    credit_card_number=models.CharField(max_length=20)
    cvv=models.CharField(max_length=20)
    balance=models.CharField(max_length=20)

class payment_tb(models.Model):
    allocation_id=models.ForeignKey(product_allot_tb,on_delete=models.CASCADE)
    amount=models.CharField(max_length=20)
    transaction_key=models.CharField(max_length=20)
    date=models.CharField(max_length=20,default='no date')
    customer_id=models.ForeignKey(customer_tb,on_delete=models.CASCADE)
    shop_id=models.ForeignKey('Admin.ration_shop_tb',on_delete=models.CASCADE)
    purchase_id=models.ForeignKey(purchase_request_tb,on_delete=models.CASCADE,default='1')
    
