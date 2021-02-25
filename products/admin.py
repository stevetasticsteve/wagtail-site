from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin
from .models import Product, ProductCategory


class ProductCategoryAdmin(ModelAdmin):
    """Product category admin."""

    model = ProductCategory
    menu_label = "Categories"
    menu_icon = "grip"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("category_name",)
    search_fields = ("category_name", "descriptive_text")


class ProductAdmin(ThumbnailMixin, ModelAdmin):
    """Individual products admin."""

    model = Product
    menu_label = "Items"
    menu_icon = "plus-inverse"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("product_name", "category", 'admin_thumb', "price")
    search_fields = ("product_name",)

    thumb_image_field_name = 'product_image'
    thumb_classname = 'admin-thumb'


class ProductGroup(ModelAdminGroup):
    menu_label = 'Products'
    menu_icon = 'placeholder'
    menu_order = 200
    items = (ProductCategoryAdmin, ProductAdmin)


modeladmin_register(ProductGroup)
