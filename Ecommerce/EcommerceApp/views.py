from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from .import models,forms
from django.contrib import messages
from ProductApp.models import Product,Images,Category,Comment
from Order_APP.models import ShopCart
# Create your views here.
from django.http import HttpResponse

def common(request):
    catagory = Category.objects.all()
    context = {
        'catagory': catagory
    }

    return render(request, 'common.html', context)


def home(request):
    pro = Product.objects.all().order_by('id')[:2]
    leatst_pro = Product.objects.all().order_by('-id')
    current_user = request.user
    cart_product = ShopCart.objects.filter(user_id = current_user.id)
    count = cart_product.count()
    total_amount = 0
    for p in cart_product:
        total_amount += p.product.new_price * p.quantity
    context = {
        'prodect': pro,
        'leatst_pro': leatst_pro,
        'cart_product': cart_product,
        'total_amount': total_amount,
        'count': count
    }
    return render(request, 'home.html', context)

def single_product(request,id):
    pro_single = Product.objects.get(id=id)
    Extra_images = Images.objects.filter(product_id=id)
    comment_show = Comment.objects.filter(product_id=id, status='True')
    catagory = Category.objects.all()
    context ={
          'pro_single': pro_single,
          'Extra_images': Extra_images,
          'catagory': catagory,
          'comment_show': comment_show


    }
    return render(request, 'single-product.html', context)

def category_product(request, id, slug):
    product_cat = Product.objects.filter(category_id=id)
    catagory = Category.objects.all()
    context = {
        'product_cat': product_cat,
        'catagory': catagory
    }
    return render(request, 'shop-left-sidebar.html', context)


def contact_page(request):
    if request.method == 'POST':
        form =models.ContactForm(request.POST)
        if form.is_valid():
            data = models.ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Profile details updated.')
            return redirect('contact_page')

    form = models.ContactForm
    catagory = Category.objects.all()
    context = {
        'catagory': catagory,
        'form' : form
    }
    return render(request, 'contact.html', context)




def searchView(request):
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            cat_id = form.cleaned_data['cat_id']
            if cat_id == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(
                    title__icontains=query, category_id=cat_id)
            catagory = Category.objects.all()
            setting = models.Setting.objects.get(id=1)
            context = {
                'catagory': catagory,
                'query': query,
                'product_cat': products,
                'setting': setting,
            }
            return render(request, 'shop-left-sidebar.html', context)
    return HttpResponseRedirect('category_product')
