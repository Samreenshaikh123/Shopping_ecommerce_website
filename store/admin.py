from django.contrib import admin

# Register your models here.
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.cart import Cart
from .models.order import OrderDetails
from .models.contact import Contact



class AdminProduct(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category','description']


class AdminCustomer(admin.ModelAdmin):
    list_display = ['id', 'name', 'password']
class AdminCart(admin.ModelAdmin):
    list_display = ['id', 'password', 'product', 'image', 'price']

class Adminorder(admin.ModelAdmin):
    list_display = ['id', 'user', 'product_name', 'qty', 'image', 'price', 'status', 'ordered_date']

class AdminContact(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'content']

class AdminProfile(admin.ModelAdmin):
    list_display = ['id','user','images']



admin.site.register(Product, AdminProduct)
admin.site.register(Category)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Cart, AdminCart)
admin.site.register(OrderDetails, Adminorder)
admin.site.register(Contact, AdminContact)


admin.site.site_header = "Paradise Mattress"
admin.site.index_title = "Paradise Mattress Administration"
admin.site.site_title = "Paradise Mattress Admin"
