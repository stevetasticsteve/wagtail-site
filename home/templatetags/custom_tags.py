import string
import random

from django import template
from wagtail.core.models import Collection
from wagtail.images.models import Image

register = template.Library()


@register.simple_tag
def get_pictures(collection_id):
    collection = Collection.objects.get(id=collection_id)
    return Image.objects.filter(collection=collection)


@register.simple_tag
def generate_random_id():
    value = ''.join(random.choice(string.ascii_letters + string.digits)
                    for n in range(20))
    return "cr-{}".format(value)
