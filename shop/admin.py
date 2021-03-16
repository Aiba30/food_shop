from django.contrib import admin
from .models import Dish,Drink,Cart,CartContent

admin.site.register(CartContent)
# admin.site.register(Cart)
@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['id','title','type','description']

@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ['id','title','type','description']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_key','user','total_cost']