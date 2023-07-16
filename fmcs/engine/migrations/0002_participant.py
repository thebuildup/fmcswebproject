# Generated by Django 4.2.2 on 2023-07-16 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='engine.tournament')),
            ],
        ),
    ]
