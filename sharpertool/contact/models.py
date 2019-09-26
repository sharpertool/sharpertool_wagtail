from django.db import models

from django.shortcuts import render
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.core.models import Orderable
from wagtail.contrib.settings.models import BaseSetting, register_setting


class ContactPage(Page):
    tagline = models.CharField(max_length=120, default='')

    content_panels = Page.content_panels + [
        FieldPanel('tagline'),
    ]

    def serve(self, request):
        from .forms import ContactForm

        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                contact = form.save()

                # ToDo: Send email, validate!
                return render(request, 'contact/thank_you.html', {
                    'page': self,
                    'contact': contact,
                })
        else:
            form = ContactForm()

        return render(request, 'contact/contact_page.html', {
            'page': self,
            'form': form,
        })


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    project_name = models.CharField(max_length=120)
    project_description = models.TextField(max_length=4096)


