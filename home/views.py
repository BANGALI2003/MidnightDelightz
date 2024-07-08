import random
from datetime import datetime, date
from django.db.models import QuerySet, Count, Sum
from .models import *
from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import *
from django.conf import settings
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from geopy.geocoders import Nominatim
import re
import json
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db.models import Q

otp_lst = []


def index(request):
    category_data = Food_Category.objects.all()
    product_data = Food_Item.objects.all()
    cart_count = cart.objects.count()
    context = {
        "categories": category_data,
        "products": product_data,
        "cart_count": cart_count
    }
    return render(request, "index.html", context=context)


def about(request):
    cart_count = cart.objects.count()
    context = {
        "cart_count": cart_count
    }
    return render(request, "about.html", context)


def geolocate(areacode):
    print("areacode", areacode)
    # query1=Area.objects.get(Pincode=areacode)
    # print(query1)
    geolocator = Nominatim(user_agent="home")
    location = geolocator.geocode(f"Ranip,Ahmedabad,Gujarat,{areacode}")
    lat = location.latitude
    long = location.longitude
    query1 = Area(Name="Ranip", Latitude=lat, Longitude=long, Pincode=areacode)
    query1.save()
    print(location.address)
    print((location.latitude, location.longitude))
    print(location.raw)


def genotp():
    otp = 0
    x = random.randint(1000, 9999)
    timestamp = datetime.now()
    if x in otp_lst:
        otp_lst.append(x)
    else:
        otp = x
        otp_lst.append(otp)
    return otp, timestamp


def login(request):
    return render(request, "login.html")


def register(request):
    query = Area.objects.all()
    context = {
        'area': query
    }
    return render(request, "register.html", context)


def send_otp(request):
    otp, timestamp = genotp()
    request.session["otp"] = otp
    request.session["otp_timestamp"] = timestamp.timestamp()
    print("otp is :", otp)
    email = request.session["useremail"]
    print(request.session["useremail"])
    subject = 'About Login...'
    message = (f'Hi ,your Login process is started  on Midnight delights and your otp is  otp is {otp}'
               f'Your Otp is valid for Five minutes only')
    email_from = 'nisargt1782@gmail.com'
    cus = [email]
    send_mail(subject, message, email_from, cus)
    return redirect("otp")


def save_data(request):
    if request.method == "POST":
        print("n")
        fname = request.POST.get("firstname")
        lname = request.POST.get("lastname")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        image = request.FILES.get('image')
        if fname == "" or fname.isnumeric() == True:
            messages.error(request, "First name is not valid")
            return render(request, "register.html")
        if lname == "" or lname.isnumeric() == True:
            messages.error(request, "Last name is not valid")
            return render(request, "register.html")
        if len(phone) != 10:
            messages.error(request, "Phone number is not valid")
            return render(request, "register.html")
        if phone.isnumeric() == False:
            messages.error(request, "phone number not contain characters")
            return render(request, "register.html")
        try:

            query = Customer.objects.get(Email=email)
        except:
            query = None
        if query is None:
            try:
                query2 = Customer.objects.get(Contact=phone)
            except:
                query2 = None
            if query2 is None:
                query3 = Customer(First_Name=fname, Last_Name=lname, Contact=phone, Email=email, cus_Image=image)
                query3.save()
                messages.success(request, "You have Succesfully registered on Midnight Delights")
                return render(request, "login.html")
            else:
                print("uc")
                messages.error(request, "User exists with that Conatct number")
                return render(request, "register.html")
        else:
            print("ue")
            messages.error(request, "User exists with that email")
            return render(request, "register.html")
    else:
        return redirect('register')


def otp(request):
    return render(request, "otp.html")


