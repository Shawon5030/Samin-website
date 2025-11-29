from django.db import models
from django.contrib.auth.models import User
# Create your models here.
DIVISION_CHOICES = (
    ('Dhaka','Dhaka'),
    ('Rangpur','Rangpur'),
    ('Rajshahi','Rajshahi'),
    ('Khulna','Khulna'),
    ('Barishal','Barishal'),
    ('Chattogram','Chattogram'),
    ('Mymenshing','Mymenshing'),
    ('Sylhet','Sylhet'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    division = models.CharField(choices=DIVISION_CHOICES, max_length=50)
    district = models.CharField(max_length=200)
    thana = models.CharField(max_length=50)
    villorroad = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    

    def __str__(self):
        return str(self.id)
    


CATEGORY_CHOICES = (
    ('L', 'Lehenga'),
    ('S', 'Saree'),
    ('GP', 'Gents Pant'),
    ('BK', 'Borkha'),
    ('BF', 'Baby Fashion'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.id)


    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price



STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the Way', 'On the Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='Pending')
    trasnjection_id = models.CharField(max_length=100, blank=True, null=True)
    payment_amount = models.IntegerField(blank=True,null=True)
    payment_method = models.CharField(blank=True,null=True,max_length=20)
    date = models.DateField(blank=True,null=True)



# models.py
from django.db import models

class SiteInfo(models.Model):
    logo_name = models.CharField(max_length=100, default="Shop")
    logo_image = models.ImageField(upload_to='site/logo/',blank=True, null=True)
    site_name = models.CharField(max_length=200, default="shop E-Commerce")
    company_name = models.CharField(max_length=200, default="shop Technologies")
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Site Information"
        verbose_name_plural = "Site Information"
        
    def __str__(self):
        return self.site_name
    
class Trasnjection(models.Model):
    t_id = models.CharField(max_length=100)
    
    
import uuid
class License(models.Model):
    name = models.CharField(max_length=100)
    license_key = models.CharField(max_length=100, unique=True, blank=True)
    expiry_date = models.DateTimeField() 

    def save(self, *args, **kwargs):
        if not self.license_key:
            # Generate unique license key
            self.license_key = uuid.uuid4().hex.upper()[0:20]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.license_key}"
    
    
from django.contrib import admin
from .models import License
@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ("name", "license_key", "expiry_date")
    search_fields = ("name", "license_key")
    list_filter = ("expiry_date",)
    ordering = ("-expiry_date",)

    readonly_fields = ("license_key",)

    fieldsets = (
        ("License Information", {
            "fields": ("name", "expiry_date", "license_key")
        }),
    )

