# Generated by Django 4.0.3 on 2022-06-02 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='Conversation',
            new_name='conversation',
        ),
    ]
