# Generated by Django 4.2.6 on 2023-11-03 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jewelGleamer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
