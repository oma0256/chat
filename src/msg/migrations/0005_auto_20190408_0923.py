# Generated by Django 2.2 on 2019-04-08 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('msg', '0004_auto_20190408_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='msg.Thread'),
        ),
    ]
