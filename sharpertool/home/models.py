from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.core.models import Orderable
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class SiteSettings(BaseSetting):
    maps_api_key = models.CharField(
        max_length=256, help_text='Google Maps API Key for contact area',
        default=''
    )


class HomePage(Page):
    tagline = models.CharField(max_length=120, default='')

    content_panels = Page.content_panels + [
        FieldPanel('tagline'),
        InlinePanel('highlights', label="Highlight Item")
    ]


class HomePageHighlight(Orderable):
    page = ParentalKey(HomePage,
                       on_delete=models.CASCADE,
                       related_name='highlights')
    name = models.CharField(max_length=30)
    link = models.URLField()
    text = RichTextField()
    graphic = models.CharField(max_length=200,
                               null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
        FieldPanel('text', classname='full'),
        FieldPanel('graphic'),
    ]


