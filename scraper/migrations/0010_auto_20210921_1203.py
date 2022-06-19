# Generated by Django 3.2.5 on 2021-09-21 06:33

from django.db import migrations, models
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0009_auto_20210920_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('recurrences', recurrence.fields.RecurrenceField()),
            ],
        ),
        migrations.AlterField(
            model_name='new',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]