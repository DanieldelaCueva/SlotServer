# Generated by Django 4.0.4 on 2022-06-22 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_useradditionaldata_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='useradditionaldata',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]