# Generated by Django 4.2.11 on 2024-05-06 15:49

import advertising.utils
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='UUID of the advertisement', primary_key=True, serialize=False)),
                ('photo', models.ImageField(help_text='Photo for the advertisement', upload_to=advertising.utils.path_and_rename)),
                ('url', models.URLField(help_text='URL linked from the advertisement')),
                ('alternate_name', models.CharField(help_text='Alternate name for the advertisement', max_length=255)),
                ('priority', models.IntegerField(default=0, help_text='Priority of the advertisement')),
            ],
            options={
                'verbose_name': 'Advertisement',
                'verbose_name_plural': 'Advertisements',
            },
        ),
    ]
