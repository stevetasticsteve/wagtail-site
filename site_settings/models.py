from django.db import models

from wagtail.contrib.settings.models import BaseSetting, register_setting
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

    panels = [
        ImageChooserPanel('logo')
    ]
