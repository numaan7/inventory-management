
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('inventory',views.inventory,name='inventory'),
    path('<id>/delete',views.deleteproduct),
    path('<id>/update',views.updateproduct),
    path('dashboard',views.dashboard,name='dashboard'),
    path('invoice',views.invoice,name='invoice'),
     path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('update/<int:id>/',views.updateinvoice),
    path('add/customer/<int:id>/',views.addcustomer),
    path('create-customer',views.createcustomer),
    path('generate-invoice',views.generateinvoice),
    path('sales',views.sales,name="sales"),
    path('clear-due/<str:po_no>/',views.cleardue,name="sales"),
    path('ledger',views.ledger,name='ledger'),
    path('add-money',views.addmoney,name='addmoney'),
    path('withdraw-money',views.removemoney,name='withdraw'),
    path('login',views.loginhandle,name="loginhandle"),
    path('logout',views.handelLogout,name="logouthandle"),
    path('invoice/<str:po_no>/',views.invoicepdf),

]
   
