from django.contrib import admin
from .import models
# Register your models here.

admin.site.register(models.Setting)
admin.site.register(models.ContactMessage)



class FAQamin(admin.ModelAdmin):
    list_display = ['ordernumber', 'question', 'status', 'created_at', 'updated_at']

admin.site.register(models.FAQ, FAQamin)