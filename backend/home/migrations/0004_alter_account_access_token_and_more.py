# Generated by Django 4.1.7 on 2023-03-29 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_account_sp_id_alter_account_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='access_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='token_expires_at',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
