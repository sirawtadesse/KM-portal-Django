# Generated by Django 5.0.2 on 2024-05-01 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_portal', '0013_category_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
            ],
        ),
    ]
