from django.db import models

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


@register_setting
class GlobalSiteSettings(BaseSetting):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        help_text='Logo image for the website header',
        on_delete=models.SET_NULL,
    )
    site_copyright = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="The copyright owner to be displayed on the site footer. Don't enter the © symbol"
    )

    panels = [
        ImageChooserPanel('logo'),
        FieldPanel('site_copyright'),
    ]
