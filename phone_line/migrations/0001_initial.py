# Generated by Django 4.1.5 on 2023-01-08 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('brand', models.CharField(max_length=40)),
                ('number', models.JSONField(blank=True, null=True, verbose_name=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=30)),
                ('problem', models.TextField()),
                ('description_status_cancel', models.TextField()),
                ('description', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('accept_time', models.DateTimeField()),
                ('finished_time', models.DateTimeField()),
                ('cancel_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('finished', 'Finished'), ('wating', 'Wating'), ('accept', 'Accept'), ('cancel', 'Cancel')], max_length=14)),
                ('phone_number', models.CharField(max_length=20)),
                ('type_phone', models.CharField(choices=[('internal', 'Internal'), ('city', 'City')], max_length=8)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='phone_line.part')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
