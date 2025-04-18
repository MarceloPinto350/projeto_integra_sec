# Generated by Django 4.2.13 on 2024-06-24 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguranca', '0010_alter_versaoaplicacao_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='versaoaplicacao',
            name='data_lancamento',
            field=models.DateField(verbose_name='Data lançamento'),
        ),
        migrations.AlterField(
            model_name='versaoaplicacao',
            name='descricao',
            field=models.TextField(max_length=1000, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='versaoaplicacao',
            name='nome_versao',
            field=models.CharField(max_length=50, verbose_name='Versão'),
        ),
        migrations.AlterField(
            model_name='versaoaplicacao',
            name='situacao',
            field=models.CharField(choices=[['EM DESENVOLVIMENTO', 'Em desenvolvimento'], ['EM HOMOLOGAÇÃO', 'Em homologação'], ['EM IMPLANTAÇÃO', 'Em implantação'], ['IMPLANTADO', 'Implantado'], ['DESCONTINUADO', 'Descontinuado']], default='EM DESENVOLVIMENTO', max_length=20, verbose_name='Situação'),
        ),
    ]
