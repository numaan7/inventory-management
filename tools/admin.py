from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'quantity', 'buy_price', 'price','total')
    list_filter = ('name', 'quantity', 'buy_price','price')
    search_fields = ('name', 'quantity', 'buy_price', 'price')
    
@admin.register(Invoice_item)
class InvoiceitemAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'invoice_no','quantity','total', 'product', 'date', 'invoice_status')
    list_filter = ('po_number', 'invoice_no','total', 'customer', 'date', 'invoice_status')
    search_fields = ('po_number', 'invoice_no','invoice_id')
    raw_id_fields = ('customer',)
    date_hierarchy = 'date'
    ordering = ('invoice_status', 'date')

   



@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'invoice_no','total', 'customer', 'date', 'invoice_status')
    list_filter = ('po_number', 'invoice_no','total', 'customer', 'date', 'invoice_status')
    search_fields = ('po_number', 'invoice_no','invoice_id')
    raw_id_fields = ('customer',)
    date_hierarchy = 'date'
    ordering = ('invoice_status', 'date')
    

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=('name', 'phone','whatsapp', 'address')
    list_filter = ('name', 'phone','whatsapp')
    search_fields = ('name', 'phone','whatsapp', 'address','gst_no')
   
    
    ordering = ('name', 'id')
@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'invoice_no','add', 'remove','due', 'date', 'status')
    list_filter = ('po_number', 'invoice_no','add', 'remove','due', 'date', 'status')
    search_fields = ('po_number', 'invoice_no')
    raw_id_fields = ('customer','user',)
    date_hierarchy = 'date'
    ordering = ('status', 'date')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone','email', 'message','date')
    list_filter = ('name', 'phone','email', 'date')
    search_fields = ('name', 'phone','email', 'message')

    date_hierarchy = 'date'
    ordering = ('id', 'date')
admin.site.register(Phone_Number)
