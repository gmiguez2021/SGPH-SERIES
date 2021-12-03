# Generated by Django 3.2.2 on 2021-11-23 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0003_alter_pricelist_dia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricelist',
            name='desc',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, verbose_name='Descuento %'),
        ),
        migrations.AlterField(
            model_name='pricelist',
            name='dia',
            field=models.IntegerField(blank=True, null=True, verbose_name='Plazo de Pago'),
        ),
        migrations.AlterField(
            model_name='pricelist',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Titulo'),
        ),
    ]