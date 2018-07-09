from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.core.models import Orderable


class ResumePage(Page):
    name = models.CharField(max_length=128, default='')

    content_panels = Page.content_panels + [
        FieldPanel('name'),
    ]
