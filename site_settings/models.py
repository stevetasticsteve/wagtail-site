from django.db import models
from django.core.exceptions import ValidationError

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
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
    disqus_site_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Write a valid disqus shortname here to enable comments on the site. https://disqus.com/"
    )

    panels = [
        ImageChooserPanel('logo'),
        FieldPanel('site_copyright'),
        FieldPanel('disqus_site_name'),
    ]

@register_setting
class FooterLink(BaseSetting):
    footer_btn_page = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        related_name='+',
        help_text='Select an internal site page',
        on_delete=models.SET_NULL,
    )
    footer_btn_link = models.URLField(
        blank=True,
        null=True,
        help_text="Optional link to that will prominantly display in the site's footer",
        verbose_name="Footer button link",
    )
    footer_btn_text = models.CharField(
        max_length=50,
        default="Find out more",
        blank=True,
        null=False,
        help_text="Text for the optional footer link."
    )
    panels = [
        PageChooserPanel("footer_btn_page"),
        FieldPanel('footer_btn_link'),
        FieldPanel('footer_btn_text'),
    ]

    def clean(self):
        super().clean()

        if self.footer_btn_page and self.footer_btn_link:
            # Both fields are filled out
            raise ValidationError({
                'footer_btn_page': ValidationError("Please only select a page OR enter an external URL"),
                'footer_btn_link': ValidationError("Please only select a page OR enter an external URL"),
            })

        if not self.footer_btn_page and not self.footer_btn_link:
            raise ValidationError({
                'footer_btn_page': ValidationError("You must always select a page OR enter an external URL"),
                'footer_btn_link': ValidationError("You must always select a page OR enter an external URL"),
            })

      
@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(
        blank=True,
        help_text='Enter your Facebook URL'
    )
    twitter = models.URLField(
        blank=True,
        help_text='Enter your Twitter URL'
    )
    youtube = models.URLField(
        blank=True,
        help_text='Enter your YouTube URL'
    )
    instagram = models.URLField(
        blank=True,
        help_text='Enter your Instagram URL'
    )

    panels = [
        FieldPanel("facebook"),
        FieldPanel("twitter"),
        FieldPanel("youtube"),
        FieldPanel("instagram"),
    ]