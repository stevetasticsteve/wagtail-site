from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock

class ParagraphBlock(blocks.StructBlock):
    text = blocks.RichTextBlock(
        help_text="Text to display"
    )

    class Meta:
        template = "streams/paragraph_block.html"
        icon = "edit"
        label = "Paragraph"
        help_text = "Formatted text to make up paragraphs"


class TextImageBlock(blocks.StructBlock):
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
