# Generated by Django 5.0 on 2023-12-28 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_create_date_product_last_edit_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(null=True),
        ),
    ]
