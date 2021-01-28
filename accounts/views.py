from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models  import Group
from  django.contrib  import messages
from django.contrib .auth.decorators import  login_required

#create your views here
from  .models import *
from.forms import orderForm, CreateUserForm
from .filters import  OrderFilter
# from.decorators import unauthenticated_user,  allowed_users,   admin_only





# @unauthenticated_user
def registrationPage(request):
    form = CreateUserForm()
    if  request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get(name='customer')
                user.groups.add(group)
                Customer.objects.create(
                    user = user,
                )
                messages.success(request, 'Account was created  successfully ' + username )
                
                login(request, user)
                return redirect('home')

    context ={'form':form}
    return render(request, 'accounts/registration.html', context)

# @unauthenticated_user
def loginPage(request):
    if request.method =='POST':
         form=AuthenticationForm(data= request.POST)   
         if form.is_valid():
             user = form.get_user()
             login(request, user)
             return redirect('home')

    else:
        messages.success(request,  'Username OR password is incorrect')
        form=AuthenticationForm()   
       
    return render(request, 'accounts/login.html', {'form':form})


def  logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url ='login')
# @admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'customers': customers,
               'total_customers': total_customers,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending}
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url ='login')
# @allowed_users(allowed_roles=['admin'])
def products(request):
    products = Products.objects.all()[:10]
    context = {'products': products}
    return render(request,'accounts/products.html', context)

def userpage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS:',orders)

    context={'orders':orders,  'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending}
    return render(request, 'accounts/user.html',context)



@login_required(login_url ='login')
# @allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter =  OrderFilter(request.GET , queryset = orders)
    orders  = myFilter.qs 
    context = {'customer': customer, 'orders': orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url ='login')
# @allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('products','status'))
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(instance=customer)
    # form = orderForm(initial={'customer':customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'accounts/order_form.html',context)

@login_required(login_url ='login')
# @allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = orderForm(instance=order)
    if request.method == 'POST':
        form = orderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url ='login')
# @allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context ={'items': order}
    return render(request, 'accounts/delete.html',context)