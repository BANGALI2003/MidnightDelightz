from django.contrib import admin
from .models import *
from django.contrib.admin.models import LogEntry


# Register your models here.
admin.site.site_header="Midnight Delights"
admin.site.index_title="Welcome To Midnight Delights"
admin.site.site_title="Midnight Delights"
class Display_Area(admin.ModelAdmin):
    list_display=['Pincode','Name']
    list_per_page=5
class display_cart(admin.ModelAdmin):
    list_display = ['food_name', 'quantity', 'customer_name', 'orderid']
class display_Restaurant(admin.ModelAdmin):
    list_display = ['id','Name','Address','OpenAt','CloseAt','OwnerName','Contact']
class Display_Address(admin.ModelAdmin):
    list_display=['id','Receiver_Name','Receiver_Contact','Landmark','Address_type','Area_Pincode','Customer_name']
    list_per_page = 5
    list_filter=['Receiver_Name']
class Display_Offers(admin.ModelAdmin):
    list_display=['id','Description','Amount','Coupon_On_Food','Coupon_On_Order','Start_Date','End_Date']
    list_per_page = 5
    list_filter = ['Start_Date','End_Date','Coupon_On_Food','Coupon_On_Order']
class Display_Customer(admin.ModelAdmin):
    list_display=['id','First_Name','Last_Name','Contact','Email','cus_Image']
    list_per_page = 5
    list_filter=['First_Name']
class Display_FoodCategory(admin.ModelAdmin):
    list_display=['id','Name','category_img','Subcategory']
    list_per_page = 5
    list_filter=['Name']
class Display_FoodItem(admin.ModelAdmin):
    list_display=['id','Name','Description','Price','Food_Image','Jain_Food','Category','Offer_Name']
    list_per_page = 5
    list_filter=['Name','Price','Jain_Food']
class Display_SaleOrder(admin.ModelAdmin):
    list_display=['id','Date','IsCancel','Payment_Status','address','Totalammount','Payment_Type','Customer_Name','location']
    list_per_page = 5
    list_filter=['Customer_Name']

class Display_SaleOrderDetail(admin.ModelAdmin):
    list_display=['id','Quantity','SaleOrder_Id','Food_Item_Name']
    list_per_page = 5
    list_filter=['Food_Item_Name']
class Display_Membership(admin.ModelAdmin):
    list_display=['id','Amount','Start_Date','End_Date','Customer_Name']
    list_per_page = 5
    list_filter=['Customer_Name','Start_Date','End_Date']
class Display_Payment(admin.ModelAdmin):
    list_display=['id','Date','Customer_Name','SaleOrder_Id','Membership_Id']
    list_per_page = 5
    list_filter=['Customer_Name','Date']
class Display_Feedback(admin.ModelAdmin):
    list_display=['id','Rating','Date','Description','Food_Item_Name','Customer_Name','SaleOrder_Id']
    list_per_page = 5
    list_filter=['Food_Item_Name','Rating','Customer_Name']
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message']
    list_filter = ['user','object_id','action_time']
class display_order_status(admin.ModelAdmin):
    list_display = ['id','date_time','Status','SaleOrder_Id']
admin.site.register(Area,Display_Area)
admin.site.register(Address,Display_Address)
admin.site.register(Customer,Display_Customer)
admin.site.register(Offers,Display_Offers)
admin.site.register(Food_Category,Display_FoodCategory)
admin.site.register(Food_Item,Display_FoodItem)
admin.site.register(SaleOrder,Display_SaleOrder)
admin.site.register(SaleOrder_Detail,Display_SaleOrderDetail)
admin.site.register(Membership,Display_Membership)
admin.site.register(Payment,Display_Payment)
admin.site.register(Feedback,Display_Feedback)
admin.site.register(Restaurant,display_Restaurant)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(cart, display_cart)
admin.site.register(Order_Status,display_order_status)