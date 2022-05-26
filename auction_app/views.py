import datetime

from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from auction_app.models import Products
from .serializers import *

# Create your views here.

def logout_user(request):
    pass

def index(request):
    product=Products.objects.all()
    context={
        'product':product,
    }
    return render(request,"index.html",context)


def add_product(request):
    return render(request,'add_product.html')


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
            messages.error(request, "Something went worng:/")
            return HttpResponseRedirect("/add_product")

class add_product_save(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        all_pro=Products.objects.all()
        serialize_data=ProductsSerializer(all_pro,many=True)
        if all_pro is not None:
            return Response(serialize_data.data,status=status.HTTP_200_OK)
        else:
            return Response({'error': ['Not Data Found.']},status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        pro_name=request.POST.get("pro_name")
        price=request.POST.get("price")
        about=request.POST.get("about")
        print(request.data)
        #new_pro=Products(product_name=pro_name,product_price=price,description=about)
        print(new_pro)
        serialize_data=ProductsSerializer(data=request.data)
        if pro_name is None:
            return Response({'pro_name': ['This field is required.']},
                            status=status.HTTP_400_BAD_REQUEST)
        if price is None:
            return Response({'price': ['This field is required.']},
                            status=status.HTTP_400_BAD_REQUEST)
        if about is None:
            return Response({'about': ['This field is required.']},
                            status=status.HTTP_400_BAD_REQUEST)
        if serialize_data.is_valid():
            new_pro.save()
            serialize_data.save()
            return Response({"status": "success", "data": serialize_data.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serialize_data.errors}, status=status.HTTP_400_BAD_REQUEST)
       