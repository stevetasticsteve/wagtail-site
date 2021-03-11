from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Collection
from django import forms


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


class TextImageBlock(blocks.StructBlock):
    """
    A two column image and rich text block.
    """
    text = blocks.RichTextBlock(
        help_text="Text to display"
    )
    image = ImageChooserBlock(
        help_text="Image will be resized to 570x370px"
    )

    class Meta:
        template = "streams/text_image_block.html"
        icon = "code"
        label = "Text and Image"
        help_text = "Image on the left, text on the right"


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


full_streamfield = StreamField([
    ('paragraph', ParagraphBlock()),
    ('text_and_image', TextImageBlock()),
    ('video', VideoBlock()),
    ('download', DownloadBlock()),
    ('quote', QuoteBlock()),
    ('image_gallery', ImageGalleryBlock()),
], null=True, blank=True)
