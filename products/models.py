from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class ProductCategory(models.Model):
    category_name = models.CharField(
        verbose_name='Product category',
        null=False,
        blank=False,
        max_length=50,
        help_text="The name of the prouct type i.e. Computers"
    )
    descriptive_text = models.TextField(
        blank=False,
        null=True,
        help_text="A short description to go on the product category's home page card",
        max_length=100)

    product_category_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        help_text='An image to represent the product category type',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.category_name

    panels = [
        FieldPanel('category_name'),
        FieldPanel('descriptive_text'),
        ImageChooserPanel('product_category_image')
    ]


class Product(models.Model):
    category = models.ForeignKey(
        'ProductCategory',
        on_delete=models.CASCADE,
        related_name='+',
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=True,
        help_text="The product price in GBP"
    )
    product_name = models.CharField(max_length=50, blank=False, null=True)

    product_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        help_text='An image to represent the product',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f'{self.product_name}, costing £{self.price}'

    panels = [
        FieldPanel('category'),
        FieldPanel('product_name'),
        FieldPanel('price'),
        ImageChooserPanel('product_image')
    ]
