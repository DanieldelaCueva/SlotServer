# Generated by Django 4.0.4 on 2022-06-02 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slotstreamer', '0002_rename_slots_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='room_id',
            field=models.CharField(default='test_room', max_length=254),
        ),
    ]
