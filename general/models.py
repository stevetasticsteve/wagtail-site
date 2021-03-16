from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel, FieldPanel

from home import blocks


class GeneralPage(Page):
    parent_page_types = ["home.HomePage", "general.GeneralPage"]
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