def validate_otp(request):
    if request.method == "POST":
        user_otp = int(request.POST.get("otp"))
        otp = int(request.session["otp"])
        email = request.session["useremail"]
        try:
            query = Customer.objects.get(Email=email)
        except:
            query = None

        timestamp = request.session.get("otp_timestamp", 0)
        current_timestamp = datetime.now().timestamp()
        if current_timestamp - timestamp <= 30:  # 30 seconds
            if otp == user_otp:
                request.session["username"] = query.First_Name
                request.session["useremail"] = query.Email
                request.session["userid"] = query.id
                request.session["userphone"] = query.Contact
                request.session.save()
                return redirect('index')
            else:
                messages.error(request, "OTP not matched")
                return redirect("otp")
        else:
            messages.error(request, "OTP has expired")
            return render(request, "otp.html")


def validate_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            query = Customer.objects.get(Email=email)
        except:
            query = None
        if query is not None:
            request.session["useremail"] = query.Email
            # request.session["username"] = query.First_Name
            # request.session["phone"]=query.Contact
            send_otp(request)
            return render(request, "otp.html")
        else:
            messages.error(request, "User not found!!")
    return redirect(login)


def areaget(request):
    return render(request, "areaget.html")


def get_area(request):
    geolocate(382480)


def cart_page(request):
    user1 = request.session['userid']
    if user1:
        print(user1)
        fetchcartdata = cart.objects.filter(customer_name=user1, product_status=1)
        carttotal = cart.objects.filter(customer_name=user1, product_status=1).aggregate(Sum('totalprice'))
        print(carttotal)
        request.session['carttotal'] = carttotal['totalprice__sum']
        request.session.save()
        fetchpid = cart.objects.filter(customer_name=user1, product_status=1).values('food_name')
        print(fetchpid)
        print(fetchcartdata)
        fetchproductdata = Food_Item.objects.filter(id__in=fetchpid)
        print(fetchproductdata)
        userdetails = Customer.objects.get(id=user1)
        cart_count = cart.objects.count()
        context = {
            'cart': fetchcartdata,
            'product': fetchproductdata,
            'user': userdetails,
            'carttotal': carttotal,
            "cart_count": cart_count
        }
        return render(request, "cart.html", context)
    else:
        return redirect(login)


def add_cart(request, id, qty):
    id2 = request.session['userid']
    # price = request.POST.get("pri")
    # quantity = request.POST.get("quan")
    foodItem = Food_Item.objects.get(id=id)
    price = foodItem.Price
    quantity = qty
    totalpricee = price * quantity
    try:
        query = cart.objects.get(food_name=id, customer_name=id2, product_status=1)
    except:
        query = None

    if query is not None:
        query.quantity = query.quantity + quantity
        query.totalprice = query.totalprice + totalpricee
        query.save()
    else:
        cartquery = cart(food_name=Food_Item(id=id), quantity=quantity, product_status=1,
                         customer_name=Customer(id=id2),
                         orderid=0,
                         totalprice=totalpricee)
        cartquery.save()
    return redirect("cart")


def removeItem_cart(request, id):
    query = cart.objects.get(id=id)
    query.delete()
    return redirect("cart")


def destroyCart(request):
    cart_items = cart.objects.all()
    cart_items.delete()
    return redirect("cart")


def recentOrders(request):
    return render(request, 'recent_orders.html')


def subcategory(request, name):
    name_list = re.split('(?<=.)(?=[A-Z])', name)
    print(name_list)
    cat_name = name_list[0]
    if len(name_list) > 1:
        for name in name_list[1:]:
            cat_name = cat_name + " " + name
    category = Food_Category.objects.get(Name=cat_name)
    subcategory_data = Food_Category.objects.filter(Subcategory=category.id).exclude(id=category.id)
    category = Food_Category.objects.get(id=category.id)
    cart_count = cart.objects.count()
    if (subcategory_data):
        context = {
            "subcategories": subcategory_data,
            "category": category,
            "cart_count": cart_count
        }
        return render(request, 'subcategory.html', context=context)
    else:
        food_data = Food_Item.objects.filter(Category=category.id)
        cart_count = cart.objects.count()
        context = {
            "category": category,
            "food_items": food_data,
            "cart_count": cart_count
        }
        return render(request, 'foodItems.html', context=context)
    return HttpResponse("Something Went Wrong!!")


