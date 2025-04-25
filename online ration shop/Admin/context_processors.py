from Ration_Shop.models import *
from Admin.models import *
import datetime

def getData(request):
    time=''
    not_count=0
    if 'ration_shop_id' in request.session:
        time=time_tb.objects.filter(shop_id=request.session['ration_shop_id'],date=datetime.date.today()).order_by('-id')
    if 'customer_id' in request.session:
        notification=notification_tb.objects.filter(customer_id=request.session['customer_id'],status='unread')
        reply=reply_tb.objects.filter(customer_id=request.session['customer_id'],status='unread')
        not_count=notification.count()+reply.count()
    return {
        'time':time,
        'not_count':not_count
        }
