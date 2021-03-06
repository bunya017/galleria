# Generated by Django 2.2 on 2019-06-30 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0011_auto_20190630_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='catalogs.Catalog')),
            ],
            options={
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
            },
        ),
        migrations.CreateModel(
            name='CollectionProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogs.Collection')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogs.ProductEntry')),
            ],
            options={
                'verbose_name': 'Collction Product',
                'verbose_name_plural': 'collection Products',
                'unique_together': {('product', 'collection')},
            },
        ),
        migrations.AddField(
            model_name='collection',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='collection_products', through='catalogs.CollectionProduct', to='catalogs.ProductEntry'),
        ),
        migrations.AlterUniqueTogether(
            name='collection',
            unique_together={('name', 'catalog')},
        ),
    ]
