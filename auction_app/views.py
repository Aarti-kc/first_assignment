import datetime
from django.contrib.auth.models import AbstractUser
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from auction_app.models import *
from django.shortcuts import get_list_or_404, get_object_or_404

# Create your views here.

def index(request):
    product=Products.objects.all()
    user=request.user.id
    all_objects=Watchlist.objects.filter(user=user)
  #  print(watchlists)
    context={
        'product':product,
        'watchlist_count':all_objects.values_list('item').count(),
        'user':user,
    }
    return render(request,"index.html",context)

class ProductSection:


    def login_now(request):
        return render(request,'login_user.html')

    def login_user(request):
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.success(request, ("There Was An Error Logging In, Try Again..."))	
                return redirect('login_now')	


        else:
            return render(request, 'login_user.html', {})

     
    def logout_user(request):
        logout(request)
        messages.success(request, ("You Were Logged Out!"))
        return redirect('index')

    
    def add_product(request):
        user=request.user
        all_objects=Watchlist.objects.filter(user=user.id)
        if user.is_authenticated:
            return render(request,'add_product.html',{'watchlist_count':all_objects.values_list('item').count(),'user':user.id})
        else:
            return HttpResponseRedirect('/login')


    def add_product_save(request):
        if request.method!="POST":
            return HttpResponseRedirect("/add_product")
        else:
            pro_name=request.POST.get("pro_name")
            price=request.POST.get("price")
            about=request.POST.get("about")
        #    img=request.POST.field("pro_img")
            print(pro_name)
            try:
                new_pro=Products(product_name=pro_name,product_price=price,description=about)
                new_pro.save()
                messages.success(request, "New product has been Added!")
                return HttpResponseRedirect("/add_product")
            except:
                messages.error(request, "Something went wrong:/")
                return HttpResponseRedirect("/add_product")

    def details(request,id):
        user=request.user
        if user.is_authenticated:
            print(user)
            product=Products.objects.get(id=id)
            bid_count=Bidding.objects.filter(product_id=id).count()
            all_bids=Bidding.objects.filter(product_id=id)
            all_objects=Watchlist.objects.filter(user=user)
            return render(request,'expand_details.html',{'product':product,'bid':bid_count,'all_bid':all_bids,'watchlist_count':all_objects.values_list('item').count(),'user':user})
        else:
            return HttpResponseRedirect('/login')
            

    def bidding(request,pro_id):
        print(request.user.id)
        user=request.user.id
        all_objects=Watchlist.objects.filter(user=user)
        if request.user.is_authenticated:
            pro=Products.objects.get(id=pro_id)
            return render(request,'add_bid.html',{'product':pro,'watchlist_count':all_objects.values_list('item').count(),'user':user})
        else:
            messages.info(request, "Something went worng:/")
            return HttpResponseRedirect('/login')

    def add_product_bidding_save(request):
        if request.method!='POST':
            return HttpResponseRedirect("/")
        else:
            user_id=request.user
            if user_id.is_authenticated:
                user=User.objects.get(id=user_id.id)
            else:
                print("No user")
            pro_id=request.POST.get('pro_id')
            pro=Products.objects.get(id=pro_id)
            new_price=request.POST.get('new_price')
            try:
                new_bid=Bidding(user_id=user,product_id=pro,new_price=new_price)
                new_bid.save()
                print(new_bid)
                messages.success(request,'New Bid Added!')
                return HttpResponseRedirect('bidding/'+pro_id)
            except:
                messages.error(request,'Oops.. something went wrong!')
                return HttpResponseRedirect('bidding/'+pro_id)


    def register_user(request):
        return render(request,'register_user.html')

    def register_user_save(request):
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            new_user=User(username=username,password=password)
            new_user.set_password(password)
            new_user.email=request.POST.get('email')
            new_user.is_superuser=True
            new_user.is_staff=True
            new_user.save()
            messages.success(request, ("Registration Successful!"))
            return redirect('index')
        else:
            messages.error(request, ("Registration Unsuccessful!"))
            return redirect('register_user')

    def watchlist_add(request, product_id):
        if request.user.is_authenticated:
            item_to_save = get_object_or_404(Products, pk=product_id)
            user=request.user
            if Watchlist.objects.filter(user=request.user, item=product_id).exists():
                messages.add_message(request, messages.ERROR, "You already have it in your watchlist.")
                return HttpResponseRedirect(reverse("index"))
            user_list, created = Watchlist.objects.get_or_create(user=request.user)
            user_list.item.add(item_to_save)
            messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
            return HttpResponseRedirect('/all_watchlist',{'user':user})
        else:
            return HttpResponseRedirect('/login')

    def all_watchlist(request):
        user=request.user.id
      
        all_objects=Watchlist.objects.filter(user=user).values_list('item')
        #print(all_objects)
        all_products=Products.objects.all().values_list('id')
        #print(all_products)
        watchlist_item=[]
        not_listed=[]
        for i in all_products:
            if i in all_objects:
                watchlist_item.append(Products.objects.get(id=i[0]))
            else:
                not_listed.append(Products.objects.get(id=i[0]))
        print(watchlist_item)
        return render(request,'all_watchlist.html',{'all_items':watchlist_item,'not_listed':not_listed,'watchlist_count':all_objects.values_list('item').count(),'user':user})
        
    def remove_from_watchlist(request,pro_id):
        user=request.user.id
        all_objects=Watchlist.objects.get(user=user).item
        product_to_remove=Products.objects.get(id=pro_id)
        all_objects.remove(product_to_remove)
        print("In products: ")
        print(product_to_remove)
        if all_objects.count()==0:
            obj=Watchlist.objects.get(user=user)
            obj.delete()
        return HttpResponseRedirect('/all_watchlist')