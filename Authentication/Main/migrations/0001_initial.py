# Generated by Django 3.2.5 on 2021-08-11 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('refresh_token', models.TextField()),
                ('access_token', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expiry', models.DateTimeField()),
            ],
        ),
    ]
