from django.db import models

from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel)
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.models import Orderable
from wagtail.contrib.settings.models import BaseSetting, register_setting


class AboutPage(Page):
    text = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('text', classname='full'),
    ]
