# Generated by Django 4.2.7 on 2024-01-10 04:51

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_parent_accounts_alter_role_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text="User's phone number", max_length=128, null=True, region=None)),
                ('user', models.ForeignKey(help_text='The user to whom this phone number belongs', on_delete=django.db.models.deletion.CASCADE, to='users.customuser')),
            ],
        ),
    ]
