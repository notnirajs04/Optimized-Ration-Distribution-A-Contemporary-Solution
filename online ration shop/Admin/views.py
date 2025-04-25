from django.shortcuts import render,redirect
from Admin.models import *
from Ration_Shop.models import *
import random
import datetime
from Customer.models import *
from decimal import Decimal
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import auth,User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.

def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')

def loginAction(request):
    admin=admin_tb.objects.filter(username=request.POST['username'],password=request.POST['password'])
    if admin.count()>0:
        request.session['admin_id']=admin[0].id
        return redirect('/')
    else:
        ration_shop=ration_shop_tb.objects.filter(username=request.POST['username'],password=request.POST['password'])
        if ration_shop.count()>0:
            request.session['ration_shop_id']=ration_shop[0].id
            user=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
            auth.login(request,user)
            return redirect('/')
        else:
            customer=customer_tb.objects.filter(username=request.POST['username'],password=request.POST['password'])
            if customer.count()>0:
                if customer[0].status=="approved":
                    request.session['customer_id']=customer[0].id
                    user=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
                    auth.login(request,user)
                    return redirect('/')
                else:
                    messages.add_message(request,messages.INFO,"account not verified yet")
                    return redirect('login')
            else:
                messages.add_message(request,messages.INFO,"Incorrect username or password")
                return redirect('login')

