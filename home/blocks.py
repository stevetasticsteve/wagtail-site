from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Collection
from django import forms
from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock


class ParagraphBlock(blocks.StructBlock):
    """
    Single column rich text block
    """
    text = blocks.RichTextBlock(
        help_text="Text to display"
    )

    class Meta:
        template = "streams/paragraph_block.html"
        icon = "edit"
        label = "Paragraph"
        help_text = "Formatted text to make up paragraphs"


class VideoBlock(blocks.StructBlock):
    """
    An embeddable video block.
    """
    video = EmbedBlock(
        help_text="Embed a video from Youtube"
    )
    caption = blocks.CharBlock(
        max_length=50,
        required=False,
        help_text="Optional caption for video")

    class Meta:
        template = "streams/embed_block.html"
        icon = "media"
        label = "Video Embed"
        help_text = "Embed a video"


class DownloadBlock(blocks.StructBlock):
    """
    Link to a file that can be downloaded.
    """
    button_title = blocks.CharBlock(
        max_length=25,
        required=True,
        help_text="Text to go on download button")
    downloadable_file = DocumentChooserBlock(
        required=True,
        help="Document to download"
    )

    class Meta:
        template = 'streams/download_block.html'
        icon = 'download'
        help_text = 'Display a button that downloads a file'


class QuoteBlock(blocks.StructBlock):
    """
    A <blockquote>.
    """
    text = blocks.TextBlock(
        required=True,
        rows=4,
        label='Quote Text',
    )
    author = blocks.CharBlock(
        required=False,
        max_length=255,
        label='Author',
    )

    class Meta:
        template = 'streams/quote_block.html'
        icon = 'openquote'
        label = 'Quote'
        help_text = 'A quotation'


class CollectionChooserBlock(blocks.FieldBlock):
    """
    Enables choosing a wagtail Collection in the streamfield.
    """
    target_model = Collection
    widget = forms.Select

    def __init__(self, required=False, label=None, help_text=None, *args, **kwargs):
        self._required = required
        self._help_text = help_text
        self._label = label
        super().__init__(*args, **kwargs)

    @property  # perhaps use from django.utils.functional import cached_property
    def field(self):
        return forms.ModelChoiceField(
            queryset=self.target_model.objects.all().order_by('name'),
            widget=self.widget,
            required=self._required,
            label=self._label,
            help_text=self._help_text,
        )

    def to_python(self, value):
        """
        Convert the serialized value back into a python object.
        """
        if isinstance(value, int):
            return self.target_model.objects.get(pk=value)
        return value

    def get_prep_value(self, value):
        """
        Serialize the model in a form suitable for wagtail's JSON-ish streamfield
        """
        if isinstance(value, self.target_model):
            return value.pk
        return value


class ImageGalleryBlock(blocks.StructBlock):
    """
    Show a collection of images with interactive previews that expand to
    full size images in a modal.
    """
    collection = CollectionChooserBlock(
        required=True,
        label='Image Collection',
    )

    class Meta:
        template = 'streams/image_gallery_block.html'
        icon = 'image'
        label = 'Image Gallery'
        help_text = 'Include an image gallery built from a collection of images. Collections are set in settings/collections'


class TableBlock(blocks.StructBlock):
    """
    A simple table.
    """
    table = WagtailTableBlock()

    class Meta:
        template = 'streams/table_block.html'
        icon = 'table'
        label = 'Table'
        help_text = 'Insert a table'


class GoogleMapBlock(blocks.StructBlock):
    """
    An embedded Google map in an <iframe>.
    """
    search = blocks.CharBlock(
        required=True,
        max_length=255,
        label='Location',
        help_text='Address or search term used to find your location on the map.',
    )

    class Meta:
        template = 'streams/google_map.html'
        icon = 'fa-map'
        label = 'Google Map'
        help_text = "Embed a Google map centered on the place specified."


class ColumnBlock(blocks.StructBlock):
    """
    Renders a row of md-6 columns.
    """
    # todo coudn't find a way to avoid circular name errors, so copy pasted here
    local_blocks = (
        ('paragraph', ParagraphBlock()),
        ('video', VideoBlock()),
        ('download', DownloadBlock()),
        ('quote', QuoteBlock()),
        ('image_gallery', ImageGalleryBlock()),
        ('table', TableBlock()),
        ('map', GoogleMapBlock()),
    )

    class Meta:
        template = 'streams/two_column_block.html'
        icon = 'fa-columns'
        label = '2 Column block'

    def __init__(self, local_blocks=local_blocks, min_num=2, max_num=2, **kwargs):
        local_blocks = (('content', blocks.StreamBlock(
            local_blocks, label='Content')),)
        super().__init__(local_blocks,)


def single_column_blocks():
    """Function to return all block types suitable for full width"""
    single_column_blocks = [
        ('column_block', ColumnBlock()),
        ('paragraph', ParagraphBlock()),
        ('video', VideoBlock()),
        ('download', DownloadBlock()),
        ('quote', QuoteBlock()),
        ('image_gallery', ImageGalleryBlock()),
        ('table', TableBlock()),
        ('map', GoogleMapBlock()),
    ]
    return single_column_blocks


full_streamfield = StreamField(single_column_blocks(), null=True, blank=True)
