from django.shortcuts import  render,redirect,get_object_or_404,HttpResponse
from .models import Product,Invoice,Customer,Invoice_item,Ledger,Contact,Phone_Number
from django.contrib.auth.decorators import login_required
from .cart import Cart
from django.contrib import messages
from qrcode import *

from django.conf import settings
import datetime
from django.contrib.auth  import authenticate,  login, logout
from django.template.loader import get_template
from weasyprint import HTML
import io
from qrcode import *
import time
import uuid
def home(request):
    if request.method=="POST":
        try:
            name=request.POST.get('name')
            phone=request.POST.get('phone')
            email=request.POST.get('email')
            message=request.POST.get('message')
            contactus=Contact(name=name,phone=phone,email=email,message=message)
            contactus.save()
            messages.success(request, "Message was succesfully")

        except:
            contact=request.POST.get('contact')
            if Phone_Number.objects.filter(phone=contact).exists:
                messages.error(request, "Your mobile number is already exsist.")
            else:
                callback=Phone_Number(phone=contact)
                callback.save()
                messages.success(request, "Your mobile number was saved.")


    return render(request,'home.html')


import json

@login_required(login_url="/login")
def inventory(request):
    

    products=Product.objects.all()
    quantites=0
    sumquantites=0
    sumtotal=0
    sumcost=0
    sumqtyprice=0
    subcost=0
    
    
    for i in products:
        sumquantites=sumquantites+i.quantity
        sumtotal=sumtotal+i.price
        sumcost=sumcost+i.buy_price
        sumqtyprice=sumqtyprice+i.total
        subcost=subcost+i.totalcost
    total=sumtotal
    quantites=sumquantites
    totalcost=sumcost
    subtotal=sumqtyprice
    finalcost=subcost

    if request.method=='POST':
        name=request.POST.get('product')
        quantity=int(request.POST.get('quantity'))
        price=int(request.POST.get('price'))
        cost=int(request.POST.get('cost'))
        product=Product(name=name,quantity=quantity,price=price,buy_price=cost)
        product.save()
        messages.success(request, "Product succesfully added")
    return render(request,'index.html',{'products':products,'quantites':quantites,'total':total,'totalcost':totalcost,'subtotal':subtotal,'finalcost':finalcost})

@login_required(login_url="/login")
def deleteproduct(request,id):
    product=Product.objects.filter(id=id)
    product.delete()
    messages.success(request, "Product has been deleted succesfully.")
    return redirect ('/inventory')

@login_required(login_url="/login")
def updateproduct(request,id):
    product=get_object_or_404(Product,id=id)
    name=request.POST.get('product')
    product.name=name
    quantity=int(request.POST.get('quantity'))
    product.quantity=quantity
    price=int(request.POST.get('price'))
    product.price=price
    cost=int(request.POST.get('cost'))
    product.buy_price=cost
    product.save()
    messages.success(request, "Product has been updated succesfully.")
    return redirect('/inventory')

