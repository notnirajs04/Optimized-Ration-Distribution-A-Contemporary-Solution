from django.shortcuts import render,redirect
from Admin.models import *
from Ration_Shop.models import *
import datetime
from Customer.models import *
import random
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth.models import auth,User
from django.contrib.auth.decorators import login_required
# Create your views here.

def signupCustomer(request):
    districts=district_tb.objects.all()
    card=card_category_tb.objects.all()
    return render(request,'signup_customer.html',{'districts':districts,'card':card})

def signupCustomerAction(request):
    d_id=district_tb.objects.get(id=request.POST['district'])
    rshop_id=ration_shop_tb.objects.get(id=request.POST['shop'])
    card_category=card_category_tb.objects.get(id=request.POST['category'])
    pic=""
    
    if(len(request.FILES)>0):
        pic=request.FILES['fileupload']
    else:
        pic="no pic"

    
    
    customer=customer_tb(card_number=request.POST['card_no'],card_owner=request.POST['owner_name'],owner_photo=pic,house_number=request.POST['house_no'],
                            address=request.POST['address'],district_id=d_id,taluk=request.POST['taluk'],ward_number=request.POST['ward_no'],
                            member_count=request.POST['m_count'],adults=request.POST['adults'],child=request.POST['children'],units=request.POST['units'],
                            shop_id=rshop_id,card_category_id=card_category,monthly_income=request.POST['income'],phone=request.POST['phone'],
                            aadhaar_number=request.POST['a_number'],username=request.POST['username'],password=request.POST['password'],status='pending')
    customer.save()
    user=User.objects.create_user(username=request.POST['username'],password=request.POST['password'])
    user.save()
    messages.add_message(request,messages.INFO,"Signup successful")
    return redirect('signupCustomer')

@login_required
def viewStockOnShop(request):
    districts=district_tb.objects.all()
    return render(request,'view_stock_on_shop.html',{'districts':districts})

def getShopArea(request):
    d_id=request.GET.get('district_id')
    shops=ration_shop_tb.objects.filter(district_id=d_id)
    return render(request,'get_shop_area.html',{'data':shops})

@login_required
def getStockOnShop(request):
    #plist=[]
    s_id=request.GET.get('shop_id')
    customer=customer_tb.objects.filter(id=request.session['customer_id'])
    
    card=customer[0].card_category_id
    stock=shop_stock_tb.objects.values('product_id__product','stock','product_id__yellow_price','product_id__pink_price','product_id__blue_price','product_id__white_price').filter(shop_id=s_id)
    
##    if(card.category=="Yellow"):
##        stock=shop_stock_tb.objects.values('product_id','stock','product_id__yellow_price').filter(shop_id=s_id)
##        #plist.append(admin_stock[0].yellow_price)
##    elif(card.category=="Pink"):
##        stock=shop_stock_tb.objects.values('product_id','stock','product_id__pink_price').filter(shop_id=s_id)
##        #plist.append(admin_stock[0].pink_price)
##    elif(card.category=="Blue"):
##        stock=shop_stock_tb.objects.values('product_id','stock','product_id__blue_price').filter(shop_id=s_id)
##        #plist.append(admin_stock[0].blue_price)
##    else:
##        stock=shop_stock_tb.objects.values('product_id','stock','product_id__white_price').filter(shop_id=s_id)
        #plist.append(admin_stock[0].white_price)
    
    #stock=shop_stock_tb.objects.filter(shop_id=s_id)
    scheduled_time=time_tb.objects.filter(shop_id=s_id,date=datetime.date.today()).order_by('-id')
    shop=ration_shop_tb.objects.filter(id=s_id)
    if(stock.count()>0):
        return render(request,'get_stock_on_shop.html',{'data':stock,'stime':scheduled_time,'shop':shop})
    else:
        return render(request,'get_stock_on_shop.html',{'msg':'no data','stime':scheduled_time,'shop':shop})

@login_required
def purchaseRequest(request):
    customer=customer_tb.objects.filter(id=request.session['customer_id'])
    members=members_tb.objects.filter(customer_id=request.session['customer_id'])
    if(members.count() == 0):
        messages.add_message(request,messages.INFO,"You must add members first")
        return redirect('index')
    elif(members.count()<int(customer[0].member_count)):
        messages.add_message(request,messages.INFO,"You must add all members")
        return redirect('index')
    else:
        districts=district_tb.objects.all()
        return render(request,'purchase_request.html',{'districts':districts,'month':range(1,13)})

