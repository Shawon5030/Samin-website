from django.contrib import admin

from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced,
    Trasnjection
)

# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id', 'user', 'name', 'division','district','thana','villorroad','zipcode']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display =['id', 'title','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','total_amount','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer','product','quantity','ordered_date','status']


from .models import SiteInfo

@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'logo_name', 'active')
    list_editable = ('active',)
    
    
admin.site.register(Trasnjection)