# Generated by Django 3.2.7 on 2023-06-14 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='description',
            new_name='descriptions',
        ),
    ]
