# Generated by Django 3.2.25 on 2025-03-27 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='assistants',
            field=models.ManyToManyField(blank=True, related_name='assigned_doctors', to='hospital.Assistant'),
        ),
        migrations.AddField(
            model_name='treatmentapplication',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.doctor'),
        ),
    ]
