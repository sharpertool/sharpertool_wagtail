from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.core.models import Orderable


class HomePage(Page):
    tagline = models.CharField(max_length=120, default='')

    content_panels = [
        FieldPanel('tagline'),
        InlinePanel('highlights', label="Highlight Item")
    ]


class HomePageHighlight(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='highlights')
    name = models.CharField(max_length=30)
    link = models.URLField()
    text = RichTextField()

    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
        FieldPanel('text', classname='full')
    ]


