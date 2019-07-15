from django.urls import path

from .views import ContactView

app_name = 'resume'


urlpatterns = (
    path('contact/', ContactView.as_view(), name='contact'),
)

