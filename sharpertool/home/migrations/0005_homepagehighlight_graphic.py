# Generated by Django 2.2.3 on 2019-09-26 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_sitesettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagehighlight',
            name='graphic',
            field=models.URLField(blank=True, null=True),
        ),
    ]
