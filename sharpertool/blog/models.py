from django.db import models

from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel)
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.models import Orderable
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


class BlogPage(Page):
    tagline = models.CharField(max_length=120, default='')

    content_panels = Page.content_panels + [
        FieldPanel('tagline'),
    ]
