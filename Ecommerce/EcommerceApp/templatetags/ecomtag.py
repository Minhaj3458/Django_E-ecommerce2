from django import template

from EcommerceApp.models import Setting
from ProductApp.models import Product,Images,Category,Comment

register = template.Library()


@register.simple_tag
def ecom_cat():
    return Category.objects.all()


@register.simple_tag
def ecom_set():
    return Setting.objects.get(id=1)