# Generated by Django 5.0.2 on 2024-02-27 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('points', models.IntegerField(default=2)),
                ('open', models.BooleanField(default=False)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('banned', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-date_updated'],
            },
        ),
    ]
