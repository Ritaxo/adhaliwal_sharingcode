# Generated by Django 3.0.3 on 2020-05-03 05:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0002_auto_20200220_2001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)])),
                ('feedback', models.TextField(blank=True, max_length=200)),
                ('coder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.Coder')),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='share.Script')),
            ],
            options={
                'unique_together': {('coder', 'script')},
            },
        ),
    ]
