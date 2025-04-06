# Generated by Django 4.2.11 on 2024-03-27 20:20

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('tagline', models.CharField(max_length=200, unique=True)),
                ('first_brewed', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('beer_image', models.URLField()),
                ('abv', models.FloatField()),
                ('food_pairing', models.JSONField()),
                ('avg_rating', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beer_name', models.CharField(max_length=200, unique=True)),
                ('brewery_name', models.CharField(blank=True, max_length=200, null=True)),
                ('image', cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image')),
                ('abv', models.FloatField()),
                ('first_brewed', models.CharField(max_length=200)),
                ('comments', models.TextField()),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
