from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.core.models import Orderable
from wagtail.contrib.settings.models import BaseSetting, register_setting


class AboutPage(Page):
    text = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('text', classname='full'),
    ]
