from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=200,unique=True)
    price=models.PositiveBigIntegerField(default=0)
    quantity=models.PositiveBigIntegerField(default=0)
    buy_price=models.PositiveBigIntegerField(default=0)
    
    date=models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.name
    @property
    def total(self):
        return self.price*self.quantity
    @property
    def totalcost(self):
        return self.buy_price*self.quantity
    
class Customer(models.Model):
    name=models.CharField(max_length=200)
    phone=models.CharField( max_length=12,unique=True)
    email=models.EmailField(blank=True)
    whatsapp=models.CharField(max_length=12,blank=True)
    gst_no=models.CharField(max_length=200,blank=True)
    address=models.TextField(blank=True)
    def __str__(self):
        return self.name
    
class Invoice_item(models.Model):
    STATUS = [
       
        ('Paid', "Paid"),
        ('Due', "Due"),
        
    ]
    invoice_no=models.CharField(max_length=10)
    po_number=models.CharField(max_length=10)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.PositiveBigIntegerField(default=0)
    quantity=models.PositiveBigIntegerField(default=0)
    total=models.PositiveBigIntegerField(default=0)
    date=models.DateTimeField(default=datetime.datetime.now())
    invoice_status=models.CharField(choices=STATUS,max_length= 100,default='Due')
    invoice_id=models.UUIDField()
    def __str__(self):
        return str(self.invoice_no)
    
class Invoice(models.Model):
    STATUS = [
        
        ('Paid', "Paid"),
        ('Due', "Due"),
        
    ]
    invoice_no=models.IntegerField()
    po_number=models.CharField(max_length=10)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    address=models.TextField(blank=True)
    invoice_items=models.ManyToManyField(Invoice_item)
    products=models.ManyToManyField(Product)
    quantity=models.PositiveBigIntegerField(default=0)
    subtotal=models.PositiveBigIntegerField(default=0)
    tax=models.PositiveBigIntegerField(default=0)
    discount=models.PositiveBigIntegerField(default=0)
    total=models.PositiveBigIntegerField(default=0)
    paid_amt=models.PositiveBigIntegerField(default=0)
    due_amt=models.PositiveBigIntegerField(default=0)
    invoice_pdf=models.FileField(upload_to='static/pdfs/',blank=True)
    date=models.DateTimeField(default=datetime.datetime.now())
    invoice_id=models.UUIDField( unique=True)
    invoice_status=models.CharField(choices=STATUS,max_length= 100,default='Due')

    
 
class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(blank=True)
    phone=models.CharField(max_length=12)
    message=models.TextField()
    date=models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.name
    
class Phone_Number(models.Model):
    phone=models.CharField(max_length=12)
    def __str__(self):
        return str(self.phone)


      


class Ledger(models.Model):
    STATUS = [
       
        ('Add', "Add"),
        ('Due', "Due"),
        ('Widthrawl','Withdrawl'),
        
    ]
    invoice_no=models.CharField(max_length=10,blank=True)
    po_number=models.CharField(max_length=10,blank=True)
    customer=models.ForeignKey(Customer ,on_delete=models.SET_NULL,blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    add=models.PositiveBigIntegerField(default=0)
    due=models.PositiveBigIntegerField(default=0)
    remove=models.PositiveBigIntegerField(default=0)
    purpose=models.TextField(default='For Business purpose')
    date=models.DateTimeField(default=datetime.datetime.now())
    status=models.CharField(choices=STATUS,max_length= 100,default='Due')
    def __str__(self):
        return str(self.id)












