"""Online_Ration_Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from Admin import views as admin_view
from Customer import views as customer_view
from Ration_Shop import views as ration_shop_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',admin_view.index,name='index'),
    url(r'^login/',admin_view.login,name='login'),
    url(r'^loginAction/',admin_view.loginAction,name='loginAction'),
    url(r'^addRationShop/',admin_view.addRationShop,name='addRationShop'),
    url(r'^getDistrict/',admin_view.getDistrict,name='getDistrict'),
    url(r'^addRationShopAction/',admin_view.addRationShopAction,name='addRationShopAction'),
    url(r'^manageRationShop/',admin_view.manageRationShop,name='manageRationShop'),
    url(r'^updateRationShop/(?P<rid>\d+)/$',admin_view.updateRationShop,name='updateRationShop'),
    url(r'^updateRationShopAction/',admin_view.updateRationShopAction,name='updateRationShopAction'),
    url(r'^deleteRationShop/(?P<rid>\d+)/$',admin_view.deleteRationShop,name='deleteRationShop'),
    url(r'^viewStock/',admin_view.viewStock,name='viewStock'),
    url(r'^updateStock/(?P<pid>\d+)/$',admin_view.updateStock,name='updateStock'),
    url(r'^updateStockAction/',admin_view.updateStockAction,name='updateStockAction'),
    url(r'^allotRationProduct/(?P<sid>\d+)/$',admin_view.allotRationProduct,name='allotRationProduct'),
    url(r'^allotAction/',admin_view.allotAction,name='allotAction'),
    url(r'^checkStock/',admin_view.checkStock,name='checkStock'),
    url(r'^viewAllotedRation/',admin_view.viewAllotedRation,name='viewAllotedRation'),
    url(r'^getAllotedRation/',admin_view.getAllotedRation,name='getAllotedRation'),
    url(r'^viewAllocationByAdmin/',admin_view.viewAllocationByAdmin,name='viewAllocationByAdmin'),
    url(r'^viewAllocation/',ration_shop_view.viewAllocation,name='viewAllocation'),
    url(r'^addProduct/',admin_view.addProduct,name='addProduct'),
    url(r'^addProductAction/',admin_view.addProductAction,name='addProductAction'),
    url(r'^signupCustomer/',customer_view.signupCustomer,name='signupCustomer'),
    url(r'^signupCustomerAction/',customer_view.signupCustomerAction,name='signupCustomerAction'),
    url(r'^viewCustomers/',admin_view.viewCustomers,name="viewCustomers"),
    url(r'^approveCustomer/(?P<cid>\d+)/$',admin_view.approveCustomer,name='approveCustomer'),
    url(r'^rejectCustomer/(?P<cid>\d+)/$',admin_view.rejectCustomer,name='rejectCustomer'),
    url(r'^viewStockOnShop/',customer_view.viewStockOnShop,name='viewStockOnShop'),
    url(r'^viewStockShop/',ration_shop_view.viewStockShop,name='viewStockShop'),
    url(r'^scheduleTime/',ration_shop_view.scheduleTime,name='scheduleTime'),
    url(r'^scheduleTimeAction/',ration_shop_view.scheduleTimeAction,name='scheduleTimeAction'),
    url(r'^purchaseRequest/',customer_view.purchaseRequest,name='purchaseRequest'),
    url(r'^getStockOnShop/',customer_view.getStockOnShop,name='getStockOnShop'),
    url(r'^getShop/',admin_view.getShop,name='getShop'),
    url(r'^purchaseRequestAction/',customer_view.purchaseRequestAction,name='purchaseRequestAction'),
    url(r'^viewPurchaseRequest/',ration_shop_view.viewPurchaseRequest,name='viewPurchaseRequest'),
    url(r'^getPurchaseRequest/',ration_shop_view.getPurchaseRequest,name='getPurchaseRequest'),
    url(r'^allotProductForCustomer/(?P<pid>\d+)/$',ration_shop_view.allotProductForCustomer,name='allotProductForCustomer'),
    url(r'^checkShopStock/',ration_shop_view.checkShopStock,name='checkShopStock'),
    url(r'^allotProductForCustomerAction/',ration_shop_view.allotProductForCustomerAction,name='allotProductForCustomerAction'),
    url(r'^allocationDetails/(?P<pid>\d+)/$',ration_shop_view.allocationDetails,name='allocationDetails'),
    url(r'^requestStatus/',customer_view.requestStatus,name='requestStatus'),
    url(r'^getPurchaseRequestStatus/',customer_view.getPurchaseRequestStatus,name='getPurchaseRequestStatus'),
    url(r'^allocationDetailsForCustomer/(?P<pid>\d+)/$',customer_view.allocationDetailsForCustomer,name='allocationDetailsForCustomer'),
    url(r'^getShopArea/',customer_view.getShopArea,name='getShopArea'),
    url(r'^writeComplaint/',customer_view.writeComplaint,name='writeComplaint'),
    url(r'^writeComplaintAction/',customer_view.writeComplaintAction,name='writeComplaintAction'),
    url(r'^viewComplaints/',admin_view.viewComplaints,name='viewComplaints'),
    url(r'^complaintDetails/(?P<cid>\d+)/$',admin_view.complaintDetails,name='complaintDetails'),
    url(r'^deleteComplaint/(?P<cid>\d+)/',admin_view.deleteComplaint,name='deleteComplaint'),
    url(r'^addMembers/',customer_view.addMembers,name='addMembers'),
    url(r'^addMembersAction/',customer_view.addMembersAction,name='addMembersAction'),
    url(r'^viewMembers/(?P<cid>\d+)/$',admin_view.viewMembers,name='viewMembers'),
    url(r'^approveOrReject/(?P<cid>\d+)/$',admin_view.approveOrReject,name='approveOrReject'),
    url(r'^payForOrder/(?P<aid>\d+)/$',customer_view.payForOrder,name='payForOrder'),
    url(r'^payForOrderAction/',customer_view.payForOrderAction,name='payForOrderAction'),
    url(r'^paymentDetailsForCustomer/(?P<aid>\d+)/$',customer_view.paymentDetailsForCustomer,name='paymentDetailsForCustomer'),
    url(r'^paymentDetailsRationShop/(?P<aid>\d+)/$',ration_shop_view.paymentDetailsRationShop,name='paymentDetailsRationShop'),
    url(r'^paymentReports/',admin_view.paymentReports,name='paymentReports'),
    url(r'^viewReport/',admin_view.viewReport,name='viewReport'),
    url(r'^reportProductShortage/',ration_shop_view.reportProductShortage,name='reportProductShortage'),
    url(r'^reportProductShortageAction/',ration_shop_view.reportProductShortageAction,name='reportProductShortageAction'),
    url(r'^shortageRequestStatus/',ration_shop_view.shortageRequestStatus,name='shortageRequestStatus'),
    url(r'^getShortageRequest/',ration_shop_view.getShortageRequest,name='getShortageRequest'),
    url(r'^updateToCollected/(?P<sid>\d+)/$',ration_shop_view.updateToCollected,name='updateToCollected'),
    url(r'^productShortageReport/',admin_view.productShortageReport,name='productShortageReport'),
    url(r'^getProductShort/',admin_view.getProductShort,name='getProductShort'),
    url(r'^getShortageReport/',admin_view.getShortageReport,name='getShortageReport'),
    url(r'^getAllottedForShortage/',admin_view.getAllottedForShortage,name='getAllottedForShortage'),
    url(r'^viewAllottedStock/',ration_shop_view.viewAllottedStock,name='viewAllottedStock'),
    url(r'^getAllottedStock/',ration_shop_view.getAllottedStock,name='getAllottedStock'),
    url(r'^statusToCollected/(?P<aid>\d+)/$',ration_shop_view.statusToCollected,name='statusToCollected'),
    url(r'^updateProfile/',customer_view.updateProfile,name='updateProfile'),
    url(r'^updateProfileAction/',customer_view.updateProfileAction,name='updateProfileAction'),
    url(r'^forgotPassword/',admin_view.forgotPassword,name='forgotPassword'),
    url(r'^getNext/',admin_view.getNext,name='getNext'),
    url(r'^changePasswordAction/',admin_view.changePasswordAction,name='changePasswordAction'),
    url(r'^checkValidOrNot/',admin_view.checkValidOrNot,name='checkValidOrNot'),
    url(r'^validateCustomerData/',admin_view.validateCustomerData,name='validateCustomerData'),
    url(r'^updateMember/(?P<mid>\d+)/$',customer_view.updateMember,name='updateMember'),
    url(r'^updateMemberAction/',customer_view.updateMemberAction,name='updateMemberAction'),
    url(r'^removeMember/(?P<mid>\d+)/$',customer_view.removeMember,name='removeMember'),
    url(r'^notification/',customer_view.notification,name='notification'),
    url(r'^replyAction/',admin_view.replyAction,name='replyAction'),
    url(r'^readNoty/(?P<nid>\d+)/(?P<tab>\d+)/$',customer_view.readNoty,name='readNoty'),
    url(r'^purchaseCollected/(?P<pid>\d+)/$',ration_shop_view.purchaseCollected,name='purchaseCollected'),
    url(r'^checkUsername/',admin_view.checkUsername,name='checkUsername'),
    url(r'^checktime/',ration_shop_view.checktime,name='checktime'),
    url(r'^checkendtime/',ration_shop_view.checkendtime,name='checkendtime'),
    url(r'^checktdate/',ration_shop_view.checktdate,name='checktdate'),
    url(r'^logout/',admin_view.logout,name='logout'),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
