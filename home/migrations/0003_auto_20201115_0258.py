# Generated by Django 3.1.2 on 2020-11-14 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_conversationmessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversationmessage',
            old_name='applications',
            new_name='application',
        ),
    ]
