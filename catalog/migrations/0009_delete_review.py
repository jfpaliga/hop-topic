# Generated by Django 4.2.11 on 2024-03-24 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_review_author_alter_review_beer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]
