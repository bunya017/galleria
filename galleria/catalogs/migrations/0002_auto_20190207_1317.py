# Generated by Django 2.1.5 on 2019-02-07 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('photo', models.ImageField(blank=True, upload_to='uploads/')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='catalog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='catalogs.Catalog'),
        ),
        migrations.AlterField(
            model_name='productentry',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_entries', to='catalogs.Category'),
        ),
        migrations.AlterField(
            model_name='productentry',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='catalogs.ProductEntry'),
        ),
    ]
