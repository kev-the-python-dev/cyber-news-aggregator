# Generated by Django 4.0.4 on 2022-05-27 03:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_headline_unique_together_alter_headline_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='headline',
            unique_together={('title', 'image', 'date', 'url')},
        ),
    ]
