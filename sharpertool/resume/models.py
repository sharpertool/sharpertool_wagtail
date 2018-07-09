from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel


class ResumePage(Page):
    heading = RichTextField(default='')
    intro = RichTextField(default='')
    name = models.CharField(max_length=128, default='')
    dob = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(default='')
    address = models.CharField(max_length=50, default='')
    website = models.URLField(null=True)
    phone = models.CharField(max_length=20, default='')
    profile_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    # Contact Information

    contact_info = RichTextField(default='')
    contact_email = models.EmailField(null=True, blank=True)
    contact_longitude = models.FloatField(null=True, blank=True)
    contact_latitude = models.FloatField(null=True, blank=True)


    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('heading'),
            FieldPanel('intro'),
            FieldPanel('name'),
            FieldPanel('dob'),
            FieldPanel('email'),
            FieldPanel('address'),
            FieldPanel('website'),
            FieldPanel('phone'),
            ImageChooserPanel('profile_image'),
        ], heading='Home Section', classname="collapsible collapsed"),
        MultiFieldPanel([
            FieldPanel('contact_info'),
            FieldPanel('contact_email', heading="Enter value if different from main email"),
            FieldPanel('contact_longitude', heading='Longitude of Contact location'),
            FieldPanel('contact_latitude', heading='Latitude of Contact location'),
        ], heading='Contacts', classname="collapsible collapsed"),
    ]
