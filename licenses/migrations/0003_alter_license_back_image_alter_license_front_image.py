# Generated by Django 4.2.10 on 2024-03-25 17:11

from django.db import migrations, models
import licenses.utils


class Migration(migrations.Migration):

    dependencies = [
        ('licenses', '0002_license_back_image_license_front_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='back_image',
            field=models.ImageField(blank=True, help_text='Upload the back image of the license.', null=True, upload_to=licenses.utils.path_and_rename),
        ),
        migrations.AlterField(
            model_name='license',
            name='front_image',
            field=models.ImageField(blank=True, help_text='Upload the front image of the license.', null=True, upload_to=licenses.utils.path_and_rename),
        ),
    ]
