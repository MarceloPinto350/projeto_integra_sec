# Generated by Django 4.2.13 on 2024-07-16 00:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('seguranca', '0015_servico_tipomodelodocumento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelodocumento',
            name='arquivo',
            field=models.FileField(default=django.utils.timezone.now, upload_to='documentos/', verbose_name='Arquivo'),
            preserve_default=False,
        ),
    ]