@login_required(login_url="/login")
def dashboard(request):
    
    sales=Invoice.objects.all()
    customers=Customer.objects.all()
    products=Product.objects.all()
    ledgers=Ledger.objects.all()
    quantites=0
    sumquantites=0
    sumtotal=0
    sumcost=0
    sumqtyprice=0
    subcost=0
    totalsold=0
    paidtotal=0
    duetotal=0
    salesworth=0
    totalbalance=0
    allbalance=0
    

    
    
    
    curentyear=datetime.datetime.now().year
    if request.GET.get('year') is not None:
        
        curentyear=request.GET.get('year')

    curentmonth=datetime.datetime.now().month
    if request.GET.get('month') is not None:
        
        curentmonth=request.GET.get('month')
    print(curentmonth)
    
    todayt=len(ledgers.filter(date__day=datetime.datetime.now().day))
    montht=len(ledgers.filter(date__month=datetime.datetime.now().month))
    salemonth=len(sales.filter(date__month=datetime.datetime.now().month))
    
    for ledger in ledgers:
        totalbalance=totalbalance + (round(int(float(ledger.add))))-(round(int(float(ledger.remove))))
        allbalance=allbalance + (round(int(float(ledger.add)))) +(round(int(float(ledger.due))))-(round(int(float(ledger.remove))))
    balance=totalbalance
    tlbalance=allbalance


    for worth in sales.filter(date__month=datetime.datetime.now().month):
        salesworth=salesworth+round(int(float(worth.total)))
    
    totalworth=salesworth
    for sale in sales:
        totalsold=totalsold + round(int(float(sale.total)))
        paidtotal=paidtotal+(round(int(float(sale.paid_amt))))
        duetotal=duetotal+round(int(float(sale.due_amt)))
    salesdue=sales.filter(invoice_status='Due')
    totaldue=0

    months=[1,2,3,4,5,6,7,8,9,10,11,12]

    monthscale=0
    mscale=[]
    costscale=[]
    monthcost=0
    productsales=[]
    productsale=0
    invoices=Invoice_item.objects.all()

    for invoiceprod in products:

        for invoice in invoices.filter(product=invoiceprod,date__year=curentyear,date__month=curentmonth):
            productsale=productsale+int(invoice.quantity)
        productsales.append(productsale)
        productsale=0



    for month in months:
        for prod in invoices.filter(date__month=month,date__year=curentyear):
               
               monthcost=monthcost+(int(prod.product.buy_price)*int(prod.quantity))
               print(monthcost)
        costscale.append(monthcost)
        monthcost=0
        
        for sale in Invoice.objects.filter(date__month=month,date__year=curentyear):
            

            monthscale=monthscale+round(int(float(sale.total)))
            
             
        mscale.append(monthscale)
        monthscale=0
        
    salescale=mscale
    cscale=costscale
    
    monthlyscale=costscale
    profit=[]
    for i in range(len(salescale)):
       profit.append(salescale[i] - cscale[i])
    totalprofit=0
    for i in profit:
        totalprofit=totalprofit+i
    alltotalcost=0
    for i in monthlyscale:
        alltotalcost=alltotalcost+i
    allmonthcost=alltotalcost
    yearsale=0
    for i in mscale:
        yearsale=yearsale+i
    yearsales=yearsale





    
    


    daydue=salesdue.filter(date__day=datetime.datetime.now().day,date__month=datetime.datetime.now().month,date__year=datetime.datetime.now().year)
    
    monthdue=salesdue.filter(date__month=datetime.datetime.now().month)
    yeardue=salesdue.filter(date__year=datetime.datetime.now().year)
    
    for due in salesdue:
        totaldue=totaldue+int(due.due_amt)
    dueworth=totaldue


    totalsales=totalsold
    duesales=duetotal
    paidsales=paidtotal
    for i in products:
        sumquantites=sumquantites+i.quantity
        sumtotal=sumtotal+i.price
        sumcost=sumcost+i.buy_price
        sumqtyprice=sumqtyprice+i.total
        subcost=subcost+i.totalcost
    total=sumtotal
    quantites=sumquantites
    totalcost=sumcost
    subtotal=sumqtyprice
    finalcost=subcost
    
    outstock=len(products.filter(quantity=0))
    warn=len(Product.objects.filter(quantity__lte=10))
    if warn >= 10:
        messages.error(request, f"({warn}) products are of low stock units!!!")
    if outstock > 0:
        messages.error(request, f"({outstock}) products are out-of-stock!!!")
   
    print(productsales)
    return render(request,'dash.html',{'curentyear':curentyear,'curentmonth':curentmonth,'productsales':productsales,'yearsales':yearsales, 'allmonthcost':allmonthcost, 'totalprofit':totalprofit,'profit':profit,'monthlyscale':monthlyscale, 'cscale':cscale, 'salescale':salescale,'daydue':daydue,'yeardue':yeardue, 'monthdue':monthdue,'dueworth':dueworth,'salesdue':salesdue, 'todayt':todayt,'montht':montht, 'totalbalance':tlbalance, 'balance':balance,'totalworth':totalworth, 'salemonth':salemonth, 'outstock':outstock, 'duesales':duesales,'paidsales':paidsales,'totalsales':totalsales,'sales':sales,'products':products,'customers':customers,'quantites':quantites,'total':total,'totalcost':totalcost,'subtotal':subtotal,'finalcost':finalcost})

@login_required(login_url="/login")
def invoice(request):
   
    products=Product.objects.all().exclude(quantity = 0)
    customers=Customer.objects.all()

    try :
        invoice=int(Invoice.objects.all().order_by('-id')[0].id)
    except:
        invoice=0
    
        
    try:
      customer=get_object_or_404(Customer,id=int(request.session['customer']))
      return render(request,'invoice.html',{ 'products':products,'invoice':invoice+1 ,'customers':customers,'customer':customer})
    except:
       return render(request,'invoice.html',{  'products':products,'invoice':invoice+1 ,'customers':customers})