@login_required
def purchaseRequestAction(request):
    purchase=purchase_request_tb.objects.filter(customer_id=request.session['customer_id'],year=request.POST['year'],month=request.POST['month'])
    if(purchase.count()>0):
        messages.add_message(request,messages.INFO,"You have already made request for this month")
        #return render(request,'purchase_request.html',{'states':states,'msg':'You have already made request for this month','month':range(1,13)})
    else:
        sid=ration_shop_tb.objects.get(id=request.POST['shop'])
        cid=customer_tb.objects.get(id=request.session['customer_id'])
        purchase=purchase_request_tb(shop_id=sid,customer_id=cid,year=request.POST['year'],month=request.POST['month'],date=datetime.date.today(),status='pending')
        purchase.save()
        messages.add_message(request,messages.INFO,"Request Sent")
        #return render(request,'purchase_request.html',{'states':states,'msg':'Request Sent','month':range(1,13)})
    return redirect('purchaseRequest')

@login_required
def requestStatus(request):
    return render(request,'request_status.html',{'month':range(1,13)})

@login_required
def getPurchaseRequestStatus(request):
    month=request.GET.get('month')
    year=request.GET.get('year')
    purchase=purchase_request_tb.objects.filter(customer_id=request.session['customer_id'],month=month,year=year)
    if(purchase.count()>0):
        return render(request,'get_purchase_request_status.html',{'data':purchase})
    else:
        return render(request,'get_purchase_request_status.html',{'msg':'No request'})

@login_required
def allocationDetailsForCustomer(request,pid):
    allot_list=[]
    allotted=product_allot_tb.objects.filter(purchase_id=pid)
    allotted_products=allocation_tb.objects.filter(allot_id=allotted[0].id)
    return render(request,'allocation_details_for_customer.html',{'data':allotted,'products':allotted_products})

@login_required
def writeComplaint(request):
    return render(request,'write_complaint.html')

@login_required
def writeComplaintAction(request):
    cid=customer_tb.objects.get(id=request.session['customer_id'])
    complaint=complaint_tb(customer_id=cid,subject=request.POST['subject'],complaint=request.POST['complaint'],date=datetime.date.today())
    complaint.save()
    messages.add_message(request,messages.INFO,"Submitted Successfully")
    return redirect('writeComplaint')

@login_required
def addMembers(request):
    members=members_tb.objects.filter(customer_id=request.session['customer_id'])
    if(members.count()>0):
        return render(request,'add_members.html',{'data':members})
    else:
        return render(request,'add_members.html',{'message':'no data'})

@login_required
def addMembersAction(request):
    cid=customer_tb.objects.get(id=request.session['customer_id'])
    members=members_tb.objects.filter(customer_id=request.session['customer_id'])
    if(members.count()<int(cid.member_count)):
        member=members_tb(name=request.POST['member_name'],relationship=request.POST['relationship'],dob=request.POST['dob'],job=request.POST['job'],
                          income=request.POST['income'],customer_id=cid)
        member.save()
        messages.add_message(request,messages.INFO,"Added Successfully")
        #return render(request,'add_members.html',{'msg':'Added Successfully','data':members})
    else:
        messages.add_message(request,messages.INFO,"Memebr Count Exceeds...") 
        #return render(request,'add_members.html',{'msg':'Memebr Count Exceeds...','data':members})
    return redirect('addMembers')

@login_required
def payForOrder(request,aid):
    allotted=product_allot_tb.objects.filter(id=aid)
    return render(request,'pay_for_order.html',{'data':allotted})

@login_required
def payForOrderAction(request):
    account=bank_tb.objects.filter(name=request.POST['name'],credit_card_number=request.POST['c_c_n'],cvv=request.POST['cvv'])
    allotted=product_allot_tb.objects.filter(id=request.POST['allocation_id'])
    if(account.count()>0):
        amount=Decimal(request.POST['amount'])
        balance=Decimal(account[0].balance)
        new_balance=balance-amount
        if(new_balance<2000):
            messages.add_message(request,messages.INFO,"Not Enough Balance")
            #return render(request,'pay_for_order.html',{'msg':'Not Enough Balance','data':allotted})
            return redirect('payForOrder',aid=request.POST['allocation_id'])
        else:
            aid=product_allot_tb.objects.get(id=request.POST['allocation_id'])
            cid=customer_tb.objects.get(id=request.session['customer_id'])
            sid=ration_shop_tb.objects.get(id=request.POST['shop_id'])
            pid=purchase_request_tb.objects.get(id=request.POST['purchase_id'])
            key=random.randint(100000,999999)
            payment=payment_tb(allocation_id=aid,amount=request.POST['amount'],transaction_key=key,date=datetime.date.today(),customer_id=cid,shop_id=sid,purchase_id=pid)
            payment.save()
            account.update(balance=new_balance)
            purchase=purchase_request_tb.objects.filter(id=request.POST['purchase_id']).update(status="paid")
            messages.add_message(request,messages.INFO,"Payment Successful")
            #return render(request,'allocation_details_for_customer.html',{'data':allotted,'msg':'Payment Successful'})
            return redirect('allocationDetailsForCustomer',pid=request.POST['purchase_id'])
    else:
        messages.add_message(request,messages.INFO,"invalid data")
        #return render(request,'pay_for_order.html',{'msg':'invalid data','data':allotted})
        return redirect('payForOrder',aid=request.POST['allocation_id'])

