from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    CATEGORY =(
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor')
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    description = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name_plural='Products'

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS=(
        ('Pending','pending'),
        ('out for delivery','out for delivery'),
        ('Delivered','Delivered')
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    products = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=222, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    note =  models.CharField(max_length=222, null=True)

    def __str__(self):
        return self.products.name

