from django.contrib import admin
from .import models
from mptt.admin import DraggableMPTTAdmin
import admin_thumbnails
# Register your models here.

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = models.Category.objects.add_related_count(
                qs,
                models.Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = models.Category.objects.add_related_count(qs,
                 models.Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


admin.site.register(models.Category, CategoryAdmin)

@admin_thumbnails.thumbnail('image')
class productImageInline(admin.TabularInline):
    model = models.Images
    extra = 1
    readonly_fields = ('id',)

class ProductVariantsInline(admin.TabularInline):
    model = models.Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at', 'updated_at', 'new_price', 'image_tag']
    list_filter = ['title', 'created_at']
    list_per_page = 10
    search_fields = ['title', 'new_price', 'detail']
    inlines = [productImageInline, ProductVariantsInline]
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(models.Product,ProductAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'status', 'created_at', 'updated_at', 'user']
    list_filter = ['status', 'created_at']
    list_per_page = 10


admin.site.register(models.Comment, CommentAdmin)



class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']


admin.site.register(models.Color, ColorAdmin)


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


admin.site.register(models.Size, SizeAdmin)


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'color', 'size', 'image_id', 'quantity', 'price', 'image_tag']


admin.site.register(models.Variants, VariantsAdmin)


