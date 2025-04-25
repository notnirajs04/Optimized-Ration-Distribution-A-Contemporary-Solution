from django.shortcuts import render,redirect
from Ration_Shop.models import *
from Admin.models import *
import datetime
from Customer.models import *
from decimal import Decimal
from django.http import JsonResponse
import time
from django.contrib import messages
from django.contrib.auth.models import auth,User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def viewStockShop(request):
    stock=shop_stock_tb.objects.filter(shop_id=request.session['ration_shop_id'])
    if(stock.count()>0):
        return render(request,'view_stock_by_shop.html',{'data':stock})
    else:
        return render(request,'view_stock_by_shop.html',{'msg':'No Data'})

@login_required
def scheduleTime(request):
    time=time_tb.objects.filter(shop_id=request.session['ration_shop_id'],date=datetime.date.today())
    return render(request,'schedule_time.html',{'stime':time})

@login_required
def scheduleTimeAction(request):
    if request.POST["sc_time"] == "Update":
        time=time_tb.objects.filter(id=request.POST['tid']).update(opening_time=request.POST['opening_time'],closing_time=request.POST['closing_time'])
        messages.add_message(request,messages.INFO,"Updated Successfully")
    else:
        sid=ration_shop_tb.objects.get(id=request.session['ration_shop_id'])
        time=time_tb(shop_id=sid,opening_time=request.POST['opening_time'],closing_time=request.POST['closing_time'],date=datetime.date.today())
        time.save()
        messages.add_message(request,messages.INFO,"Added Successfully")
    return redirect('/')

@login_required
def viewPurchaseRequest(request):
    return render(request,'view_purchase_request.html',{'month':range(1,13)})

@login_required
def getPurchaseRequest(request):
    month=request.GET.get('month')
    year=request.GET.get('year')
    own=request.GET.get('own')
    print(own)
    if(own=='true'):
        purchase=purchase_request_tb.objects.filter(shop_id=request.session['ration_shop_id'],month=month,year=year,customer_id__in=customer_tb.objects.filter(shop_id=request.session['ration_shop_id']).values('id')).order_by('-id')
    else:
        purchase=purchase_request_tb.objects.filter(shop_id=request.session['ration_shop_id'],month=month,year=year).order_by('-id')
    if(purchase.count()>0):
        return render(request,'get_purchase_request.html',{'data':purchase})
    else:
        return render(request,'get_purchase_request.html',{'msg':'No requests'})

@login_required
def allotProductForCustomer(request,pid):
    purchase=purchase_request_tb.objects.filter(id=pid)
    members=members_tb.objects.filter(customer_id=purchase[0].customer_id_id)
    
    stock=shop_stock_tb.objects.filter(shop_id=request.session['ration_shop_id'])
    products=admin_stock_tb.objects.filter(id__in=shop_stock_tb.objects.filter(shop_id=request.session['ration_shop_id']).values('product_id'))
    return render(request,'allot_product_customer.html',{'purchase':purchase,'stock':stock,'members':members,'products':products})

