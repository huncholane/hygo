# Generated by Django 4.1.7 on 2023-03-30 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_account_access_token_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='sp_id',
        ),
    ]
