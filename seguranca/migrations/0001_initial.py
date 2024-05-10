# Generated by Django 4.2.13 on 2024-05-09 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aplicacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, unique=True, verbose_name='Nome')),
                ('sigla', models.CharField(max_length=20, unique=True, verbose_name='Sigla')),
                ('descricao', models.TextField(max_length=1000, verbose_name='Descrição')),
                ('categoria', models.TextField(choices=[['ADMINISTRATIVA', 'Administrativa'], ['TI', 'Tecnologia da Informação'], ['JUDICIAL', 'Judicial']], default='ADMINISTRATIVA', verbose_name='Categoria')),
                ('abrangencia', models.TextField(choices=[['REGIONAL', 'Regional'], ['NACIONAL', 'Nacional'], ['CNJ', 'CNJ']], default='REGIONAL', verbose_name='Abrangência')),
                ('url_fonte', models.URLField(max_length=500, unique=True, verbose_name='URL Fonte')),
                ('data_registro', models.DateTimeField(auto_now_add=True, verbose_name='Data cadastro')),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('data_descontinuacao', models.DateTimeField(null=True, verbose_name='Data descontinuação')),
                ('essencial', models.BooleanField(default=True, verbose_name='Essencial')),
                ('estrategico', models.BooleanField(default=False, verbose_name='Estratégico')),
                ('arquitetura', models.CharField(choices=[['WEB', 'Web'], ['CLIENTE/SERVIDOR', 'Cliente/Servidor'], ['MAINFRAME', 'Mainframe']], default='WEB', max_length=20, verbose_name='Arquitetura')),
                ('hospedagem', models.CharField(choices=[['LOCAL', 'Local'], ['CLOUD', 'Cloud'], ['HÍBRIDO', 'Híbrido'], ['EXTERNO', 'Externo']], default='LOCAL', max_length=20, verbose_name='Hospedagem')),
                ('url_acesso', models.URLField(max_length=500, unique=True, verbose_name='URL Acesso')),
                ('usuario_servico', models.CharField(max_length=50, verbose_name='Usuário de serviço')),
                ('senha_servico', models.CharField(max_length=50, verbose_name='Senha de serviço')),
                ('token_acesso', models.CharField(max_length=1000, verbose_name='Token de acesso')),
                ('aplicacao_pai', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seguranca.aplicacao', verbose_name='Aplicação pai')),
            ],
            options={
                'verbose_name': 'Aplicação',
                'verbose_name_plural': 'Aplicações',
                'db_table': 'tb_aplicacao',
                'permissions': [('can_view_aplicacao', 'Can view aplicações'), ('can_change_aplicacao', 'Can change aplicações'), ('can_add_aplicacao', 'Can add aplicações'), ('can_delete_aplicacao', 'Can delete aplicações')],
            },
        ),
        migrations.CreateModel(
            name='AreaNegocial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, unique=True, verbose_name='Nome')),
                ('sigla', models.CharField(max_length=20, unique=True, verbose_name='Sigla')),
                ('id_sigep', models.CharField(max_length=5, unique=True, verbose_name='Código SIGEP')),
                ('ativa', models.BooleanField(default=True, verbose_name='Ativa')),
            ],
            options={
                'verbose_name': 'Área Negocial',
                'verbose_name_plural': 'Áreas Negociais',
                'db_table': 'tb_area_negocial',
                'permissions': [('can_view_area_negocial', 'Can view areas negociais'), ('can_change_area_negocial', 'Can change areas negociais'), ('can_add_area_negocial', 'Can add areas negociais'), ('can_delete_area_negocial', 'Can delete areas negociais')],
            },
        ),
        migrations.CreateModel(
            name='TipoAplicacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True, verbose_name='Nome')),
                ('descricao', models.TextField(max_length=1000, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Tipo de aplicação',
                'verbose_name_plural': 'Tipos de aplicação',
                'db_table': 'tb_tipo_aplicacao',
                'permissions': [('can_view_tipo_aplicacao', 'Can view tipos aplicação'), ('can_change_tipo_aplicacao', 'Can change tipos aplicação'), ('can_add_tipo_aplicacao', 'Can add tipos aplicação'), ('can_delete_tipo_aplicacao', 'Can delete tipos aplicação')],
            },
        ),
        migrations.CreateModel(
            name='TipoAtivoInfraestrutura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True)),
                ('descricao', models.TextField(max_length=1000)),
            ],
            options={
                'verbose_name': 'Tipo de Ativo de Infraestrutura',
                'verbose_name_plural': 'Tipos de Ativos de Infraestrutura',
                'db_table': 'tb_tipo_ativo_infraestrutura',
                'permissions': [('can_view_tipo_ativo_infraestrutura', 'Can view tipos ativos infraestrutura'), ('can_change_tipo_ativo_infraestrutura', 'Can change tipos ativos infraestrutura'), ('can_add_tipo_ativo_infraestrutura', 'Can add tipos ativos infraestrutura'), ('can_delete_tipo_ativo_infraestrutura', 'Can delete tipos ativos infraestrutura')],
            },
        ),
        migrations.CreateModel(
            name='ResultadoScan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultado', models.JSONField(verbose_name='Resultado')),
                ('data_resultado', models.DateTimeField(auto_now=True, verbose_name='Data da análise')),
                ('aplicacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguranca.aplicacao', verbose_name='Aplicação')),
            ],
            options={
                'verbose_name': 'Resultado da Varredura',
                'verbose_name_plural': 'Resultados da Varredura',
                'db_table': 'tb_resultado_scan',
                'permissions': [('can_view_resultado_scan', 'Can view resultados scan'), ('can_change_resultado_scan', 'Can change resultados scan'), ('can_add_resultado_scan', 'Can add resultados scan'), ('can_delete_resultado_scan', 'Can delete resultados scan')],
            },
        ),
        migrations.CreateModel(
            name='AtivoInfraestrutura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, unique=True, verbose_name='Nome')),
                ('descricao', models.TextField(max_length=1000, verbose_name='Descrição')),
                ('url_localizacao', models.URLField(verbose_name='URL localização do ativo')),
                ('endereco_ip', models.GenericIPAddressField(protocol='IPv4', verbose_name='Endereço IP')),
                ('porta_acesso', models.IntegerField(verbose_name='Porta')),
                ('usuario_acesso', models.CharField(max_length=50, verbose_name='Usuário de serviço')),
                ('senha_acesso', models.CharField(max_length=50, verbose_name='Senha do usuário de serviço')),
                ('token_acesso', models.CharField(max_length=1000, verbose_name='Token de acesso ao ativo')),
                ('status', models.CharField(choices=[['ATIVO', 'Ativo'], ['DESATIVADO', 'Desativado'], ['EM MANUTENÇÃO', 'Em manutenção']], max_length=20, verbose_name='Situação do ativo')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguranca.tipoativoinfraestrutura', verbose_name='Tipo de Ativo')),
            ],
            options={
                'verbose_name': 'Ativo de Infraestrutura',
                'verbose_name_plural': 'Ativos de Infraestrutura',
                'db_table': 'tb_ativo_infraestrutura',
                'permissions': [('can_view_ativo_infraestrutura', 'Can view ativos infraestrutura'), ('can_change_ativo_infraestrutura', 'Can change ativos infraestrutura'), ('can_add_ativo_infraestrutura', 'Can add ativos infraestrutura'), ('can_delete_ativo_infraestrutura', 'Can delete ativos infraestrutura')],
            },
        ),
        migrations.AddField(
            model_name='aplicacao',
            name='area_responsavel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguranca.areanegocial', verbose_name='Área responsável'),
        ),
        migrations.AddField(
            model_name='aplicacao',
            name='gestor_negocial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Gestor responsável'),
        ),
        migrations.AddField(
            model_name='aplicacao',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguranca.tipoaplicacao'),
        ),
        migrations.CreateModel(
            name='VersaoAplicacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_versao', models.CharField(max_length=50)),
                ('data_lancamento', models.DateField()),
                ('descricao', models.TextField()),
                ('situacao', models.CharField(choices=[['EM DESENVOLVIMENTO', 'Em desenvolvimento'], ['EM HOMOLOGAÇÃO', 'Em homologação'], ['EM IMPLANTAÇÃO', 'Em implantação'], ['IMPLANTADO', 'Implantado'], ['DESCONTINUADO', 'Descontinuado']], default='EM DESENVOLVIMENTO', max_length=20)),
                ('aplicacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguranca.aplicacao')),
            ],
            options={
                'verbose_name': 'Versão da Aplicação',
                'verbose_name_plural': 'Versões da Aplicação',
                'db_table': 'tb_versao_aplicacao',
                'permissions': [('can_view_versao_aplicacao', 'Can view versões aplicação'), ('can_change_versao_aplicacao', 'Can change versões aplicação'), ('can_add_versao_aplicacao', 'Can add versões aplicação'), ('can_delete_versao_aplicacao', 'Can delete versões aplicação')],
                'unique_together': {('aplicacao', 'numero_versao')},
            },
        ),
    ]
