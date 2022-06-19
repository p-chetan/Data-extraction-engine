# Generated by Django 3.2.5 on 2021-09-23 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scraper', '0013_investwithbuzz'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buzz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=200)),
                ('DXpath', models.CharField(max_length=1000)),
                ('BXpath', models.CharField(max_length=1000)),
                ('col', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='InvestwithBuzz',
        ),
    ]