def product_details(request, cat, name):
    name_list = re.split('(?<=.)(?=[A-Z])', name)
    print(name_list)
    food_name = name_list[0]
    if len(name_list) > 1:
        for name in name_list[1:]:
            food_name = food_name + " " + name
    print("name :", food_name)
    food_item_data = Food_Item.objects.get(Name=food_name)
    other_food_items_data = Food_Item.objects.filter(Category=food_item_data.Category).exclude(id=food_item_data.id)
    cart_count = cart.objects.count()
    context = {
        "food_data": food_item_data,
        "other_food_items_data": other_food_items_data,
        "cart_count": cart_count

    }
    return render(request, "product-details.html", context=context)


# def product_details(request,id):
#     food_item_data = Food_Item.objects.get(id=id)
#     other_food_items_data = Food_Item.objects.filter(Category=food_item_data.Category).exclude(id=food_item_data.id)
#     context = {
#         "food_data" : food_item_data,
#         "other_food_items_data" : other_food_items_data
#     }
#     return render(request, "product-details.html",context=context)

# def subcategory(request,id):
#     parent_category_id = id
#     subcategory_data = Food_Category.objects.filter(Subcategory = parent_category_id).exclude(id=id)
#     category = Food_Category.objects.get(id=id)  
#     if(subcategory_data):
#         context = {
#         "subcategories" : subcategory_data,
#         "category" : category
#         }
#         return render(request,'subcategory.html',context=context)
#     else:
#         food_data = Food_Item.objects.filter(Category=id)
#         context = {
#             "category" : category,
#             "food_items" : food_data
#         }
#         return render(request,'foodItems.html',context=context)
#     return HttpResponse("Something Went Wrong!!")

def error(request):
    return render(request, "404.html")


def checkout(request):
    global customer_id

    try:
        customer_id = request.session['userid']
        address_data = Address.objects.filter(Customer_name=Customer(id=customer_id))
    except:
        address_data = None
    if address_data is None:
        area_name = Area.objects.all()
        context = {
            'areaname': area_name
        }
        messages.error(request, "Please add your address first")
        return render(request, "address.html", context)
    area_name = Area.objects.all()
    print(address_data)
    cart_items = cart.objects.count()

    user = request.session['userid']
    fee = 20
    # carttotal = cart.objects.filter(customer_name=user, product_status=1).aggregate(Sum('totalprice'))[
    #     'totalprice__sum']
    carttotal = request.session.get('carttotal', None)
    print("cartotal", request.session.get('carttotal'))
    carttotal = carttotal + fee
    print(carttotal)
    if cart_items > 0:
        user_cart_items = cart.objects.filter(customer_name=user, product_status=1)
        print(user_cart_items)
        cart_count = cart.objects.count()
        context = {
            "cart_items": user_cart_items,
            "total_price": carttotal,
            "cart_count": cart_count,
            'packfees': fee,
            'address_data': address_data,
        }
        return render(request, "checkout.html", context)

    return redirect("cart")


def contact(request):
    cart_count = cart.objects.count()
    context = {
        "cart_count": cart_count
    }
    return render(request, "contact.html", context)


def saveContact(request):
    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("message")
        subject = "Contact"
        message = "Hey," + email + " is contacting you. " + message
        email_from = "nisargt1782@gmail.com"
        cus = ['dvp060723@gmail.com']
        send_mail(subject, message, email_from, cus)
        if (send_mail):
            messages.success(request, "Success👏,We are contacting you shortly.")
        else:
            messages.error(request, "Something Went Wrong")
    return redirect(contact)


def login(request):
    return render(request, "login.html")


def wishlist(request):
    cart_count = cart.objects.count()
    context = {
        "cart_count": cart_count
    }
    return render(request, "wishlist.html", context)


def service(request):
    cart_count = cart.objects.count()
    context = {
        "cart_count": cart_count
    }
    return render(request, "service.html", context)


def logout(request):
    del request.session["username"]
    del request.session["useremail"]
    del request.session["userphone"]
    return redirect('login')


