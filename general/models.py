from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import StreamFieldPanel

from home import blocks


class GeneralPage(Page):
    parent_page_types = ["home.HomePage", "general.GeneralPage"]
    body = blocks.full_streamfield

    content_panels = Page.content_panels + [
        StreamFieldPanel("body")
    ]
