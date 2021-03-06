# Generated by Django 2.2 on 2019-08-28 16:00

import catalogs.models
from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0014_auto_20190711_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='background_image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, upload_to=catalogs.models.catalog_bg_photo_upload_path),
        ),
    ]
