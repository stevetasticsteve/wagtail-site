from django.db import models

from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel, MultiFieldPanel
from . import blocks


class HomePage(Page):
    """
    The home page of the website. Consists of a hero unit followed by optional streamfield.
    """
    parent_page_types = ["wagtailcore.Page"]
    lead_text = models.CharField(
        max_length=140,
        blank=True,
        help_text="Subheading text under the banner title",
    )

    banner_background_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        help_text="The banner background image",
        on_delete=models.SET_NULL,
    )

    button = models.ForeignKey(
        "wagtailcore.Page",
        blank=True,
        null=True,
        related_name="+",
        help_text="Select an optional page to link to",
        on_delete=models.SET_NULL,
    )
    button_text = models.CharField(
        max_length=50,
        default="Read More",
        blank=False,
        help_text="Button text",
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
    """
    A flexible page with no particular defined structure or relation to other pages.
    """
    parent_page_types = ["HomePage", "GeneralPage"]
    body = blocks.full_streamfield

    comments = models.BooleanField(
        default=False,
        help_text="Should comments be allowed on the page?",
        verbose_name="Enable comments?"
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body")
    ]
    promote_panels = Page.promote_panels + [
        FieldPanel("comments")
    ]

    promote_panels = [
        MultiFieldPanel(promote_panels, "Common page configuration")
    ]


class SeriesIndexPage(Page):
    """
    A page to act as a container for a series. Can include an overview of the series. Links to child pages automatically shown.
    """
    parent_page_types = ["GeneralPage"]
    body = blocks.full_streamfield

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)

        context["child_pages"] = self.get_children().live()
        return context


class SeriesPage(Page):
    """
    A flexible page for varied content that automatically links to sibling pages belonging to the same family. Designed for creating a series of pages on the same subject.
    """
    parent_page_types = ["SeriesIndexPage"]

    summary = models.CharField(
        max_length=250,
        help_text="A short summary to go into links.",
        blank=False,
        null=False,
    )
    body = blocks.full_streamfield

    comments = models.BooleanField(
        default=True,
        help_text="Should comments be allowed on the page?",
        verbose_name="Enable comments?"
    )

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        StreamFieldPanel("body"),
    ]
    promote_panels = Page.promote_panels + [
        FieldPanel("comments")
    ]

    promote_panels = [
        MultiFieldPanel(promote_panels, "Common page configuration")
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        context["related_pages"] = self.get_siblings().live().specific()

        return context


class CalendarPage(Page):
    """
    A page to host a google calendar embed.
    """
    parent_page_types = ["HomePage"]
    max_count = 1

    calendar_url = models.CharField(
        max_length=250,
        help_text="Enter an embed link for a Google calendar.",
        blank=False,
        null=False,
    )

    content_panels = Page.content_panels + [
        FieldPanel("calendar_url"),
    ]