@login_required(login_url="/login")
def cleardue(request,po_no):
    due=int(request.POST.get('due'))
    dueobj=get_object_or_404(Invoice,po_number=po_no)
    invoiceitem=Invoice_item.objects.filter(po_number=po_no)
    invoice=Invoice.objects.filter(po_number=po_no)
    total=round(int(float(dueobj.paid_amt)))
    ledger=Ledger.objects.filter(po_number=po_no)
    if due == int(dueobj.due_amt):
        paid=due+total
        invoice.update(paid_amt=paid,due_amt=0,invoice_status="Paid")
        ledger.update(add=paid,due=0,status="Add")
        invoiceitem.update(invoice_status="Paid")
        messages.success(request, f"Due is now cleared for Invoice {po_no}.")
       
        return redirect(f'/invoice/{po_no}/')
    else:
        
        if int(dueobj.due_amt) > due:
            paid=due+total
            stilldue=int(dueobj.due_amt)-due
            invoice.update(paid_amt=paid,due_amt=stilldue,invoice_status="Due")
            ledger.update(add=paid,due=stilldue,status="Due")
            messages.success(request, f"Due is not cleared for Invoice {po_no}.")
            
            return redirect(f'/invoice/{po_no}/')
        else:
            paid=due+total
            stilldue=due-int(dueobj.due_amt)
            invoice.update(paid_amt=paid,due_amt=stilldue,invoice_status="Due")
            ledger.update(add=paid,due=stilldue,status="Due")
            messages.success(request, f"Due is now cleared for Invoice {po_no}.")
            
            return redirect(f'/invoice/{po_no}/')

       
    return redirect(f'/invoice/{po_no}/')

    

def invoicepdf(request,po_no):
    invoice=get_object_or_404(Invoice,po_number=po_no)
    data=f'http://192.168.31.224:8000/sales?id={invoice.invoice_id}'
    img = make(data)
    img_name = 'qr' + str(invoice.po_number) + '.png'
    img.save('static/images/' + img_name )
    return render(request,'pdf.html',{'invoice':invoice,'img_name': img_name})


@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("invoice")

@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("invoice")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("invoice")

def updateinvoice(request, id):
    qty=request.POST.get('quantity')
    total=request.POST.get('price')
    cart = Cart(request)
    product = Product.objects.get(id=id)
    print(product)
    cart.setquantity(product=product,quantity=int(qty),price=int(total))
    messages.success(request, f"Invoice is updated")
   
    return redirect("invoice")



@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("invoice")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("invoice")

def addcustomer(request,id):
    request.session['customer']=str(id)
    return redirect('invoice')



def createcustomer(request):
    if request.method=="POST":
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        whatsapp=request.POST.get('whatsapp')
        gst=request.POST.get('gst')
        address=request.POST.get('address')
        url=request.POST.get('url')
        
        
        customer=Customer(name=name,phone=phone,email=email,whatsapp=whatsapp,gst_no=gst,address=address)

        if Customer.objects.filter(phone=phone).exists():
          ucustomer=Customer.objects.filter(phone=phone)
          ucustomer.update(name=name)
          ucustomer.update(email=email)
          ucustomer.update(whatsapp=whatsapp)
          ucustomer.update(gst_no=gst)
          ucustomer.update(address=address)
          ucustomer.update(phone=phone)
          messages.success(request, f"Customer is updated {name}")
          return redirect(f'{url}')
        else:
          customer.save()
          messages.success(request, f"New customer is created {name}")
          return redirect(f'{url}')


def generateinvoice(request):
    uid=uuid.uuid4()
    print(uid)
    cart=request.session.get('cart')
    quantity=int(request.POST.get('items'))
    po_no=request.POST.get('po')
    invoiceno=request.POST.get('invoiceno')
    subtotal=int(float(request.POST.get('invoicesubtotal')))
    discount=int(float(request.POST.get('discountint')))
    tax=int(float(request.POST.get('invoicetax')))
    total=int(float(request.POST.get('invoicetotal')))
    paid=int(float(request.POST.get('paid')))
    due=int(float(request.POST.get('due')))
    print(total,paid)

    customer=get_object_or_404(Customer,id=int(request.session['customer']))
    invoice=Invoice(invoice_no=invoiceno,po_number=po_no,customer=customer,address=customer.address,quantity=quantity,subtotal=subtotal,discount=discount,tax=tax,total=total,due_amt=due,paid_amt=paid,invoice_id=uid)
    invoice.save()
    if round(int(due))==0:
        Invoice.objects.filter(invoice_id=uid).update(invoice_status='Paid')
        ledger=Ledger(invoice_no=invoiceno,customer=customer,po_number=po_no,user=request.user,add=paid,due=due,remove=0,purpose='Purchase',status='Add')
        ledger.save()
    if round(int(due))>0:
        Invoice.objects.filter(invoice_id=uid).update(due_amt=due,invoice_status='Due')
        ledger=Ledger(invoice_no=invoiceno,customer=customer,po_number=po_no,user=request.user,add=paid,due=due,remove=0,purpose='Purchase',status='Due')
        ledger.save()

    for i in cart:
        
        id=cart[i]['product_id']
        price=cart[i]['price']
        quantity=cart[i]['quantity']
        addproduct=get_object_or_404(Product,id=int(id))
        get_object_or_404(Invoice,invoice_id=uid).products.add(addproduct)
        Product.objects.filter(id=int(id)).update(quantity=int(addproduct.quantity)-int(quantity))
        Item=Invoice_item(product=Product.objects.get(id=int(id)),po_number=po_no,price=price,total=total,quantity=quantity,invoice_no=invoiceno,invoice_id=uid,customer=customer)
        Item.save()
        get_object_or_404(Invoice,invoice_id=uid).invoice_items.add((Item))
        if round(int(due))>0:
          Invoice_item.objects.filter(invoice_id=uid).update(invoice_status='Due')
          
        if round(int(due))==0:
          Invoice_item.objects.filter(invoice_id=uid).update(invoice_status='Paid')

    cart_clear(request)
    
        
    messages.success(request, f"New invoice is created {po_no}.")

    return redirect('invoice')

