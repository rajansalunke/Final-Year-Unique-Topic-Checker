# Generated by Django 5.0.1 on 2024-03-23 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('abstract', models.TextField()),
                ('algorithm', models.TextField()),
                ('methodology', models.TextField()),
                ('results', models.TextField()),
            ],
        ),
    ]