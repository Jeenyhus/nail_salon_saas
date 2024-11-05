# Generated by Django 5.1.3 on 2024-11-05 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='service',
            name='duration',
        ),
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='service_images/'),
        ),
    ]