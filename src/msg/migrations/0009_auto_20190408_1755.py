# Generated by Django 2.2 on 2019-04-08 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msg', '0008_auto_20190408_1446'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thread',
            options={'ordering': ['-created_at']},
        ),
    ]
