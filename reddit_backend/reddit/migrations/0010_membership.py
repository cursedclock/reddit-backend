# Generated by Django 3.2.8 on 2022-01-28 22:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0009_auto_20220128_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subreddit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reddit.subreddit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'subreddit')},
            },
        ),
    ]
