from django import template
from wagtail.core.models import Site

register = template.Library()

@register.simple_tag()
def get_menu_pages():
    site = Site.objects.get(is_default_site=True)
    home_page = site.root_page
    menu_pages = home_page.get_children().live().in_menu()

    return menu_pages
    