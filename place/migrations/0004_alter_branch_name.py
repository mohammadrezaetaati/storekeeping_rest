# Generated by Django 4.1.5 on 2023-01-08 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0003_alter_branch_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]