def profile(request):
    cart_count = cart.objects.count()
    # print(request.session["email"])
    email = request.session["useremail"]
    try:
        query = Customer.objects.get(Email=email)
    except:
        query = None
    if query.cus_Image is not None:
        context = {
            'first_name': query.First_Name,
            'last_name': query.Last_Name,
            'email': query.Email,
            'contact': query.Contact,
            'img': query.cus_Image,
            "cart_count": cart_count
        }
    else:
        context = {
            'first_name': query.First_Name,
            'last_name': query.Last_Name,
            'email': query.Email,
            'contact': query.Contact,
            # 'img': query.cus_Image,
            "cart_count": cart_count
        }
    return render(request, "profile.html", context)


def update_profile(request):
    if request.method == "POST":
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        phone = request.POST.get("contact")
        email = request.POST.get("email")
        print(request.session["userphone"])
        if fname == "" or fname.isnumeric() == True:
            messages.error(request, "First name is not valid")
            return render(request, "profile.html")
        if lname == "" or lname.isnumeric() == True:
            messages.error(request, "Last name is not valid")
            return render(request, "profile.html")
        if len(phone) != 10:
            messages.error(request, "Phone number is not valid")
            return render(request, "profile.html")
        if phone.isnumeric() == False:
            messages.error(request, "phone number not contain characters")
            return render(request, "profile.html")
        try:
            query = Customer.objects.get(Email=email)
        except:
            query = None
        if query is not None:
            try:
                query2 = Customer.objects.get(Contact=phone)
            except:
                query2 = None
            if query2 is None:
                query3 = Customer.objects.get(Email=email)
                query3.First_Name = fname
                query3.Last_Name = lname
                query3.Contact = phone
                query3.save()
                del request.session["userphone"]
                request.session["userphone"] = query3.Contact
                return redirect('profile')
            else:
                query.First_Name = fname
                query.Last_Name = lname
                query.save()
                return redirect('profile')


