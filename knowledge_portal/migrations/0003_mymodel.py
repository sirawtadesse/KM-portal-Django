# Generated by Django 5.0.3 on 2024-04-03 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_portal', '0002_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
        ),
    ]