@login_required
def allotProductForCustomerAction(request):
    t_price=0
    doc=request.POST['date']
    toc=request.POST['time']
    purchase=purchase_request_tb.objects.filter(id=request.POST['purchase_id'])
    sid=ration_shop_tb.objects.get(id=request.session['ration_shop_id'])
    cid=customer_tb.objects.get(id=request.POST['customer_id'])
    pid=purchase_request_tb.objects.get(id=request.POST['purchase_id'])
    allocation=request.POST['products']
    plist=allocation.split(',')
    print(plist)
    customer=customer_tb.objects.filter(id=request.POST['customer_id'])
    card=customer[0].card_category_id
    j=1
    for pr in range(int(len(plist)/4)):
        u_stock=admin_stock_tb.objects.filter(id=int(plist[j]))
        if(card.category=="Yellow"):
            t_price=Decimal(t_price+(u_stock[0].yellow_price*Decimal(plist[j+2])))
        elif(card.category=="Pink"):
            t_price=Decimal(t_price+(u_stock[0].pink_price*Decimal(plist[j+2])))
        elif(card.category=="Blue"):
            t_price=Decimal(t_price+(u_stock[0].blue_price*Decimal(plist[j+2])))
        else:
            t_price=Decimal(t_price+(u_stock[0].white_price*Decimal(plist[j+2])))
    
        j=j+4
    allotted=product_allot_tb(purchase_id=pid,shop_id=sid,customer_id=cid,date_of_allocation=datetime.date.today(),date_for_collecting=doc,
                             time_for_collecting=toc,total_price=t_price)
    allotted.save()
    latest_allot=product_allot_tb.objects.all().order_by('-id')
    aid=product_allot_tb.objects.get(id=latest_allot[0].id)
    price=0
    j=1
    for pr in range(int(len(plist)/4)):
        u_stock=shop_stock_tb.objects.filter(shop_id=request.session['ration_shop_id'],product_id=int(plist[j]))
        new_stock=u_stock[0].stock-Decimal(plist[j+2])
        u_stock.update(stock=new_stock)
        
        prdct=admin_stock_tb.objects.get(id=int(plist[j]))
        if(card.category=="Yellow"):
            price=prdct.yellow_price*Decimal(plist[j+2])
        elif(card.category=="Pink"):
            price=prdct.pink_price*Decimal(plist[j+2])
        elif(card.category=="Blue"):
            price=prdct.blue_price*Decimal(plist[j+2])
        else:
            price=prdct.white_price*Decimal(plist[j+2])
        product_obj=allocation_tb(allot_id=aid,product_id=prdct,stock=Decimal(plist[j+2]),price=price)
        product_obj.save()
        
        j=j+4
        
    purchase.update(status="allotted")
    notification=notification_tb(request_id=pid,customer_id=cid,datetime=time.asctime(time.localtime(time.time())))
    notification.save()
    members=members_tb.objects.filter(customer_id=purchase[0].customer_id_id)
    products=admin_stock_tb.objects.all()
    stock=shop_stock_tb.objects.filter(shop_id=request.session['ration_shop_id'])
    messages.add_message(request,messages.INFO,"Allotted Successfully")
    #return render(request,'allot_product_customer.html',{'msg':'Allotted Successfully','purchase':purchase,'stock':stock,'members':members,'products':products})
    return redirect('allotProductForCustomer',pid=request.POST['purchase_id'])

@login_required
def checkShopStock(request):
    pid=request.GET.get('pid')
    allotted=Decimal(request.GET.get('allotted'))
    shop_stock=shop_stock_tb.objects.filter(shop_id=request.session['ration_shop_id'],product_id=pid)
    if shop_stock.count()>0:
        new_stock=shop_stock[0].stock-allotted
        if(new_stock<0):
            return JsonResponse({'message':'not ok'})
        else:
            return JsonResponse({'message':'ok'})
    else:
        return JsonResponse({'message':'empty'})

@login_required
def allocationDetails(request,pid):
    allocation=product_allot_tb.objects.filter(purchase_id=pid)
    allotted_products=allocation_tb.objects.filter(allot_id=allocation[0].id)
    return render(request,'allocation_details.html',{'data':allocation,'products':allotted_products})

@login_required
def paymentDetailsRationShop(request,aid):
    payment=payment_tb.objects.filter(allocation_id=aid)
    return render(request,'payment_details_shop.html',{'data':payment})

@login_required
def reportProductShortage(request):
    products=admin_stock_tb.objects.all()
    return render(request,'report_product_shortage.html',{'month':range(1,13),'products':products})

@login_required
def reportProductShortageAction(request):
    sid=ration_shop_tb.objects.get(id=request.session['ration_shop_id'])
    shortage=product_shortage_tb(shop_id=sid,month=request.POST['month'],year=request.POST['year'],date=datetime.date.today(),status='pending')
    shortage.save()
    required=request.POST['products']
    plist=required.split(',')
    
    latest_shortage=product_shortage_tb.objects.all().order_by('-id')
    lid=product_shortage_tb.objects.get(id=latest_shortage[0].id)
    
    j=1
    for pr in range(int(len(plist)/4)):
        prdct=admin_stock_tb.objects.get(id=int(plist[j]))
        product=product_required_tb(shortage_id=lid,product_id=prdct,stock=Decimal(plist[j+2]))
        product.save()
        j=j+4
    products=admin_stock_tb.objects.all()
    messages.add_message(request,messages.INFO,"Submitted Successfully")
    #return render(request,'report_product_shortage.html',{'month':range(1,13),'msg':'Submitted Successfully','products':products})
    return redirect('reportProductShortage')

