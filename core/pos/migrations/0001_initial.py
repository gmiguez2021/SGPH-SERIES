# Generated by Django 3.2.2 on 2021-11-20 20:45

import datetime
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
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Marca',
                'verbose_name_plural': 'Marca',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('inventoried', models.BooleanField(default=True, verbose_name='¿Es inventariado?')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=10, unique=True, verbose_name='Teléfono')),
                ('birthdate', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de nacimiento')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Dirección')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('ruc', models.CharField(max_length=13, verbose_name='Ruc')),
                ('address', models.CharField(max_length=200, verbose_name='Dirección')),
                ('mobile', models.CharField(max_length=10, verbose_name='Teléfono celular')),
                ('phone', models.CharField(max_length=9, verbose_name='Teléfono convencional')),
                ('email', models.CharField(max_length=50, verbose_name='Email')),
                ('website', models.CharField(max_length=250, verbose_name='Página web')),
                ('desc', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción')),
                ('image', models.ImageField(blank=True, null=True, upload_to='company/%Y/%m/%d', verbose_name='Logo')),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Iva')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
                'ordering': ['-id'],
                'permissions': (('view_company', 'Can view Company'),),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='CtasCollect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('end_date', models.DateField(default=datetime.datetime.now)),
                ('debt', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('saldo', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('state', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Cuenta por cobrar',
                'verbose_name_plural': 'Cuentas por cobrar',
                'ordering': ['-id'],
                'permissions': (('view_ctascollect', 'Can view Cuentas por cobrar'), ('add_ctascollect', 'Can add Cuentas por cobrar'), ('delete_ctascollect', 'Can delete Cuentas por cobrar')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='DebtsPay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('end_date', models.DateField(default=datetime.datetime.now)),
                ('debt', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('saldo', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('state', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Cuenta por pagar',
                'verbose_name_plural': 'Cuentas por pagar',
                'ordering': ['-id'],
                'permissions': (('view_debtspay', 'Can view Cuentas por pagar'), ('add_debtspay', 'Can add Cuentas por pagar'), ('delete_debtspay', 'Can delete Cuentas por pagar')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Exemplar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.brand', verbose_name='Marca')),
            ],
            options={
                'verbose_name': 'Modelo',
                'verbose_name_plural': 'Modelos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('desc', models.CharField(blank=True, max_length=150, null=True, verbose_name='Descripcion ')),
            ],
            options={
                'verbose_name': 'Plazo de Pago',
                'verbose_name_plural': 'Plazo de Pago',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Código')),
                ('reference', models.CharField(blank=True, max_length=150, null=True, verbose_name='Referencia')),
                ('detail', models.CharField(blank=True, max_length=250, null=True, verbose_name='Detalle')),
                ('stock_maximum', models.IntegerField(default=0, verbose_name='Stock Máximo')),
                ('stock_minimum', models.IntegerField(default=0, verbose_name='Stock Mínimo')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de Compra')),
                ('pvp', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de Venta')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/%Y/%m/%d', verbose_name='Imagen')),
                ('stock', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.category', verbose_name='Categoría')),
                ('exemplar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.exemplar', verbose_name='Marca/Modelo')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=datetime.datetime.now)),
                ('end_date', models.DateField(default=datetime.datetime.now)),
                ('state', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Promoción',
                'verbose_name_plural': 'Promociones',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('ruc', models.CharField(max_length=13, unique=True, verbose_name='Ruc')),
                ('mobile', models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Dirección')),
                ('email', models.CharField(max_length=50, unique=True, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_condition', models.CharField(choices=[('contado', 'Contado'), ('credito', 'Credito')], default='contado', max_length=50)),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('end_credit', models.DateField(default=datetime.datetime.now)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.provider')),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
                'ordering': ['-id'],
                'permissions': (('view_purchase', 'Can view Compras'), ('add_purchase', 'Can add Compras'), ('delete_purchase', 'Can delete Compras')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.IntegerField(default=0)),
                ('concepto', models.CharField(max_length=150, verbose_name='Concepto')),
                ('payment_condition', models.CharField(choices=[('contado', 'Contado'), ('credito', 'Credito')], default='contado', max_length=50)),
                ('data_joined', models.DateField(default=datetime.datetime.now)),
                ('end_credit', models.DateField(default=datetime.datetime.now)),
                ('state', models.CharField(choices=[('Enviado', 'Enviado'), ('Aprobar', 'Aprobar')], default='Enviado', max_length=50)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.provider')),
            ],
            options={
                'verbose_name': 'Orden de Compra',
                'verbose_name_plural': 'Ordenes de Compra',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PurchaseRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('state', models.CharField(choices=[('Enviado', 'Enviado'), ('Aprobar', 'Aprobar')], default='Enviado', max_length=50)),
                ('concepto', models.CharField(blank=True, max_length=150, null=True, verbose_name='Concepto')),
                ('payment_condition', models.CharField(choices=[('contado', 'Contado'), ('credito', 'Credito')], default='Credito', max_length=150)),
                ('end_credit', models.DateField(default=datetime.datetime.now)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total_dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total_iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('subtotaldos', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('plazo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pos.payment')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pos.provider')),
            ],
            options={
                'verbose_name': 'Solicitud de Compra',
                'verbose_name_plural': 'Solicitudes de Compra',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_condition', models.CharField(choices=[('contado', 'Contado'), ('credito', 'Credito')], default='contado', max_length=50)),
                ('payment_method', models.CharField(choices=[('efectivo', 'Efectivo'), ('tarjeta_debito_credito', 'Tarjeta de Debito / Credito'), ('efectivo_tarjeta', 'Efectivo y Tarjeta')], default='efectivo', max_length=50)),
                ('type_voucher', models.CharField(choices=[('ticket', 'Ticket'), ('factura', 'Factura')], default='ticket', max_length=50)),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('end_credit', models.DateField(default=datetime.datetime.now)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total_dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total_iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cash', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('change', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('card_number', models.CharField(blank=True, max_length=30, null=True)),
                ('titular', models.CharField(blank=True, max_length=30, null=True)),
                ('amount_debited', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pos.client')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'ordering': ['-id'],
                'permissions': (('view_sale', 'Can view Ventas'), ('add_sale', 'Can add Ventas'), ('delete_sale', 'Can delete Ventas')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('state', models.CharField(choices=[('Realizada', 'Realizada'), ('Rechazada', 'Rechazada')], default='Realizada', max_length=100)),
                ('concepto', models.CharField(blank=True, max_length=150, null=True, verbose_name='Concepto')),
                ('payment_condition', models.CharField(choices=[('contado', 'Contado'), ('credito', 'Credito')], default='credito', max_length=50)),
                ('end_credit', models.DateField(default=datetime.datetime.now)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total_dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total_iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('subtotaldos', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
            options={
                'verbose_name': 'Solicitud de Transferencia',
                'verbose_name_plural': 'Solicitudes de Transferencia',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('location', models.CharField(blank=True, max_length=500, null=True, verbose_name='Ubicación')),
                ('serie', models.CharField(blank=True, max_length=30, null=True, verbose_name='Serie')),
            ],
            options={
                'verbose_name': 'Sucursal',
                'verbose_name_plural': 'Sucursal',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TypeExpense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Tipo de Gasto',
                'verbose_name_plural': 'Tipos de Gastos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='StockMovementDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.product')),
                ('stockmovement', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.stockmovement')),
            ],
            options={
                'verbose_name': 'Detall de Solicitud de Transferencia',
                'verbose_name_plural': 'Detalle de Solicitud de Transferencia',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='bodestino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bodestino_fixturetables', to='pos.sucursal', verbose_name='Bodega Destino'),
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='borigen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='borigen_fixturetables', to='pos.sucursal', verbose_name='Bodega Origen'),
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='plazo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pos.payment'),
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pos.provider'),
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total_dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.sale')),
            ],
            options={
                'verbose_name': 'Detalle de Venta',
                'verbose_name_plural': 'Detalle de Ventas',
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PurchaseRequestDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.product')),
                ('purchaserequest', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.purchaserequest')),
            ],
            options={
                'verbose_name': 'Detalle de solicitud de Compra',
                'verbose_name_plural': 'Detalle de solicitud de Compra',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='purchaserequest',
            name='sucursal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pos.sucursal'),
        ),
        migrations.CreateModel(
            name='PurchaseOrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.product')),
                ('purchaseorder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.purchaseorder')),
            ],
            options={
                'verbose_name': 'Detalle de Compra',
                'verbose_name_plural': 'Detalle de Compras',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.sucursal'),
        ),
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('cant', models.IntegerField(default=0)),
                ('serie', models.CharField(max_length=10, unique=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('state', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.purchase')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.sucursal')),
            ],
            options={
                'verbose_name': 'Detalle de Compra',
                'verbose_name_plural': 'Detalle de Compras',
                'ordering': ['-id'],
                'permissions': (),
            },
        ),
        migrations.AddField(
            model_name='purchase',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.sucursal'),
        ),
        migrations.CreateModel(
            name='PromotionsDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_current', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total_dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('price_final', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.product')),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.promotions')),
            ],
            options={
                'verbose_name': 'Detalle Promoción',
                'verbose_name_plural': 'Detalle de Promociones',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PaymentsDebtsPay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de registro')),
                ('desc', models.CharField(blank=True, max_length=500, null=True, verbose_name='Detalles')),
                ('valor', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Valor')),
                ('debtspay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.debtspay')),
            ],
            options={
                'verbose_name': 'Det. Cuenta por pagar',
                'verbose_name_plural': 'Det. Cuentas por pagar',
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PaymentsCtaCollect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de registro')),
                ('desc', models.CharField(blank=True, max_length=500, null=True, verbose_name='Detalles')),
                ('valor', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Valor')),
                ('ctascollect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.ctascollect')),
            ],
            options={
                'verbose_name': 'Pago Cuenta por cobrar',
                'verbose_name_plural': 'Pagos Cuentas por cobrar',
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de Registro')),
                ('valor', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Valor')),
                ('typeexpense', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.typeexpense', verbose_name='Tipo de Gasto')),
            ],
            options={
                'verbose_name': 'Gasto',
                'verbose_name_plural': 'Gastos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Devolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('cant', models.IntegerField(default=0)),
                ('motive', models.CharField(blank=True, max_length=500, null=True)),
                ('saledetail', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.saledetail')),
            ],
            options={
                'verbose_name': 'Devolución',
                'verbose_name_plural': 'Devoluciones',
                'ordering': ['-id'],
                'permissions': (('view_devolution', 'Can view Devoluciones'), ('add_devolution', 'Can add Devoluciones'), ('delete_devolution', 'Can delete Devoluciones')),
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='debtspay',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.purchase'),
        ),
        migrations.AddField(
            model_name='ctascollect',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.sale'),
        ),
    ]