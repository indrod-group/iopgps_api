# Generated by Django 4.2.7 on 2024-01-29 22:14

from django.db import migrations, models
import vehicles.validators


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicletype',
            name='engine_displacement',
            field=models.DecimalField(blank=True, decimal_places=3, default='0.0', help_text='Engine displacement of the vehicle', max_digits=5),
        ),
        migrations.AddField(
            model_name='vehicletype',
            name='fuel_value',
            field=models.DecimalField(blank=True, decimal_places=4, default='0.0', help_text='Fuel value for the vehicle', max_digits=6),
        ),
        migrations.AddField(
            model_name='vehicletype',
            name='vehicle_type',
            field=models.CharField(choices=[('car', 'Car'), ('truck', 'Truck')], default='car', help_text='Type of the vehicle', max_length=31),
        ),
        migrations.AlterField(
            model_name='battery',
            name='registration_date',
            field=models.PositiveBigIntegerField(default=1706566445, help_text='The date the item was registered'),
        ),
        migrations.AlterField(
            model_name='tire',
            name='manufacturing_code',
            field=models.CharField(help_text='The manufacturing code of the tire.', max_length=18, validators=[vehicles.validators.validate_dot_code], verbose_name='Manufacturing code'),
        ),
        migrations.AlterField(
            model_name='tire',
            name='registration_date',
            field=models.PositiveBigIntegerField(default=1706566445, help_text='The date the item was registered'),
        ),
        migrations.AlterField(
            model_name='vehiclestatus',
            name='status_updated_at',
            field=models.PositiveBigIntegerField(default=1706566445, help_text='The date the status was updated'),
        ),
        migrations.AlterField(
            model_name='vehicletype',
            name='fuel_type',
            field=models.CharField(choices=[('Gasoline', 'Gasoline'), ('Diesel', 'Diesel'), ('Gas', 'Gas'), ('Electric', 'Electric')], default='Gasoline', help_text='Type of fuel used by the vehicle', max_length=31),
        ),
    ]
