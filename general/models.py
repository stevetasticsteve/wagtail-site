from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from home import blocks


class GeneralPage(Page):
    parent_page_types = ["home.HomePage", "general.GeneralPage"]
    body = StreamField([
        ('paragraph', blocks.ParagraphBlock()),
        ('text_and_image', blocks.TextImageBlock()),
        ('video', blocks.VideoBlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel("body")
    ]
