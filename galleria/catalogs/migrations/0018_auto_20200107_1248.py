# Generated by Django 2.2.9 on 2020-01-07 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0017_auto_20200105_1204'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collectionproduct',
            options={'verbose_name': 'Collection Product', 'verbose_name_plural': 'Collection Products'},
        ),
        migrations.AlterModelOptions(
            name='featuredproducts',
            options={'verbose_name': 'Featured Products', 'verbose_name_plural': 'Featured Products'},
        ),
    ]
