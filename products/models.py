from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField


class ProductCategory(models.Model):
    """An admin model for organising products into groups. Is a required Foreign key to individual products.
    The save method has been extended to automatically generate a ProductCategoryPage for new categories."""
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

    description = RichTextField(
        blank=True,
        null=True,
        help_text='Optional paragraph describing the products that will appear on the product category page. Supposed to be a fuller description than the text entered for the card view under products'
    )

    def __str__(self):
        return self.category_name

    panels = [
        FieldPanel('category_name'),
        FieldPanel('descriptive_text'),
        FieldPanel("description"),
        ImageChooserPanel('product_category_image')
    ]

    def save(self, *args, **kwargs):
        super(ProductCategory, self).save(*args, **kwargs)

        # Find all Category pages
        category_pages = Page.objects.type(ProductCategoryPage).specific()
        # If the ProductParentPage doesn't exist yet create it
        if not Page.objects.type(ProductParentPage):
            parent_page = ProductParentPage(title='Products')
            home = Page.objects.get(id=3)
            home.add_child(instance=parent_page)
            parent_page.save_revision().publish()
        else:
            parent_page = Page.objects.type(ProductParentPage)[0]

        # If category page already exists do nothing
        for p in category_pages:
            if p.category == self:
                return
        # If the category has no page create it
        category_page = ProductCategoryPage(
            title=self.category_name, category=self)
        parent_page.add_child(instance=category_page)
        category_page.save_revision().publish()


class Product(models.Model):
    """An admin model for individual products.
    The save method has been extended to automatically create a product page upon save."""
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

    panels = [
        FieldPanel('category'),
        FieldPanel('product_name'),
        FieldPanel('price'),
        ImageChooserPanel('product_image')
    ]

    def __str__(self):
        return f'{self.product_name}, costing £{self.price}'

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        # If product page already exists do nothing
        product_pages = Page.objects.type(ProductPage).specific()
        for product_p in product_pages:
            if product_p.product == self:
                return

        # find category page
        category_pages = Page.objects.type(ProductCategoryPage).specific()
        for p in category_pages:
            if p.category == self.category:
                category_page = p

        # If the product has no page create it
        product_page = ProductPage(title=self.product_name, product=self)
        category_page.add_child(instance=product_page)
        category_page.save_revision().publish()


class ProductParentPage(Page):
    """An empty page to simply serve to organise all products under one heading."""
    template = '404.html'
    # pages are auto generated don't allow the user access
    parent_page_types = []
    sub_page_types = []
    max_count = 1


class ProductPage(Page):
    """A detail page for an individial product"""
    template = 'products/product_page.html'

    # pages are auto generated don't allow the user access
    parent_page_types = []
    sub_page_types = []

    product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True
    )


class ProductCategoryPage(Page):
    """A page that serves as a list view for a product category."""
    template = 'products/product_category_page.html'

    # pages are auto generated don't allow the user access
    parent_page_types = []
    sub_page_types = []

    category = models.ForeignKey(
        'ProductCategory',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['products'] = Product.objects.filter(category=self.category)
        return context
