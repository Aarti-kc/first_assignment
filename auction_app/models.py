from django.db import models

# Create your models here.

class User(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=255,default="@",null=False)
    name=models.CharField(max_length=255,default="")
    email=models.CharField(max_length=255,default="",null=False)
    password=models.CharField(max_length=255,default="",null=False)
    gender=models.CharField(max_length=100,default="")

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()



class Products(models.Model):
    id=models.AutoField(primary_key=True)
    pro_img= models.ImageField(upload_to='uploads/', height_field=None, width_field=None,default="static/default.png")
    product_name=models.CharField(max_length=255,default="")
    product_price=models.FloatField(max_length=100,null=False,default='0')
    description=models.CharField(max_length=255,default="")
    product_quantity = models.IntegerField(default=1)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Bidding(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE,default=1)
    new_price=models.CharField(max_length=100,null=False,default='0')

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Comments(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default="")
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE,default=1)
    title=models.CharField(max_length=100,null=False,default="")
    comment=models.CharField(max_length=200,null=False,default='')

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()