def placeorder(request):
    if request.method == "POST":
        # if request.POST.get('paypal'):
        reciver_name = request.POST.get("name")
        request.session['username'] = reciver_name
        customer_id = request.session["userid"]
        reciver_phone = request.POST.get("phone")
        address = request.POST.get("address")
        print("address", address)
        if address is not None:
            address_data = Address.objects.filter(id=address)
            print("address data is", address_data)
            area_pincode = address_data.first().Area_Pincode.Name
            print("Area pincode is:", area_pincode)
            data = "https://www.google.com/maps/place/" + area_pincode + ",+Ahmedabad,+Gujarat"
            print("your url is ", data)
            payment_type = request.POST.get("payment_type")

            if not reciver_name or not reciver_name.strip() or reciver_name.isdigit():  # Checking if name is empty or only whitespace
                messages.error(request, "Name is not valid")
                return redirect("checkout")
            # Validate phone
            if not reciver_phone or not reciver_phone.isdigit() or len(reciver_phone) != 10:
                messages.error(request, "Phone number must contain 10 digits")
                return redirect("checkout")
            fee = 20
            print("fee is ")
            print("fee is ", fee)
            # carttotal = cart.objects.filter(customer_name=customer_id, product_status=1).aggregate(Sum('totalprice'))[
            #     'totalprice__sum']
            carttotal = request.session.get('carttotal')
            print("cart total is : ", carttotal)
            carttotal = carttotal + fee
            print("again carttotal is : ", carttotal)
            # request.session['total'] = carttotal
            # total = request.session.get('total')
            # total = {
            #     'total': carttotal
            # }
            print(carttotal)
            if payment_type == "Cash On Delivery":
                mode = True
                payment_mode = False
                payment_type = 'cash'
            elif payment_type == "Pay Pal":
                payment_mode = True
                payment_type = 'Card'
                mode = True
                print("88888888")
                print('paypal')
                print("88888888")



            else:
                payment_mode = False
            orderquery = SaleOrder(address=Address(id=address), IsCancel=0, Totalammount=carttotal,
                                   Customer_Name=Customer(id=customer_id), Payment_Status=payment_mode,
                                   Payment_Type=payment_type, location=data)
            request.session['order_id'] = orderquery.id

            orderquery.save()

            lastid = SaleOrder.objects.latest('id').pk
            request.session['lastpid'] = lastid

            print(lastid)
            sale_data = SaleOrder.objects.get(id=lastid)
            # request.session['datetime'] = sale_data.Date
            order_status = Order_Status(SaleOrder_Id=SaleOrder(id=lastid), Status=1)
            order_status.save()
            fetchcartdata = cart.objects.filter(customer_name=Customer(id=customer_id))
            for ob in fetchcartdata:
                ob.product_status = 0
                ob.orderid = lastid
                ob.save()
                pid = ob.food_name
                quan = ob.quantity
                query = SaleOrder_Detail(SaleOrder_Id=SaleOrder(id=lastid), Quantity=quan,
                                         Food_Item_Name=pid)
                query.save()
            cart_count = cart.objects.count()
            request.session['cart_count'] = cart_count
            if (payment_type == "cash"):
                today = datetime.today()
                context = {
                    'lastpid': lastid,
                    'datetime': sale_data.Date,
                    "cart_count": cart_count
                }
                fetchcartdata.delete()
                email = request.session["useremail"]
                print(email)
                subject = 'About Login...'
                order_id = orderquery.id
                subject = 'Confirmation: Your Order has been placed successfully'
                message = f"Dear Customer,\n\nThank you for placing your order. Your order ID is: {order_id}. We will process it shortly.\n\nRegards,\nMidnight Delights"

                email_from = 'nisargt1782@gmail.com'
                cus = [email]
                send_mail(subject, message, email_from, cus)
                return render(request, "thanku.html", context)
            if (payment_type == "Card"):
                today = datetime.today()
                context = {
                    'lastpid': lastid,
                    'datetime': sale_data.Date,
                    "cart_count": cart_count,
                    'total': carttotal,
                    'username': request.session.get('username')
                }
                fetchcartdata.delete()
                return render(request, "pay_pal.html", context)
                # return render(request, "thanku.html", context)
            # elif (payment_type == "paypal"):
            # today = datetime.today()
            # context = {
            #     'lastpid': lastid,
            #     'datetime': sale_data.Date,
            #     "cart_count": cart_count
            # }
            # return render('pay_pal.html', total)

            del request.session['carttotal']
            request.session.save()
        else:
            area_name = Area.objects.all()
            context = {
                'areaname': area_name
            }
            return render(request, "address.html", context)
        # email = request.session["useremail"]
        # print(email)
        # subject = 'About Login...'
        # message = (f'Hi ,your Login process is started  on Midnight delights and your otp is  otp is '
        #            f'Your Otp is valid for Five minutes only')
        # email_from = 'nisargt1782@gmail.com'
        # cus = [email]
        # send_mail(subject, message, email_from, cus)
    else:
        return redirect("cart")


def paypal(request):
    return render(request, 'pay_pal.html')


def process_payment(request):
    if request.method == 'POST':
        # payment_details = request.POST.get('payment_details')
        # Process payment details as needed
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def address(request):
    area_name = Area.objects.all()
    cart_count = cart.objects.count()
    context = {
        'areaname': area_name,
        'cart_count': cart_count
    }
    return render(request, "address.html", context)


