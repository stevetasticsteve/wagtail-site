import re
import string
import random

from django import template
from wagtail.core.models import Collection
from wagtail.images.models import Image
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_pictures(collection_id):
    collection = Collection.objects.get(id=collection_id)
    return Image.objects.filter(collection=collection)


@register.simple_tag
def generate_random_id():
    value = "".join(
        random.choice(string.ascii_letters + string.digits) for n in range(20)
    )
    return "cr-{}".format(value)


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


@register.filter(name="embedurl")
def get_embed_url_with_parameters(url):
    if "youtube.com" in url or "youtu.be" in url:
        # Get video id from URL
        regex = (
            r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"
        )
        embed_url = re.sub(
            regex, r"https://www.youtube.com/embed/\1", url
        )  # Append video id to desired URL
        embed_url_with_parameters = embed_url + "?rel=0"  # Add additional parameters
        return embed_url_with_parameters
    else:
        return None
