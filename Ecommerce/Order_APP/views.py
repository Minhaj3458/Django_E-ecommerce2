from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from .import models
from django.contrib import messages
from ProductApp.models import Product,Images,Category
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from UserApp.models import UserProfile
# Create your views here.
def Add_to_Shoping_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checking = models.ShopCart.objects.filter(
        product_id=id, user_id=current_user.id)
    if checking:
        control = 1
    else:
        control = 0

    if request.method == "POST":
        form = models.ShopingCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = models.ShopCart.objects.filter(
                    product_id=id, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = models.ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, 'Your Product  has been added')
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = models.ShopCart.objects.filter(
                product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()
        else:
            data =models.ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, 'Your  product has been added')
        return HttpResponseRedirect(url)

def Cart_details(request):
    catagory = Category.objects.all()
    current_user = request.user
    cart_product = models.ShopCart.objects.filter(user_id=current_user.id)
    total_amount = 0
    for p in cart_product:
        total_amount += p.product.new_price * p.quantity
    context={
        'catagory': catagory,
        'cart_product': cart_product,
        'total_amount': total_amount
    }
    return render(request, 'shopping-cart.html', context)

def cart_delete(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    cart_product = models.ShopCart.objects.filter(id=id, user_id=current_user.id)
    cart_product.delete()
    messages.warning(request, 'Your product has been deleted.')
    return HttpResponseRedirect(url)





def OrderCart(request):
    current_user = request.user
    shoping_cart = models.ShopCart.objects.filter(user_id=current_user.id)
    totalamount = 0
    for rs in shoping_cart:
        totalamount += rs.quantity*rs.product.new_price
    if request.method == "POST":
        form = models.OderForm(request.POST, request.FILES)
        if form.is_valid():
            dat = models.Order()
            # get product quantity from form
            dat.first_name = form.cleaned_data['first_name']
            dat.last_name = form.cleaned_data['last_name']
            dat.address = form.cleaned_data['address']
            dat.city = form.cleaned_data['city']
            dat.phone = form.cleaned_data['phone']
            dat.country = form.cleaned_data['country']
            dat.transaction_id = form.cleaned_data['transaction_id']
            dat.transaction_image = form.cleaned_data['transaction_image']
            dat.user_id = current_user.id
            dat.total = totalamount
            dat.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random cod
            dat.code = ordercode
            dat.save()

            # moving data shortcart to product cart
            for rs in shoping_cart:
                data = models.OderProduct()
                data.order_id = dat.id
                data.product_id = rs.product_id
                data.user_id = current_user.id
                data.quantity = rs.quantity
                data.price = rs.product.new_price
                data.amount = rs.amount
                data.save()
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
            # Now remove all oder data from the shoping cart
            models.ShopCart.objects.filter(user_id=current_user.id).delete()
            # request.session['cart_item']=0
            messages.success(request, 'Your oder has been completed')
            catagory = Category.objects.all()
            context = {
                # 'category':category,
                'ordercode': ordercode,
                'catagory': catagory,
            }

            return render(request, 'oder_completed.html', context)
        else:
            messages.warning(request, form.errors)
          #  return HttpResponseRedirect("/order/oder_cart")
    form = models.OderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    total_amount = 0
    for p in shoping_cart:
        total_amount += p.product.new_price*p.quantity
    catagory = Category.objects.all()

    context = {
        # 'category':category,
        'shoping_cart': shoping_cart,
        'totalamount': totalamount,
        'profile': profile,
        'form': form,
        'catagory': catagory,
        'total_amount': total_amount
    }
    return render(request, 'order_form.html', context)



def Order_showing(request):
    catagory = Category.objects.all()
    current_user = request.user
    orders = models.Order.objects.filter(user_id=current_user.id)
    context = {
        'catagory': catagory,
        'orders': orders,
      }
    return render(request, 'user_order_showing.html', context)


def Order_Product_showing(request):
    catagory = Category.objects.all()
    current_user = request.user
    order_product = models.OderProduct.objects.filter(user_id=current_user.id)
    context = {
        'catagory': catagory,
        'order_product': order_product

    }

    return render(request, 'OrderProducList.html', context)



@login_required(login_url='/user/login')
def user_oder_details(request, id):
    catagory = Category.objects.all()
    current_user = request.user
    order = models.Order.objects.get(user_id=current_user.id, id=id)
    order_products = models.OderProduct.objects.filter(user_id=current_user.id)
    context = {
        'catagory': catagory,
        'order': order,
        'order_products': order_products,
    }
    return render(request, 'user_order_details.html', context)



@login_required(login_url='/user/login')
def useroderproduct_details(request, id, oid):
    catagory = Category.objects.all()
    current_user = request.user
    order = models.Order.objects.get(user_id=current_user.id, id=oid)
    order_products = models.OderProduct.objects.get(user_id=current_user.id, id=id)
    context = {
        'order': order,
        'order_products': order_products,
        'catagory': catagory,
    }
    return render(request, 'user_order_pro_details.html', context)





