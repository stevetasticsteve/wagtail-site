from django.db import models

from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel, MultiFieldPanel

from . import blocks


class HomePage(Page):
    parent_page_types = ["wagtailcore.Page"]
    lead_text = models.CharField(
        max_length=140,
        blank=True,
        help_text='Subheading text under the banner title',
    )

    banner_background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        help_text='The banner background image',
        on_delete=models.SET_NULL,
    )

    button = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        related_name='+',
        help_text='Select an optional page to link to',
        on_delete=models.SET_NULL,
    )
    button_text = models.CharField(
        max_length=50,
        default='Read More',
        blank=False,
        help_text='Button text',
    )

    body = body = blocks.full_streamfield

    content_panels = Page.content_panels + [
        FieldPanel("lead_text"),
        ImageChooserPanel("banner_background_image"),
        PageChooserPanel("button"),
        FieldPanel("button_text"),
        StreamFieldPanel("body"),
    ]


class GeneralPage(Page):
    parent_page_types = ["HomePage", "GeneralPage"]
    body = blocks.full_streamfield

    comments = models.BooleanField(
        default=False,
        help_text="Should comments be allowed on the page?",
        verbose_name='Enable comments?'
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body")
    ]
    promote_panels = Page.promote_panels + [
        FieldPanel('comments')
    ]

    promote_panels = [
        MultiFieldPanel(promote_panels, "Common page configuration")
    ]
