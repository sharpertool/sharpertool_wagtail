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
            InlinePanel('project_item'),
        ], heading='Project Work Items', classname='collapsible collapsed'),
        MultiFieldPanel([
            InlinePanel('education', heading='Educational Items'),
            InlinePanel('skills', heading='Skills'),
            InlinePanel('experience', heading='Experience Items'),
        ], heading='Education and Experience', classname='collapsible collapsed'),
        MultiFieldPanel([
            FieldPanel('contact_info'),
            FieldPanel('contact_email', heading="Enter value if different from main email"),
            FieldPanel('contact_longitude', heading='Longitude of Contact location'),
            FieldPanel('contact_latitude', heading='Latitude of Contact location'),
        ], heading='Contacts', classname="collapsible collapsed"),
        MultiFieldPanel([
            InlinePanel('blog_entries')
        ], heading='Blog Entries', classname="collapsible collapsed")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        return context


class ResumeProjectItem(Orderable):

    SECTION_CHOICES = (
        ('webdesign', 'Web Design',),
        ('engineering', 'Engineering',),
        ('edatools', 'EDA Tools'),
    )

    page = ParentalKey(ResumePage, on_delete=models.CASCADE, related_name='project_item')
    section = models.CharField(choices=SECTION_CHOICES, max_length=20, null=True, blank=True)
    title = models.CharField(max_length=40)
    subtext = models.CharField(max_length=80, null=True, blank=True)
    thumb = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('section'),
        FieldPanel('title'),
        FieldPanel('subtext'),
        ImageChooserPanel('image', heading='Large image for lightbox'),
        ImageChooserPanel('thumb', heading='thumbnail image'),
    ]


class EducationItem(Orderable):
    page = ParentalKey(ResumePage, on_delete=models.CASCADE, related_name='education')
    title = models.CharField(max_length=120, null=True, blank=True)
    start = models.CharField(max_length=20, null=True, blank=True)
    end = models.CharField(max_length=20, null=True, blank=True)
    text = RichTextField(null=True, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('start', heading='Start month-year, or just year'),
        FieldPanel('end', heading='End month-year, or just year'),
        FieldPanel('text'),
    ]


class Skills(Orderable):
    page = ParentalKey(ResumePage, on_delete=models.CASCADE, related_name='skills')
    title = models.CharField(max_length=120, null=True, blank=True)
    percent = models.CharField(max_length=5, null=True, blank=True)
    details = RichTextField(null=True, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('percent', heading='A percent value from 0-100, format: 56%'),
        FieldPanel('details', heading='Provide some justification on your percentage'),
    ]


class Experience(Orderable):
    page = ParentalKey(ResumePage, on_delete=models.CASCADE, related_name='experience')
    title = models.CharField(max_length=120, null=True, blank=True)
    start = models.CharField(max_length=20, null=True, blank=True)
    end = models.CharField(max_length=20, null=True, blank=True)
    text = RichTextField(null=True, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('start', heading='Start month-year, or just year'),
        FieldPanel('end', heading='End month-year, or just year'),
        FieldPanel('text'),
    ]


class ResumeBlog(Orderable):
    page = ParentalKey(ResumePage, on_delete=models.CASCADE, related_name='blog_entries')
    title = models.CharField(max_length=120, null=True, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    text = RichTextField(null=True, blank=True)

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('image', heading='Large image for lightbox'),
        FieldPanel('text'),
    ]