def saveaddress(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("contact")
        landmark = request.POST.get("landmark")
        address_type = request.POST.get("address_type")
        area_name = request.POST.get("area_name")
        customer_id = request.session["userid"]
        if not name or not name.strip() or name.isdigit():  # Checking if name is empty or only whitespace
            messages.error(request, "Name is required")
            return redirect("address")

        # Validate phone
        if not phone or not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must contain 10 digits")
            return redirect("address")
        # Validate landmark
        if not landmark or not landmark.strip():  # Checking if landmark is empty or only whitespace
            messages.error(request, "Landmark is required")
            return redirect("address")
        try:
            query = Address.objects.get(Landmark=address, Customer_name=Customer(id=customer_id),
                                        Receiver_Contact=phone, Receiver_Name=name)
        except:
            query = None
        if query is None:
            data = Address(Receiver_Name=name, Receiver_Contact=phone,
                           Address_type=address_type,
                           Landmark=landmark, Area_Pincode=Area(Pincode=area_name),
                           Customer_name=Customer(id=customer_id))
            data.save()
            return redirect("checkout")
        else:
            messages.error(request, "Address already exists")
            return redirect("address")


def thanku(request):
    lastid = request.session.get('lastpid')
    sale_data = SaleOrder.objects.get(id=lastid)
    cart_count = cart.objects.count()
    context = {
        'lastpid': lastid,
        'datetime': sale_data.Date,
        'cart_count': cart_count,

    }
    email = request.session["useremail"]
    print(email)
    subject = 'About Login...'
    order_id = request.session.get('order_id')
    subject = 'Confirmation: Your Order has been placed successfully'
    message = f"Dear Customer,\n\nThank you for placing your order. Your order ID is: {order_id}. We will process it shortly.\n\nRegards,\nMidnight Delights"

    email_from = 'nisargt1782@gmail.com'
    cus = [email]
    send_mail(subject, message, email_from, cus)
    return render(request, "thanku.html", context)


def orderhistory(request):
    try:
        print("0")
        user1 = request.session['userid']

        orders = SaleOrder.objects.filter(Customer_Name=user1).order_by('-id')
        print("1")
        print(orders)
        # user4=cart.objects.filter(order_id=)
        cart_count = cart.objects.count()
        context = {
            'data': orders,
            "cart_count": cart_count
            # 'data4':user4
        }
        return render(request, "recent_orders.html", context)
    except:
        u1 = None
        return render(request, "order.html")


def order(request):
    return render(request, "order.html")


def orderdetails(request, id):
    try:

        global mode

        user1 = request.session['userid']
        print("1")
        sale_order = SaleOrder.objects.get(id=id)
        print("2")
        print(sale_order)
        # print(x.order_status)
        # print("3")
        # status = x.order_status
        print("4")
        fetchcartdata = SaleOrder_Detail.objects.filter(SaleOrder_Id=id)
        print("cart : " + str(fetchcartdata))
        print("5")
        # carttotal = cart.objects.filter(orderid=id).aggregate(Sum('totalprice'))
        # print(carttotal)
        fetchpid = SaleOrder_Detail.objects.filter(SaleOrder_Id=id).values('Food_Item_Name')

        print(fetchpid)
        print("6")
        print(fetchpid)
        print(fetchcartdata)
        fetchproductdata = Food_Item.objects.filter(id__in=fetchpid)
        print("products: " + str(fetchproductdata))
        # userdetails = Customer.objects.get(id=user1)
        print("n")
        order_statuses = Order_Status.objects.filter(SaleOrder_Id=id).order_by('id')
        print("status is",order_statuses)
        # Loop through each order status
        # for order_status in order_statuses:
        #     # Access and print timestamp and status
        #     print("Timestamp:", order_status.date_time)
        #     print("Status:", order_status.Status)
        # user = Food_Category.objects.all()
        # x = request.session['feedb']
        print("nisu")
        # order_deleted = get_object_or_404(SaleOrder, id=id)
        # order_deleted.IsCancel = True
        # order_deleted.save()
        cart_count = cart.objects.count()
        context = {
            'cart': fetchcartdata,
            'order_status': order_statuses[0],
            'product': fetchproductdata,
            'orderid': id,
            'cart_count': cart_count,
            'total_price': sale_order.Totalammount,
            # 'order':order_deleted
        }
        return render(request, "orderdetails.html", context)
    except:
        u1 = None


def delete_order(request, id):
    try:
        sale_order = SaleOrder.objects.get(id=id)
        # sale_order.delete()
        sale_order.IsCancel = True
        sale_order.save()
        messages.success(request, "Order cancelled successfully.")
    except SaleOrder.DoesNotExist:
        messages.error(request, "Order does not exist.")
    return redirect("orderhistory")


def feedback(request, id, id2):
    # id1= order id
    # id2=food item id
    customer_id = request.session["userid"]
    try:
        query = Feedback.objects.get(SaleOrder_Id=SaleOrder(id=id), Customer_Name=Customer(id=customer_id),
                                     Food_Item_Name=Food_Item(id=id2))
    except:
        query = None
    print(query)
    if query is None:
        food_item_name = Food_Item.objects.get(id=id2)
        print(food_item_name.Name)
        context = {
            'orderid': id,
            'prod': food_item_name.Name,
            'prodid': id2
        }
        return render(request, "feedback.html", context)
    else:
        print(query.Food_Item_Name)
        print(query.SaleOrder_Id)
        print(query.Customer_Name)
        print(query.Description)
        context = {
            'orderid': id,
            'prod': query.Food_Item_Name,
            'prodid': id2,
            'description': query.Description

        }
        return render(request, "feedback.html", context)


def send_feed(request, id, id2):
    customer_id = request.session["userid"]
    description = request.POST.get("feedback")
    try:
        query = Feedback.objects.get(SaleOrder_Id=SaleOrder(id=id), Customer_Name=Customer(id=customer_id),
                                     Food_Item_Name=Food_Item(id=id2))
    except:
        query = None
    print(query)
    if query is None:
        description = request.POST.get("feedback")
        order_id = id
        product_id = id2
        customer_id = request.session["userid"]
        query2 = Feedback(Rating=1, SaleOrder_Id=SaleOrder(id=order_id), Customer_Name=Customer(id=customer_id),
                          Description=description,
                          Food_Item_Name=Food_Item(id=product_id))
        query2.save()
        messages.success(request, "Thank You for Giving Feedback")
        return redirect("orderhistory")
    else:
        query.Description = description
        query.save()
        return redirect("orderhistory")


def updatefeedback(request):
    return render(request, "updatefeedback.html")


def resend_otp(request):
    if 'otp_timestamp' in request.session:
        timestamp = datetime.fromtimestamp(request.session.get("otp_timestamp"))
        current_time = datetime.now()
        time_difference = current_time - timestamp

        if time_difference.total_seconds() < 30:
            # Render a page with a popup message indicating they cannot resend yet
            messages.warning(request, "You can resend the OTP after 30 seconds.")
            return redirect("otp")  # Replace 'otp' with the actual URL name
    request.session["otp_timestamp"] = timestamp.timestamp()
    print("OTP is:", otp)

    email = request.session.get("useremail")

    send_otp(request)

    return redirect("otp")

from django.template.loader import get_template
from xhtml2pdf import pisa
def invoice(request, id):
    try:
        user1 = request.session['userid']
    except:
        user1 = None
    if (user1 is not None):
        fetchcartdata = SaleOrder_Detail.objects.filter(id=id)
        carttotal = cart.objects.filter(orderid=id).aggregate(Sum('totalprice'))
        print(carttotal)
        today = date.today()
        fetchpid = SaleOrder_Detail.objects.filter(id=id).values('Food_Item_Name')
        print(fetchpid)
        # print(fetchcartdata.SaleOrder_Id)
        s1 = SaleOrder.objects.get(id=id)
        print("amount: ",s1.Totalammount)
        ct = s1.Totalammount
        da = s1.address
        dat = s1.Date
        fetchproductdata = Food_Item.objects.filter(id__in=fetchpid)
        print("product data:", fetchproductdata)
        userdetails = Customer.objects.filter(id=user1)
        user = Food_Category.objects.all()
        context = {
            'cart': fetchcartdata,
            'product': fetchproductdata,
            'user': userdetails,
            'carttotal': ct,
            'orderid': id,
            'daddress': da,
            'dat': dat,
            'dateq': today,
            'data1': user
        }
        temp = get_template('invoice.html')
        html = temp.render(context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')

        return render(request, "invoice.html", context)

        # return None

    else:
        return redirect("login")




def get_data(request):
    customers = Customer.objects.all()
    cus_data = []
    for customer_data in customers:
        customer_data = {
            'id': customer_data.id,
            'First_Name': customer_data.First_Name,
            'Email': customer_data.Email,
            # 'phone': str(customer_data.phone),  # Convert DecimalField to string for JSON serialization
            'img_url': customer_data.cus_Image.url if customer_data.cus_Image else None
            # if cus_img is None, provide None as the URL, otherwise provide the actual URL
        }

        cus_data.append(customer_data)
        print(cus_data)
    return JsonResponse({"data": cus_data})





@csrf_exempt
def update_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        email = data.get('email')
        first_name = data.get('firstname')
        last_name = data.get('lastname')
        contact = data.get('contact')

        if Customer.objects.filter(Email=email).exists():
            if Customer.objects.filter(Contact=contact).exists():
                return JsonResponse({'error': 'Contact already exists'}, status=409)
            else:
                customer = Customer.objects.get(Email=email)
                customer.First_Name = first_name
                customer.Last_Name = last_name
                customer.Contact = contact
                customer.save()
                return JsonResponse({'msg': 'Updated Successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Email does not match'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def user_data(request, id):
    if request.method == 'GET':
        try:
            user_profile = Customer.objects.get(id=id)
            data = {
                'firstname': user_profile.First_Name,
                'lastname': user_profile.Last_Name,
                'email': user_profile.Email,
                'phone_number': user_profile.Contact,
                # Add other fields as needed
            }
            return JsonResponse(data)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User profile does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


@csrf_exempt
def address_list(request):
    if request.method == 'GET':
        addresses = Address.objects.all()
        data = [{'Receiver_Name': address.Receiver_Name,
                 'Receiver_Contact': address.Receiver_Contact,
                 'Landmark': address.Landmark,
                 'Address_type': address.Address_type,
                 'Area_Pincode': address.Area_Pincode.Pincode if address.Area_Pincode else None,
                 'Customer_name': address.Customer_name.First_Name if address.Customer_name else None
                }
                for address in addresses]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        data = request.POST
        receiver_name = data.get('Receiver_Name')
        receiver_contact = data.get('Receiver_Contact')
        landmark = data.get('Landmark')
        address_type = data.get('Address_type')
        area_pincode_id = data.get('Area_Pincode')  # Assuming this is provided as ID
        customer_name_id = data.get('Customer_name')  # Assuming this is provided as ID

        # Validate receiver_name
        if receiver_name.isdigit():
            raise ValidationError('Name should not contain only digits.')

        # Create Address object
        address = Address(
            Receiver_Name=receiver_name,
            Receiver_Contact=receiver_contact,
            Landmark=landmark,
            Address_type=address_type
        )

        # Assign Area and Customer if provided
        if area_pincode_id:
            address.Area_Pincode = area_pincode_id
        if customer_name_id:
            address.Customer_name = customer_name_id

        address.save()

        return JsonResponse({'message': 'Address created successfully'}, status=201)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def search_food(request):
    cart_count = cart.objects.count()
    if request.method == "POST":
        query = request.POST.get("search")
        if len(query) > 30:
            user = Food_Category.objects.all()
            context = {
                'data1': user

            }
            messages.error(request, "Your search result is too long...")
            return render(request, "search.html", context)
        categoryName = ''.join(word.capitalize() for word in query.split())
        user2 = Food_Item.objects.filter(Q(Name__icontains=categoryName,))
        user3 = Food_Item.objects.filter(Description__icontains=categoryName)
        user31 = Food_Category.objects.filter(Q(Name__icontains=categoryName))
        category_data = Food_Category.objects.all()
        product_data = Food_Item.objects.all()

        # user4 = user2.union(user3, user31)
        user4 = list(user2) + list(user31) + list(user3)
        user = Food_Category.objects.all()


        context = {
            'data1': user,
            'data2': user4,
            'query': query,
            'cart_count':cart_count
        }
        return render(request, "search.html", context)
    else:
        messages.error(request, "Please enter product name which you want to search")
        return redirect("search")

def search(request):
    return render(request,'search.html')