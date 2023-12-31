# Generated by Django 4.2.4 on 2023-09-05 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Premium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_platinum', models.BooleanField(default=False)),
                ('is_gold', models.BooleanField(default=False)),
                ('is_diamond', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('starting_date', models.DateField()),
                ('ending_date', models.DateField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.member')),
            ],
        ),
    ]
