# Generated by Django 3.1.7 on 2021-02-25 17:14

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalpage',
            name='body',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.RichTextBlock(help_text='Text to display', required=False))])), ('text_and_image', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.RichTextBlock(help_text='Text to display', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image will be resized to 570x370px'))]))], blank=True, null=True),
        ),
    ]