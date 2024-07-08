from django.db import models
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator,MinValueValidator
from datetime import timedelta, timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone

# Create your models here.
address_list=(
    ('1','Home'),
    ('2','Office'),
    ('3','Other')
)

payment_list=(
    ('1','Cash On Delivery'),
    ('2','UPI'),
    ('3','Card')
)
order_status=(
('1','Waiting for Accept'),
    ('2','Accepted'),
    ('3','Start Cooking'),
('4','Packaged'),
    ('5','Ready for Delivery'),
    ('6','Out for delivery'),
('7','Delivered'),
('8','Canceled'),
)

class Restaurant(models.Model):
    Name = models.CharField(default="MidNight Delights", max_length=25)
    Address = models.TextField(null=False)
    OpenAt = models.CharField(max_length=10)
    CloseAt = models.CharField(max_length=10)
    OwnerName = models.CharField(max_length=15)
    Contact = models.DecimalField(max_digits=10, decimal_places=0)

    def clean(self):
        # Check that the Name does not contain only numerics
        if self.Name.isdigit():
            raise ValidationError( 'Name should not contain only numerics.')

        # Check that the Address does not contain only numerics
        if self.Address.isdigit():
            raise ValidationError( 'Address should not contain only numerics.')

        super().clean()

class Area(models.Model):
    Pincode = models.DecimalField(max_digits=6, primary_key=True, decimal_places=0)
    Name = models.CharField(max_length=25, unique=True)
    Latitude = models.FloatField(null=False)
    Longitude = models.FloatField(null=False)

    def __str__(self):
        return self.Name

    def clean(self):
        # Check that the Name does not contain only digits
        if self.Name.isdigit():
            raise ValidationError('Name should not contain only digits.')
        super().clean()

class Customer(models.Model):
    First_Name=models.CharField(max_length=15)
    Last_Name=models.CharField(max_length=15,null=False)
    Contact=models.CharField(max_length=10,unique=True,null=False)
    Email=models.EmailField(unique=True,null=False)
    cus_Image=models.ImageField(upload_to='photos',null=True)
    def __str__(self):
        return self.First_Name
    def customer_img(self):
        return mark_safe('<img src="{}" width="50%">'.format(self.cus_Image.url))

    customer_img.allow_tags = True
    def clean(self):
        # Check that the Name does not contain only digits
        if self.First_Name.isdigit() or self.Last_Name.isdigit():
            raise ValidationError( 'Name should not contain only digits.')
        super().clean()

class Address(models.Model):
    Receiver_Name=models.CharField(max_length=15,null=False)
    Receiver_Contact=models.DecimalField(max_digits=10,decimal_places=0)
    Landmark=models.TextField(null=False)
    Address_type=models.CharField(max_length=6)
    Area_Pincode=models.ForeignKey(Area,on_delete=models.SET_NULL,to_field='Pincode',null=True)
    Customer_name=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.Landmark
    def clean(self):
        # Check that the Name does not contain only digits
        if self.Receiver_Name.isdigit():
            raise ValidationError( 'Name should not contain only digits.')

        super().clean()

class Offers(models.Model):
    Description = models.TextField(null=False, unique=True)
    Amount = models.IntegerField(validators=[MaxValueValidator(300)])
    Coupon_On_Food = models.BooleanField(default=False)
    Coupon_On_Order = models.BooleanField(default=False)
    Start_Date = models.DateField(null=False)
    End_Date = models.DateField(null=False)

    def __str__(self):
        return self.Description

    def clean(self):
        today = timezone.now().date()

        # Check if Start_Date is greater than or equal to today's date
        if self.Start_Date and self.Start_Date < today:
            raise ValidationError( 'Start date must be greater than or equal to today s date')

        # Check if End_Date is greater than Start_Date
        if self.Start_Date and self.End_Date and self.Start_Date >= self.End_Date:
            raise ValidationError( 'End date must be greater than the start date.')
        if self.Description.isdigit():
            raise ValidationError( 'Description should not contain only numerics.')

            # Check that the description has a length of 20
        if len(self.Description) < 20:
            raise ValidationError( 'Description must have a mre than of 20 characters.')

        super().clean()

def validate_image_extension(value):
    valid_extensions = ['jpg', 'jpeg', 'png']
    extension = value.name.split('.')[-1].lower()
    if extension not in valid_extensions:
        raise ValidationError('Only JPG and PNG files are allowed.')

