from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.models import ParentalKey

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField

FORM_FIELD_CHOICES = (
    ('singleline', _('Single line text')),
    ('multiline', _('Multi-line text')),
    ('email', _('Email')),
    ('url', _('URL')),
    ('radio', _('Radio buttons')),
)


class CustomAbstractFormField(AbstractFormField):
    field_type = models.CharField(
        verbose_name="Field Type",
        max_length=16,
        choices=FORM_FIELD_CHOICES,
    )

    class Meta:
        abstract = True
        ordering = ["sort_order"]


class FormField(CustomAbstractFormField):
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,
        related_name='form_fields'
    )


class ContactPage(AbstractEmailForm):
    template = "contact/contact_page.html"
    landing_page_template = "contact/contact_page_landing.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = []
    max_count = 1

    intro = RichTextField(
        blank=True,
        features=["bold", "link", "ol", "li"],
    )
    thank_you_text = RichTextField(
        blank=True,
        features=["bold", "link", "ol", "li"],
    )
    contact_page_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text="Image will be cropped to 580px by 355px",
        related_name="+"
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        ImageChooserPanel("contact_page_image"),
        InlinePanel("form_fields", label='Form Fields'),
        FieldPanel("thank_you_text"),
        FieldPanel("from_address"),
        FieldPanel("to_address"),
        FieldPanel("subject"),
    ]
