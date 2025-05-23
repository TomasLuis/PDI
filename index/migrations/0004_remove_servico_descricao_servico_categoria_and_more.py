# Generated by Django 5.1.7 on 2025-04-16 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_servico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servico',
            name='descricao',
        ),
        migrations.AddField(
            model_name='servico',
            name='categoria',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='servico',
            name='contacto',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='servico',
            name='distrito',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='servico',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='servico',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='servicos/'),
        ),
        migrations.AddField(
            model_name='servico',
            name='informacoes_adicionais',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='servico',
            name='nome',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servico',
            name='prestador',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