@login_required
def paymentDetailsForCustomer(request,aid):
    payment=payment_tb.objects.filter(allocation_id=aid)
    return render(request,'view_payment_details.html',{'data':payment})

@login_required
def updateProfile(request):
    customer=customer_tb.objects.filter(id=request.session['customer_id'])
    districts=district_tb.objects.all().exclude(id=customer[0].district_id_id)
    shops=ration_shop_tb.objects.filter(district_id=customer[0].district_id_id).exclude(id=customer[0].shop_id_id)
    card=card_category_tb.objects.all().exclude(id=customer[0].card_category_id_id)
    return render(request,'update_profile.html',{'data':customer,'districts':districts,'shops':shops,'card':card})

@login_required
def updateProfileAction(request):
    pic=""
    customer=customer_tb.objects.filter(id=request.session['customer_id'])
    if(len(request.FILES)>0):
        pic=request.FILES['fileupload']
    else:
        pic=customer[0].owner_photo
    d_id=district_tb.objects.get(id=request.POST['district'])
    rshop_id=ration_shop_tb.objects.get(id=request.POST['shop'])
    card_category=card_category_tb.objects.get(id=request.POST['category'])


    user=User.objects.get(username=customer[0].username)
##    cstmr=customer_tb.objects.filter(username=request.POST['username']).exclude(username=customer[0].username)
##    admin=admin_tb.objects.filter(username=request.POST['username'])
##    shop=ration_shop_tb.objects.filter(username=request.POST['username'])
##    if((cstmr.count()>0) or (admin.count()>0) or (shop.count()>0)):
##        return render(request,'update_profile.html',{'data':customer,'states':states,'districts':districts,'shops':shops,'card':card,'msg':'Username already exists'})
##    else:
    customer_obj=customer_tb.objects.get(id=request.session['customer_id'])
    customer_obj.card_number=request.POST['card_no']
    customer_obj.card_owner=request.POST['owner_name']
    customer_obj.owner_photo=pic
    customer_obj.house_number=request.POST['house_no']
    customer_obj.address=request.POST['address']
    customer_obj.district_id=d_id
    customer_obj.taluk=request.POST['taluk']
    customer_obj.ward_number=request.POST['ward_no']
    customer_obj.member_count=request.POST['m_count']
    customer_obj.adults=request.POST['adults']
    customer_obj.child=request.POST['children']
    customer_obj.units=request.POST['units']
    customer_obj.shop_id=rshop_id
    customer_obj.card_category_id=card_category
    customer_obj.monthly_income=request.POST['income']
    customer_obj.phone=request.POST['phone']
    customer_obj.aadhaar_number=request.POST['a_number']
    customer_obj.username=request.POST['username']
    customer_obj.password=request.POST['password']
    customer_obj.save()
    user.username=request.POST['username']
    user.set_password(request.POST['password'])
    user.save()
    user=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
    auth.login(request,user)
    request.session['customer_id']=customer[0].id
    messages.add_message(request,messages.INFO,"Updated Successfully")
    #return render(request,'update_profile.html',{'data':customer,'states':states,'districts':districts,'shops':shops,'card':card,'msg':'Updated Successfully'})
    return redirect('updateProfile')

@login_required
def updateMember(request,mid):
    member=members_tb.objects.filter(id=mid)
    return render(request,'update_member.html',{'data':member})

@login_required
def updateMemberAction(request):
    member=members_tb.objects.filter(id=request.POST['mid'])
    member.update(name=request.POST['member_name'],relationship=request.POST['relationship'],dob=request.POST['dob'],job=request.POST['job'],
                  income=request.POST['income'])
    messages.add_message(request,messages.INFO,"Updated Successfully")
    #return render(request,'update_member.html',{'data':member,'msg':'Updated Successfully'})
    return redirect('updateMember',mid=request.POST['mid'])

@login_required
def removeMember(request,mid):
    member=members_tb.objects.filter(id=mid).delete()
    members=members_tb.objects.filter(customer_id=request.session['customer_id'])
    if(members.count()>0):
        return render(request,'add_members.html',{'data':members})
    else:
        return render(request,'add_members.html',{'message':'no data'})

@login_required
def notification(request):
    notifications=notification_tb.objects.filter(customer_id=request.session['customer_id'],status='unread').order_by('-id')
    replies=reply_tb.objects.filter(customer_id=request.session['customer_id'],status='unread').order_by('-id')
    return render(request,'notification.html',{'data':notifications,'replies':replies})

@login_required
def readNoty(request,nid,tab):
    if(tab == '1'):
        noty=notification_tb.objects.filter(id=nid).update(status='read')
    else:
        reply=reply_tb.objects.filter(id=nid).update(status='read')
    return redirect('notification')


    


    