@login_required(login_url="/login")
def sales(request):
    

    if request.method== "GET":
        sort=request.GET.get('sort','')
        po_no=(request.GET.get('pono',''))
        id=(request.GET.get('id',''))
        if sort=='due':
            sales=Invoice.objects.filter(invoice_status="Due")
        elif sort =='paid':
            sales=Invoice.objects.filter(invoice_status="Paid")
        elif sort == 'new':
            sales=Invoice.objects.all().order_by('-id')
        elif sort == 'old':
            sales=Invoice.objects.all().order_by('id')
        elif sort == 'low':
            sales=Invoice.objects.all().order_by('total')
        elif sort == 'high':
            sales=Invoice.objects.all().order_by('-total')
        elif po_no:
            sales=Invoice.objects.filter(po_number__icontains=po_no)
        elif id:
            sales=Invoice.objects.filter(invoice_id=id)
        else:
            sales=Invoice.objects.all()
    
   
        
    return render(request,'sales.html',{'sales':sales})

@login_required(login_url="/login")
def addmoney(request):
    if request.method=='POST':
        add=request.POST.get('add')
        
        purpose=request.POST.get('purpose')
        if int(add) > 0 :
          ledger=Ledger(add=round(int(add)),remove=0,due=0,status='Add',user=request.user,purpose=purpose)
          ledger.save()
          messages.success(request, f"₹ {round(int(add))} is added successfully by {request.user.username} for {purpose}.")
          
        return redirect('ledger')
    
@login_required(login_url="/login")
def removemoney(request):
    if request.method=='POST':
        
        withdraw=request.POST.get('withdraw')
        purpose=request.POST.get('purpose')
        total=request.POST.get('total')
        if int(withdraw) > 0 and int(withdraw) < int(total):
          ledger=Ledger(add=0,remove=round(int(withdraw)),due=0,status='Widthrawl',user=request.user,purpose=purpose)
          messages.success(request, f"Money is withdrawl successfully")
          ledger.save()
        
       
        return redirect('ledger')

@login_required(login_url="/login")
def ledger(request):
   
    
    if request.method== "GET":
        sort=request.GET.get('sort','')
        if sort=='due':
            ledgers=Ledger.objects.filter(status="Due")
        elif sort=='remove':
            ledgers=Ledger.objects.filter(status="Widthrawl")
        elif sort =='paid':
            ledgers=Ledger.objects.filter(status="Add")
        elif sort == 'new':
            ledgers=Ledger.objects.all().order_by('-id')
        elif sort == 'old':
            ledgers=Ledger.objects.all().order_by('id')
        elif sort == 'low':
            ledgers=Ledger.objects.all().order_by('add')
        elif sort == 'high':
            ledgers=Ledger.objects.all().order_by('-add')
        else:
            ledgers=Ledger.objects.all()
    totalbalance=0
    allbalance=0
    ledgerss=Ledger.objects.all()
    for ledgerr in ledgerss:
        totalbalance=totalbalance + (round(int(float(ledgerr.add))))-(round(int(float(ledgerr.remove))))
        allbalance=allbalance + (round(int(float(ledgerr.add)))) +(round(int(float(ledgerr.due))))-(round(int(float(ledgerr.remove))))
    balance=totalbalance
    tlbalance=allbalance
    

    dues=len(ledgerss.filter(status="Due"))
    return render(request,'ledger.html',{'dues':dues,'balance':balance,'tlbalance':tlbalance,'ledgers':ledgers})

def loginhandle(request):
   next=request.GET.get('next')
   if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        nextpage=request.POST.get('next','')
        user=authenticate(username= username, password= password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            if nextpage:
                try:
                   return redirect(f'{nextpage}')
                except:
                   return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/login")
   return render(request,'login.html',{'next':next})

@login_required(login_url='/login')
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')