@login_required
def shortageRequestStatus(request):
    return render(request,'shortage_request_status.html',{'month':range(1,13)})

@login_required
def getShortageRequest(request):
    month=request.GET.get('month')
    year=request.GET.get('year')
    shortage=product_shortage_tb.objects.filter(shop_id=request.session['ration_shop_id'],month=month,year=year).order_by('-id')
    if(shortage.count()>0):
        return render(request,'get_shortage_request_status.html',{'data':shortage})
    else:
        return render(request,'get_shortage_request_status.html',{'msg':'No Reports'})

@login_required
def updateToCollected(request,sid):
    shortage=product_shortage_tb.objects.filter(id=sid)
    stock=shop_stock_tb.objects.filter(shop_id=request.session['ration_shop_id'])
    sid=ration_shop_tb.objects.get(id=request.session['ration_shop_id'])
##    allotted=stock_allot_tb.objects.filter(id=shortage[0].allocation_id_id)
##    
##    for s in stock:
##        u_stock=shop_stock_tb.objects.filter(shop_id=request.session['ration_shop_id'],product_id=s.product_id_id)
##        if u_stock.count()>0:
##            a_stock=allotted_product_tb.objects.filter(product_id=u_stock[0].product_id_id,allot_id=shortage[0].allocation_id_id)
##        
##            new_stock=u_stock[0].stock+a_stock[0].stock
##            u_stock.update(stock=new_stock)
##        else:
##            new_product=shop_stock_tb(shop_id=s.shop_id,product_id=allocation[i].product_id,stock=allocation[i].stock)
    allotted=allotted_product_tb.objects.filter(allot_id=shortage[0].allocation_id_id)   
    for a in allotted:
        stock=shop_stock_tb.objects.filter(product_id=a.product_id_id,shop_id=request.session['ration_shop_id'])
        if stock.count()>0:
            new_stock=stock[0].stock+a.stock
            stock.update(stock=new_stock)
        else:
            s_stock=shop_stock_tb(shop_id=sid,product_id=a.product_id,stock=a.stock)
            s_stock.save()
    shortage.update(status='collected')
    allotted=stock_allot_tb.objects.filter(id=shortage[0].allocation_id_id)
    allotted.update(status='collected')
    return render(request,'shortage_request_status.html',{'data':shortage,'msg':'Updated Successfully','month':range(1,13)})

@login_required
def viewAllottedStock(request):
    return render(request,'view_allotted_stock.html',{'month':range(1,13)})

@login_required
def getAllottedStock(request):
    month=request.GET.get('month')
    year=request.GET.get('year')
    allocation=stock_allot_tb.objects.filter(shop_id=request.session['ration_shop_id'],month=month,year=year).order_by('-id')
    if(allocation.count()>0):
        return render(request,'get_allotted_stock.html',{'data':allocation})
    else:
        return render(request,'get_allotted_stock.html',{'msg':'No Allocations'})

@login_required    
def viewAllocation(request):
    aid=request.GET.get('allotid')
    allotted=allotted_product_tb.objects.filter(allot_id=aid)
    return render(request,'view_allocation.html',{'data':allotted})

@login_required
def statusToCollected(request,aid):
    allotted_stock=stock_allot_tb.objects.filter(id=aid)
    allotted_stock.update(status='collected')
    sid=ration_shop_tb.objects.get(id=request.session['ration_shop_id'])
    shop_stock=shop_stock_tb.objects.filter(shop_id=sid)
    allocation=allotted_product_tb.objects.filter(allot_id=aid)   
    for a in allocation:
        stock=shop_stock_tb.objects.filter(product_id=a.product_id_id,shop_id=request.session['ration_shop_id'])
        if stock.count()>0:
            new_stock=stock[0].stock+a.stock
            stock.update(stock=new_stock)
        else:
            s_stock=shop_stock_tb(shop_id=sid,product_id=a.product_id,stock=a.stock)
            s_stock.save()
