# Generated by Django 3.2.5 on 2021-08-02 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_rename_email_new_row'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new',
            name='date',
        ),
    ]
