from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from ProductApp.models import Product,Images,Category,Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .import forms, models
# Create your views here.
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.


def user_logout(request):
    logout(request)
    return redirect('home')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Your username or password is invalid.')
    catagory = Category.objects.all()
    contaxt = {
        'catagory': catagory,
    }
    return render(request, 'login-register.html',contaxt)



def user_register(request):
    if request.method == 'POST':
        form =forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password_raw = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password_raw)
            login(request, user)
            current_user = request.user
            data = models.UserProfile()
            data.user_id = current_user.id
            data.image = "user_img/minhaj.jpg"
            data.save()
            return redirect('home')
        else:
            messages.warning(request, "Your new and reset password is not matching")
    else:
        form = forms.SignUpForm()
    catagory = Category.objects.all()
    context = {
               'catagory': catagory,
               'form': form
               }
    return render(request, 'register.html', context)


def userprofile(request):
    catagory = Category.objects.all()
    current_user = request.user
    profile = models.UserProfile.objects.get(user_id=current_user.id)

    context = {
               'catagory': catagory,
               'profile': profile
    }
    return render(request, 'user_profile.html', context)

@login_required(login_url='/user/login')  # Check login
def user_update(request):
    if request.method == 'POST':
        # request.user is user  data
        user_form = forms.UserUpdateForm(request.POST, instance=request.user)
        profile_form = forms.ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('userprofile')
    else:
       # category = Category.objects.all()
        user_form = forms.UserUpdateForm(instance=request.user)
        # "userprofile" model -> OneToOneField relatinon with user
        profile_form = forms.ProfileUpdateForm(instance=request.user)
        catagory = Category.objects.all()

        context = {
            # 'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'catagory': catagory,
        }
        return render(request, 'userupdate.html', context)


@login_required(login_url='/user/login')  # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('userprofile')
        else:
            messages.error(
                request, 'Please correct the error below.<br>' + str(form.errors))
            return redirect('user_password')
    else:
        catagory = Category.objects.all()
        form = PasswordChangeForm(request.user)
        context = {
            'form': form,
            'catagory': catagory,

        }
        return render(request, 'userpasswordupdate.html', context )

@login_required(login_url='/user/login')
def usercomment(request):
    catagory = Category.objects.all()
    current_user = request.user
    comment = Comment.objects.filter(user_id=current_user.id)
    context = {
            'catagory': catagory,
            'comment': comment
          }
    return render(request, 'usercomment.html', context)



def comment_delete(request, id):
    current_user = request.user
    comment = Comment.objects.filter(user_id=current_user.id, id=id)
    comment.delete()
    messages.success(request, 'Your comment is successfully deleted')
    return redirect('usercomment')