class Food_Category(models.Model):
    Name = models.CharField(max_length=25, unique=True, null=True)
    Image = models.ImageField(upload_to='photos', validators=[validate_image_extension])
    Subcategory = models.ForeignKey('self', on_delete=models.SET_NULL, to_field='id', null=True, blank=True)

    def __str__(self):
        return self.Name

    def category_img(self):
        return mark_safe('<img src="{}" width="50%">'.format(self.Image.url))

    category_img.allow_tags = True

class Food_Item(models.Model):
    Name = models.CharField(max_length=40, unique=True)
    Description = models.TextField(null=False)
    Price = models.IntegerField(null=False)
    Food_Image = models.ImageField(upload_to='photos', null=False,validators=[validate_image_extension])
    Jain_Food = models.BooleanField(default=False)
    Category = models.ForeignKey('Food_Category', on_delete=models.SET_NULL, to_field='id', null=True)
    Offer_Name = models.ForeignKey('Offers', on_delete=models.SET_NULL, null=True, to_field='id')

    def __str__(self):
        return self.Name

    def Food_img(self):
        return mark_safe('<img src="{}" width="50%">'.format(self.Food_Image.url))

    Food_img.allow_tags = True

    def clean(self):
        # Check that the description does not contain only numerics
        if self.Description.isdigit():
            raise ValidationError( 'Description should not contain only numerics.')

        # Check that the description has a length of 20
        if len(self.Description) <= 20:
            raise ValidationError('Description must have a  of more than 20 characters.')

        super().clean()

class cart(models.Model):
    food_name = models.ForeignKey(Food_Item, on_delete=models.SET_NULL, null=True)
    customer_name = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True)
    totalprice = models.IntegerField(null=True)
    product_status = models.IntegerField(null=True)
    orderid = models.IntegerField(null=True)

class SaleOrder(models.Model):
    Date=models.DateTimeField(auto_now_add=True)
    IsCancel=models.BooleanField(default=False)
    Payment_Status=models.BooleanField(default=False)
    Payment_Type=models.CharField(max_length=30)
    Tax = models.FloatField(default=9.5, editable=False)
    Customer_Name=models.ForeignKey(Customer,on_delete=models.SET_NULL,to_field='id',null=True)
    Totalammount=models.IntegerField(default=0)
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    location=models.URLField(null=True,max_length=500)


class SaleOrder_Detail(models.Model):
    Quantity=models.IntegerField(validators=[MaxValueValidator(10)])
    SaleOrder_Id=models.ForeignKey(SaleOrder,on_delete=models.SET_NULL,to_field='id',null=True)
    Food_Item_Name=models.ForeignKey(Food_Item,on_delete=models.SET_NULL,to_field='id',null=True)

class Membership(models.Model):
    Amount = models.IntegerField(editable=False, default=499)
    Start_Date = models.DateField()
    End_Date = models.DateField(editable=False)
    Customer_Name = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, to_field='id')

    def save(self, *args, **kwargs):
        # Check if End_Date is not set before calculating
        if not self.End_Date:
            self.End_Date = self.Start_Date + timedelta(days=365)

        super().save(*args, **kwargs)

class Payment(models.Model):
    Date=models.DateField(auto_now_add=True)
    Customer_Name=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL,to_field='id')
    SaleOrder_Id=models.ForeignKey(SaleOrder,on_delete=models.SET_NULL,to_field='id',null=True)
    Membership_Id=models.ForeignKey(Membership,on_delete=models.SET_NULL,to_field='id',null=True)

class Feedback(models.Model):
    Rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    Date=models.DateField(auto_now_add=True)
    Description=models.TextField(null=False)
    Food_Item_Name = models.ForeignKey(Food_Item, on_delete=models.SET_NULL, to_field='id', null=True)
    Customer_Name = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, to_field='id')
    SaleOrder_Id = models.ForeignKey(SaleOrder, on_delete=models.SET_NULL, to_field='id', null=True)

class Order_Status(models.Model):
    date_time=models.DateTimeField(auto_now=True)
    Status=models.CharField(choices=order_status,max_length=30)
    SaleOrder_Id = models.ForeignKey(SaleOrder, on_delete=models.SET_NULL, to_field='id', null=True)

