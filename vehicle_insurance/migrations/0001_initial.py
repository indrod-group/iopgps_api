# Generated by Django 4.2.11 on 2024-05-06 15:31

from django.db import migrations, models
import django.db.models.deletion
import licenses.validators
import uuid
import vehicles.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicles', '0005_vehicle_front_photo_vehicle_heavy_transport_permit_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrokerInfo',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, help_text='UUID of the broker info', primary_key=True, serialize=False)),
                ('insurance_document', models.FileField(blank=True, help_text='Insurance document of the vehicle', null=True, upload_to=vehicles.utils.path_and_rename)),
                ('issue_date', models.DateField(help_text='Issue date of the insurance document', validators=[licenses.validators.validate_issue_date])),
                ('expiry_date', models.DateField(help_text='Expiry date of the insurance document', validators=[licenses.validators.validate_license_validity])),
                ('insurance_company', models.CharField(help_text='Name of the insurance company', max_length=255)),
                ('broker_name', models.CharField(help_text='Name of the broker', max_length=255)),
                ('vehicle', models.ForeignKey(help_text='The vehicle that this broker info belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='broker_infos', to='vehicles.vehicle')),
            ],
            options={
                'verbose_name': 'Broker Info',
                'verbose_name_plural': 'Broker Infos',
            },
        ),
    ]