##    if(shop_stock.count()>0):
##        for i in range(allocation.count()):
##            u_stock=shop_stock_tb.objects.filter(shop_id=sid,product_id=allocation[i].product_id)
##            allot_stock=allotted_product_tb.objects.filter(allot_id=aid,product_id=u_stock[0].product_id)
##            new_stock=u_stock[0].stock+allot_stock[0].stock
##            u_stock.update(stock=new_stock)
##    else:
##        for i in range(allocation.count()):
##            stock=shop_stock_tb(shop_id=sid,product_id=allocation[i].product_id,stock=allocation[i].stock)
##            stock.save()

    shortage=product_shortage_tb.objects.filter(allocation_id=aid)
    if(shortage.count()>0):
        shortage.update(status='collected')
    #return render(request,'view_allotted_stock.html',{'msg':'Updated Successfully','month':range(1,13)})
    messages.add_message(request,messages.INFO,"Updated Successfully")
    return redirect('viewAllottedStock')

@login_required
def purchaseCollected(request,pid):
    purchase=purchase_request_tb.objects.filter(id=pid).update(status="collected")
    messages.add_message(request,messages.INFO,"Updated Status To Collected")
    return redirect('viewPurchaseRequest')

def checktime(request):
    crrnt = datetime.datetime.now().strftime('%H:%M')
    crrnt_obj = datetime.datetime.strptime(crrnt, '%H:%M')
    time_en=request.GET['time']
    if 'P' in time_en:
        ptime = int(time_en.split(' ')[0].split(':')[0])
        if ptime != 12:
            ptime = ptime + 12
            s = ':'
            l = [str(ptime), time_en.split(' ')[0].split(':')[1]]
            realtime = s.join(l)
        else:
            realtime = time_en.split(' ')[0]
    else:
        realtime = time_en.split(' ')[0]
    time_en_obj = datetime.datetime.strptime(realtime, '%H:%M')
    if time_en_obj < crrnt_obj:
        return JsonResponse({'status':'not ok'})
    else:
        return JsonResponse({'status':'ok'})

def checkendtime(request):
    stime=request.GET['stime']
    etime=request.GET['etime']
    if stime:
        if 'P' in stime:
            ptime = int(stime.split(' ')[0].split(':')[0])
            if ptime != 12:
                ptime = ptime + 12
                s = ':'
                l = [str(ptime), stime.split(' ')[0].split(':')[1]]
                realtime = s.join(l)
            else:
                realtime = stime.split(' ')[0]
        else:
            realtime = stime.split(' ')[0]
        stime_obj = datetime.datetime.strptime(realtime, '%H:%M')
    
        if 'P' in etime:
            ptime = int(etime.split(' ')[0].split(':')[0])
            if ptime != 12:
                ptime = ptime + 12
                s = ':'
                l = [str(ptime), etime.split(' ')[0].split(':')[1]]
                realtime = s.join(l)
            else:
                realtime = etime.split(' ')[0]
        else:
            realtime = etime.split(' ')[0]
        etime_obj = datetime.datetime.strptime(realtime, '%H:%M') 
        if(etime_obj < stime_obj):
            return JsonResponse({'status':'not ok'})
        else:
            return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'no stime'})

def checktdate(request):
    date=request.GET['date']
    datelist=date.split('-')
    cdate=datetime.datetime(int(datelist[0]),int(datelist[1]),int(datelist[2]))
    currnt_date=str(datetime.date.today())
    cdatelist=currnt_date.split('-')
    currnt_date=datetime.datetime(int(cdatelist[0]),int(cdatelist[1]),int(cdatelist[2]))
    if cdate < currnt_date:
        return JsonResponse({'status':'not ok'})
    else:
        return JsonResponse({'status':'ok'})
    
    
    
                              