@never_cache
def addRationShop(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    districts=district_tb.objects.all()
    return render(request,'add_ration_shop.html',{'districts':districts})

def getDistrict(request):
    s_id=request.GET.get('state_id')
    districts=district_tb.objects.filter(state_id=s_id)
    return render(request,'get_district.html',{'data':districts})


def addRationShopAction(request):
    password=random.randint(10000000,99999999)
    d_id=district_tb.objects.get(id=request.POST['district'])
    shop=ration_shop_tb.objects.filter(shop_number=request.POST['shop_no'])
    if(shop.count()>0):
        messages.add_message(request,messages.INFO,"Shop Number Already Exists")
        
    else:
        shop_obj=ration_shop_tb.objects.filter(district_id=request.POST['district'],area=request.POST['area'])
        if(shop_obj.count()>0):
            messages.add_message(request,messages.INFO,"You have already added a shop for this area")
            
        else:
            ration_shop=ration_shop_tb(shop_number=request.POST['shop_no'],district_id=d_id,area=request.POST['area'],address=request.POST['address'],
                               username=request.POST['shop_no'],password=password)
            ration_shop.save()
            user=User.objects.create_user(username=request.POST['shop_no'],password=str(password))
            user.save()
            messages.add_message(request,messages.INFO,"Added successfully")
    return redirect('addRationShop')

@never_cache
def manageRationShop(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    ration_shop=ration_shop_tb.objects.all().order_by('-id')
    return render(request,'manage_ration_shop.html',{'data':ration_shop})

@never_cache
def updateRationShop(request,rid):
    if 'admin_id' not in request.session:
        return redirect('login')
    ration_shop=ration_shop_tb.objects.filter(id=rid)
    districts=district_tb.objects.all().exclude(id=ration_shop[0].district_id_id)
    return render(request,'update_ration_shop.html',{'data':ration_shop,'districts':districts})


def updateRationShopAction(request):
    rid=request.POST['shop_id']
    d_id=district_tb.objects.get(id=request.POST['district'])
    ration_shop=ration_shop_tb.objects.filter(id=rid).update(shop_number=request.POST['shop_no'],district_id=d_id,
                                                             area=request.POST['area'],address=request.POST['address'],username=request.POST['shop_no'])
    r_shop=ration_shop_tb.objects.filter(id=rid)
    user=User.objects.get(username=r_shop[0].username)
    user.username=request.POST['shop_no']
    user.save()
    messages.add_message(request,messages.INFO,"update successful")
    return redirect('updateRationShop',rid=rid)
    

@never_cache
def deleteRationShop(request,rid):
    if 'admin_id' not in request.session:
        return redirect('login')
    ration_shop=ration_shop_tb.objects.filter(id=rid)
    username=ration_shop[0].username
    ration_shop.delete()
    user=User.objects.filter(username=username).delete()
    ration_shop=ration_shop_tb.objects.all().order_by('-id')
    messages.add_message(request,messages.INFO,"Deleted Successfully")
    return redirect('manageRationShop')

@never_cache
def viewStock(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    product=admin_stock_tb.objects.all()
    return render(request,'admin_view_stock.html',{'data':product})

@never_cache
def updateStock(request,pid):
    if 'admin_id' not in request.session:
        return redirect('login')
    product=admin_stock_tb.objects.filter(id=pid)
    return render(request,'update_stock.html',{'data':product})


def updateStockAction(request):
    product=admin_stock_tb.objects.filter(id=request.POST['p_id']).update(stock=request.POST['stock'],blue_price=request.POST['bprice'],
                                                                          pink_price=request.POST['pprice'],white_price=request.POST['wprice'],
                                                                          yellow_price=request.POST['yprice'])
    #u_product=admin_stock_tb.objects.filter(id=request.POST['p_id'])
    messages.add_message(request,messages.INFO,"Updated successfully")
    return redirect('updateStock',pid=request.POST['p_id'])

@never_cache
def allotRationProduct(request,sid):
    if 'admin_id' not in request.session:
        return redirect('login')
    districts=district_tb.objects.all()
    products=admin_stock_tb.objects.all()
    if( sid != 0):
        shortage=product_shortage_tb.objects.filter(id=sid)
        return render(request,'allot_ration_for_shop.html',{'districts':districts,'products':products,'shortage':shortage,'shortage_id':sid,'month':range(1,13)})
    else:
        return render(request,'allot_ration_for_shop.html',{'districts':districts,'products':products,'shortage_id':sid,'month':range(1,13)})


def checkStock(request):
    pid=request.GET.get('pid')
    allotted=Decimal(request.GET.get('allotted'))
    product=admin_stock_tb.objects.filter(id=pid)
    new_stock=product[0].stock-allotted
    if(new_stock<0):
        return JsonResponse({'message':'not ok'})
    else:
        return JsonResponse({'message':'ok'})

@never_cache
def allotAction(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    sid=int(request.GET.get('shortage'))
    shop=ration_shop_tb.objects.get(id=request.GET.get('shop'))
    month=request.GET.get('month')
    year=request.GET.get('year')
    products=request.GET.get('products')
    plist=products.split(',')
    
        
    allot_obj=stock_allot_tb(shop_id=shop,date=datetime.date.today(),month=month,year=year,status='allotted')
    allot_obj.save()
    latest_allot=stock_allot_tb.objects.all().order_by('-id')
    aid=stock_allot_tb.objects.get(id=latest_allot[0].id)
    j=1
    for pr in range(int(len(plist)/4)):
        u_stock=admin_stock_tb.objects.filter(id=int(plist[j]))
        new_stock=u_stock[0].stock-Decimal(plist[j+2])
        u_stock.update(stock=new_stock)
        
        pid=admin_stock_tb.objects.get(id=int(plist[j]))
        product_obj=allotted_product_tb(allot_id=aid,product_id=pid,stock=Decimal(plist[j+2]))
        product_obj.save()
        
        j=j+4

    if(sid != 0):
        shortage=product_shortage_tb.objects.filter(id=sid).update(allocation_id=aid,status="allotted")
       
    #products_combo=admin_stock_tb.objects.all()
    messages.add_message(request,messages.INFO,"Allotted Successfully")
    return redirect('allotRationProduct',sid=sid)

@never_cache
def viewAllotedRation(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    allotted=stock_allot_tb.objects.all()
    #shop=ration_shop_tb.objects.all()
    districts=district_tb.objects.all()
    return render(request,'view_allotted_ration.html',{'data':allotted,'districts':districts,'month':range(1,13)})

def getShop(request):
    d_id=request.GET.get('district_id')
    shops=ration_shop_tb.objects.filter(district_id=d_id)
    return render(request,'get_shops.html',{'data':shops})

@never_cache
def getAllotedRation(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    s_id=request.GET.get('shop_id')
    month=request.GET.get('month')
    year=request.GET.get('year')
    allotted=stock_allot_tb.objects.filter(shop_id=s_id,month=month,year=year).order_by('-id')
    return render(request,'get_allotted_ration.html',{'data':allotted})

@never_cache
def viewAllocationByAdmin(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    aid=request.GET.get('allotid')
    allocation=allotted_product_tb.objects.filter(allot_id=aid)
    return render(request,'view_allocation_by_admin.html',{'data':allocation})

@never_cache
def addProduct(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    return render(request,'add_product.html')

@never_cache
def addProductAction(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    product=request.POST['product']
    stock=Decimal(request.POST['stock'])
    white=Decimal(request.POST['white'])
    blue=Decimal(request.POST['blue'])
    yellow=Decimal(request.POST['yellow'])
    pink=Decimal(request.POST['pink'])
    check_product=admin_stock_tb.objects.filter(product=product)
    if(check_product.count()>0):
        messages.add_message(request,messages.INFO,"Already Added")
        return redirect('addProduct')
    else:
        product_stock=admin_stock_tb(product=product,stock=stock,yellow_price=yellow,pink_price=pink,blue_price=blue,white_price=white)
        product_stock.save()
        messages.add_message(request,messages.INFO,"Added Successfully")
        return redirect('addProduct')

@never_cache
def viewCustomers(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    customer=customer_tb.objects.all().order_by('-id')
    return render(request,'view_customers.html',{'data':customer})

@never_cache
def approveOrReject(request,cid):
    if 'admin_id' not in request.session:
        return redirect('login')
    customer=customer_tb.objects.filter(id=cid)
    return render(request,'approve_or_reject.html',{'data':customer})

@never_cache
def approveCustomer(request,cid):
    if 'admin_id' not in request.session:
        return redirect('login')
    customer=customer_tb.objects.filter(id=cid).update(status="approved")
    messages.add_message(request,messages.INFO,"Approved")
    return redirect('viewCustomers')

@never_cache
def rejectCustomer(request,cid):
    if 'admin_id' not in request.session:
        return redirect('login')
    customer=customer_tb.objects.filter(id=cid).update(status="rejected")
    messages.add_message(request,messages.INFO,"Rejected")
    return redirect('viewCustomers')

@never_cache
def viewComplaints(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    complaints=complaint_tb.objects.all().order_by('-id')
    if(complaints.count()>0):
        return render(request,'view_complaints.html',{'data':complaints})
    else:
        return render(request,'view_complaints.html',{'msg':'No Complaints'})

@never_cache
def complaintDetails(request,cid):
    if 'admin_id' not in request.session:
        return redirect('login')
    complaint=complaint_tb.objects.filter(id=cid)
    return render(request,'view_complaint_details.html',{'data':complaint})

@never_cache
def deleteComplaint(request,cid):
    if 'admin_id' not in request.session:
        return redirect('login')
    complaint=complaint_tb.objects.filter(id=cid).delete()
    complaints=complaint_tb.objects.all()
    if(complaints.count()>0):
        return render(request,'view_complaints.html',{'data':complaints})
    else:
        return render(request,'view_complaints.html',{'msg':'No Complaints'})

@never_cache
def viewMembers(request,cid):
    if 'admin_id' not in request.session:
        return redirect('login')
    members=members_tb.objects.filter(customer_id=cid)
    if(members.count()>0):
        return render(request,'view_members.html',{'data':members,'customer':cid})
    else:
        return render(request,'view_members.html',{'msg':'No data','customer':cid})



@never_cache
def paymentReports(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    districts=district_tb.objects.all()
    return render(request,'payment_reports.html',{'districts':districts,'month':range(1,13),'msg':' '})

@never_cache
def viewReport(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    payment_list=[]
    sid=request.GET.get('shop')
    month=request.GET.get('month')
    year=request.GET.get('year')
    purchase=purchase_request_tb.objects.filter(shop_id=sid,month=month,year=year,status="paid")
    if(purchase.count()>0):
        for p in purchase:
            payment=payment_tb.objects.filter(purchase_id=p.id)
            payment_list.append(payment)
        return render(request,'view_reports.html',{'data':payment_list})
    else:
        return render(request,'view_reports.html',{'msg':'No Data'})

@never_cache
def productShortageReport(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    return render(request,'product_shortage_report.html',{'month':range(1,13)})

@never_cache
def getShortageReport(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    month=request.GET.get('month')
    year=request.GET.get('year')
    shortage=product_shortage_tb.objects.filter(month=month,year=year).order_by('-id')
    if(shortage.count()>0):
        return render(request,'get_shortage_report.html',{'data':shortage})
    else:
        return render(request,'get_shortage_report.html',{'msg':'No Reports'})

@never_cache
def getProductShort(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    sid=request.GET.get('sid')
    products=product_required_tb.objects.filter(shortage_id=sid)
    return render(request,'get_product_short.html',{'products':products})

@never_cache
def getAllottedForShortage(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    sid=request.GET.get('sid')
    shortage=product_shortage_tb.objects.filter(id=sid)
    allotted=allotted_product_tb.objects.filter(allot_id=shortage[0].allocation_id_id)
    return render(request,'get_allotted_for_shortage.html',{'data':allotted})


def forgotPassword(request):
    return render(request,'forgot_password.html')

def getNext(request):
    username=request.POST['username']
    
    shop=ration_shop_tb.objects.filter(username=username)
    if(shop.count()>0):
        return render(request,'shop_data.html',{'username':username})
    else:
        customer=customer_tb.objects.filter(username=username)
        if(customer.count()>0):
            return render(request,'customer_data.html',{'username':username})
        else:
            messages.add_message(request,messages.INFO,"Invalid Username")
            return redirect('forgotPassword')

def changePasswordAction(request):
    new_password=request.POST['password']
    confirm_password=request.POST['confirm_password']
    username=request.POST['username']
    
    shop=ration_shop_tb.objects.filter(username=username)
    customer=customer_tb.objects.filter(username=username)
    
    if(shop.count()>0):
        shop.update(password=new_password)
    else:
        customer.update(password=new_password)
    user=User.objects.get(username=username)
    user.set_password(new_password)
    user.save()
    messages.add_message(request,messages.INFO,"Password Changed Successfully")
    return redirect('login')
            
            
def checkValidOrNot(request):
    shop_number=request.POST['shop_number']
    area=request.POST['area']
    username=request.POST['username']
    shop=ration_shop_tb.objects.filter(shop_number=shop_number,area=area,username=username)
    if(shop.count()>0):
        return render(request,'change_password.html',{'username':username})
    else:
        return render(request,'shop_data.html',{'msg':'Invalid Data','username':username})

def validateCustomerData(request):
    username=request.POST['username']
    card_number=request.POST['card_number']
    card_owner=request.POST['card_owner']
    aadhaar_number=request.POST['a_number']
    customer=customer_tb.objects.filter(card_number=card_number,card_owner=card_owner,aadhaar_number=aadhaar_number,username=username)
    if(customer.count()>0):
        return render(request,'change_password.html',{'username':username})
    else:
        return render(request,'customer_data.html',{'msg':'Invalid Data','username':username})

@never_cache
def replyAction(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    customer=customer_tb.objects.get(id=request.POST['customerid'])
    complaint=complaint_tb.objects.get(id=request.POST['complaintid'])
    subject=request.POST['subject']
    reply=request.POST['reply']
    reply_obj=reply_tb(complaint_id=complaint,customer_id=customer,subject=subject,reply=reply,date=datetime.date.today())
    reply_obj.save()
    messages.add_message(request,messages.INFO,"Reply Sent Successfully")
    return redirect('complaintDetails',cid=request.POST['complaintid'])
    
@never_cache
def returnToAdminHome(request):
    if 'admin_id' not in request.session:
        return redirect('login')
    return render(request,'admin_home.html')

def checkUsername(request):
    username=request.GET.get('username')
    status=''
    if 'customer_id' in request.session:
        customer=customer_tb.objects.filter(username=username).exclude(id=request.session['customer_id'])
    else:
        customer=customer_tb.objects.filter(username=username)
    admin=admin_tb.objects.filter(username=username)
    shop=ration_shop_tb.objects.filter(username=username)
    if((customer.count()>0) or (admin.count()>0) or (shop.count()>0)):
        status='exists'
    else:
        status='not exists'
    return JsonResponse({'status':status})
        
def logout(request):
    if 'customer_id' in request.session:
        del request.session['customer_id']
    if 'admin_id' in request.session:
        del request.session['admin_id']
    if 'ration_shop_id' in request.session:
        del request.session['ration_shop_id']
    auth.logout(request)
    return redirect('/')
        
    
    
