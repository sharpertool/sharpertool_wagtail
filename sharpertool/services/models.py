from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.core.models import Orderable
from wagtail.contrib.settings.models import BaseSetting


class ServicesPage(Page):
    tagline = models.CharField(max_length=120, default='')

    content_panels = Page.content_panels + [
        FieldPanel('tagline'),
        InlinePanel('services', label="Service Item")
    ]

class ServiceItem(Orderable):
    page = ParentalKey(ServicesPage,
                       on_delete=models.CASCADE,
                       related_name='services')
    name = models.CharField(max_length=30)
    short_description = models.CharField(max_length=200,
                                         null=True, blank=True)
    link = models.URLField(blank=True, null=True)
    text = RichTextField()
    text2 = RichTextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    graphic = models.CharField(max_length=200,
                               null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('graphic'),
        FieldPanel('short_description'),
        FieldPanel('link'),
        FieldPanel('text', classname='full'),
        FieldPanel('code'),
        FieldPanel('text2', classname='full'),
    ]

