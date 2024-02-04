# Generated by Django 4.2.6 on 2023-11-03 03:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField(default=0)),
                ('details', models.TextField()),
                ('description', models.TextField()),
                ('materials', models.TextField()),
                ('urls', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField(default=0)),
                ('url', models.CharField(max_length=200)),
                ('author', models.CharField(default='Sindhu')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('details', models.TextField(default='Made in 14k solid gold, the alloy gives our pieces its beautiful, subtle hue. Band Thickness: 1.0 mm')),
                ('description', models.TextField(default='The Stacker is the white tee of rings. It is everyone go-to because there is nothing it cant go with. This 14k solid gold essential is the perfect starter ring or addition to anyone collection.')),
                ('materials', models.TextField(default='14k Solid Gold Our 14k solid gold pieces are made to last forever. 14k gold will not oxidize or discolor, so you can wear your jewelry every day.')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
            ],
        ),
    ]
