# Generated by Django 5.0.3 on 2024-04-04 08:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_portal', '0003_mymodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
