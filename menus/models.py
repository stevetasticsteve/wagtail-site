from django.db import models
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.core.models import Orderable

from django_extensions.db.fields import AutoSlugField


class MenuItem(Orderable):
    link_title = models.CharField(
        blank=True,
        max_length=50,
        help_text="Optional. Default link title will be the page tile, you can overwrite this."
        )
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        help_text="Link to a page on this site.",
        related_name='+',
        on_delete=models.CASCADE,
    )
    link_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Optional. Link to an external page. Internal pages will always take priority if both are set."
        ) 
    open_in_new_tab = models.BooleanField(
        default=False,
        blank=True,
        help_text="Should the page open in a new tab?"
        )

    panels = [
        FieldPanel("link_title"),
        PageChooserPanel("link_page"),
        FieldPanel("link_url"),
        FieldPanel("open_in_new_tab"),
    ]

    page = ParentalKey("Menu", related_name="menu_items")

    @property
    def link(self) -> str:
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return "#"

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return "Missing Title"


class Menu(ClusterableModel):

    title = models.CharField(
        max_length=100,
        help_text='The name you want to give to this menu.'
    )
    slug = AutoSlugField(
        populate_from="title",
        editable=True,
        help_text="The name used internally in html templates to include the menu."
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("menu_items", label="Menu Item"),
    ]

    def __str__(self):
        return self.title
