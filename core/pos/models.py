import math
import os
import re
from datetime import datetime

from django.db import models
from django.db.models import FloatField
from django.db.models import Sum
from django.db.models.fields import CharField, DecimalField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config import settings
from core.pos.choices import payment_condition, payment_method, voucher,state_request,state_transfer
from core.user.models import User


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, verbose_name='Ruc')
    address = models.CharField(max_length=200, verbose_name='Dirección')
    mobile = models.CharField(max_length=10, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=9, verbose_name='Teléfono convencional')
    email = models.CharField(max_length=50, verbose_name='Email')
    website = models.CharField(max_length=250, verbose_name='Página web')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(null=True, blank=True, upload_to='company/%Y/%m/%d', verbose_name='Logo')
    iva = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Iva')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def get_iva(self):
        return format(self.iva, '.2f')

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        default_permissions = ()
        permissions = (
            ('view_company', 'Can view Company'),
        )
        ordering = ['-id']


class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, unique=True, verbose_name='Ruc')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    email = models.CharField(max_length=50, unique=True, verbose_name='Email')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-id']

class Payment(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=150,null=True, blank=True, verbose_name='Descripcion ')

    def __str__(self):
        return self.name
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        verbose_name = 'Plazo de Pago'
        verbose_name_plural = 'Plazo de Pago'
        ordering = ['-id']       

class Sucursal(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    location = models.CharField(max_length=500, null=True, blank=True, verbose_name='Ubicación')
    serie = models.CharField(max_length=30, null=True, blank=True, verbose_name='Serie')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursal'
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    inventoried = models.BooleanField(default=True, verbose_name='¿Es inventariado?')

    def __str__(self):
        return '{} / {}'.format(self.name, self.get_inventoried())

    def get_inventoried(self):
        if self.inventoried:
            return 'Inventariado'
        return 'No inventariado'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-id']


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marca'
        ordering = ['id']


class Exemplar(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Marca')
    name = models.CharField(max_length=100, verbose_name='Nombre')

    def __str__(self):
        return 'Modelo: {} / Marca: {}'.format(self.name, self.brand.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['brand'] = self.brand.toJSON()
        return item

    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    code = models.CharField(max_length=10, unique=True, verbose_name='Código')
    reference = models.CharField(max_length=150, null=True, blank=True, verbose_name='Referencia')
    detail = models.CharField(null=True, blank=True, max_length=250, verbose_name='Detalle')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoría')
    exemplar = models.ForeignKey(Exemplar, on_delete=models.PROTECT, verbose_name='Marca/Modelo')
    stock_maximum = models.IntegerField(default=0, verbose_name='Stock Máximo')
    stock_minimum = models.IntegerField(default=0, verbose_name='Stock Mínimo')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio de Compra')
    pvp = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Precio de Venta')
    image = models.ImageField(upload_to='product/%Y/%m/%d', verbose_name='Imagen', null=True, blank=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_stock(self):
        return self.purchasedetail_set.filter(state=True).count()

    def remove_image(self):
        try:
            if self.image:
                os.remove(self.image.path)
        except:
            pass
        finally:
            self.image = None

    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        item['exemplar'] = self.exemplar.toJSON()
        item['price'] = format(self.price, '.2f')
        item['price_promotion'] = format(self.get_price_promotion(), '.2f')
        item['price_current'] = format(self.get_price_current(), '.2f')
        item['pvp'] = format(self.pvp, '.2f')
        item['image'] = self.get_image()
        item['stock'] = self.get_stock()

        
        return item

    def get_price_promotion(self):
        promotions = self.promotionsdetail_set.filter(promotion__state=True)
        if promotions.exists():
            return promotions[0].price_final
        return 0.00

    def get_price_current(self):
        price_promotion = self.get_price_promotion()
        if price_promotion > 0:
            return price_promotion
        return self.pvp

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/default/empty.png')

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Product, self).delete()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-name']


class Purchase(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    payment_condition = models.CharField(choices=payment_condition, max_length=50, default='contado')
    date_joined = models.DateField(default=datetime.now)
    end_credit = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.provider.name

    def calculate_invoice(self):
        subtotal = 0.00
        for d in self.purchasedetail_set.all():
            subtotal += float(d.price) * int(d.cant)
        self.subtotal = subtotal
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.purchasedetail_set.all():
                i.product.stock -= i.cant
                i.product.save()
                i.delete()
        except:
            pass
        super(Purchase, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['nro'] = format(self.id, '06d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['end_credit'] = self.end_credit.strftime('%Y-%m-%d')
        item['provider'] = self.provider.toJSON()
        item['sucursal'] = self.sucursal.toJSON()
        item['payment_condition'] = {'id': self.payment_condition, 'name': self.get_payment_condition_display()}
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        default_permissions = ()
        permissions = (
            ('view_purchase', 'Can view Compras'),
            ('add_purchase', 'Can add Compras'),
            ('delete_purchase', 'Can delete Compras'),
        )
        ordering = ['-id']


class PurchaseDetail(models.Model):
    date_joined = models.DateField(default=datetime.now)
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    serie = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['purchase'])
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['product'] = self.product.toJSON()
        item['sucursal'] = self.sucursal.toJSON()
        item['price'] = format(self.price, '.2f')
        item['dscto'] = format(self.dscto, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'
        permissions = ()
        ordering = ['-id']


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')

    def __str__(self):
        return '{} / {}'.format(self.user.get_full_name(), self.user.dni)

    def birthdate_format(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']


class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    payment_condition = models.CharField(choices=payment_condition, max_length=50, default='contado')
    payment_method = models.CharField(choices=payment_method, max_length=50, default='efectivo')
    type_voucher = models.CharField(choices=voucher, max_length=50, default='ticket')
    date_joined = models.DateField(default=datetime.now)
    end_credit = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    cash = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    change = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    card_number = models.CharField(max_length=30, null=True, blank=True)
    titular = models.CharField(max_length=30, null=True, blank=True)
    amount_debited = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.client.user.get_full_name()} / {self.nro()}'

    def nro(self):
        return format(self.id, '06d')

    def get_client(self):
        if self.client:
            return self.client.toJSON()
        return {}

    def card_number_format(self):
        if self.card_number:
            cardnumber = self.card_number.split(' ')
            convert = re.sub('[0-9]', 'X', ' '.join(cardnumber[1:]))
            return '{} {}'.format(cardnumber[0], convert)
        return self.card_number

    def toJSON(self):
        item = model_to_dict(self, exclude=[''])
        item['nro'] = format(self.id, '06d')
        item['card_number'] = self.card_number_format()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['end_credit'] = self.end_credit.strftime('%Y-%m-%d')
        item['employee'] = {} if self.employee is None else self.employee.toJSON()
        item['client'] = {} if self.client is None else self.client.toJSON()
        item['payment_condition'] = {'id': self.payment_condition, 'name': self.get_payment_condition_display()}
        item['payment_method'] = {'id': self.payment_method, 'name': self.get_payment_method_display()}
        item['type_voucher'] = {'id': self.type_voucher, 'name': self.get_type_voucher_display()}
        item['subtotal'] = format(self.subtotal, '.2f')
        item['dscto'] = format(self.dscto, '.2f')
        item['total_dscto'] = format(self.total_dscto, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total_iva'] = format(self.total_iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['cash'] = format(self.cash, '.2f')
        item['change'] = format(self.change, '.2f')
        item['amount_debited'] = format(self.amount_debited, '.2f')
        return item

    def calculate_invoice(self):
        subtotal = 0.00
        for d in self.saledetail_set.filter():
            d.subtotal = float(d.price) * int(d.cant)
            d.total_dscto = float(d.dscto) * float(d.subtotal)
            d.total = d.subtotal - d.total_dscto
            d.save()
            subtotal += d.total
        self.subtotal = subtotal
        self.total_iva = self.subtotal * float(self.iva)
        self.total_dscto = self.subtotal * float(self.dscto)
        self.total = float(self.subtotal) - float(self.total_dscto) + float(self.total_iva)
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.saledetail_set.filter(product__category__inventoried=True):
                i.product.stock += i.cant
                i.product.save()
                i.delete()
        except:
            pass
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        default_permissions = ()
        permissions = (
            ('view_sale', 'Can view Ventas'),
            ('add_sale', 'Can add Ventas'),
            ('delete_sale', 'Can delete Ventas'),
        )
        ordering = ['-id']


class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = format(self.price, '.2f')
        item['dscto'] = format(self.dscto, '.2f')
        item['total_dscto'] = format(self.total_dscto, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
        ordering = ['-id']


class CtasCollect(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    debt = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    saldo = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    state = models.BooleanField(default=True)

    def __str__(self):
        return '{} / {} / ${}'.format(self.sale.client.user.get_full_name(), self.date_joined.strftime('%Y-%m-%d'),
                                      format(self.debt, '.2f'))

    def validate_debt(self):
        try:
            saldo = self.paymentsctacollect_set.aggregate(resp=Coalesce(Sum('valor'), 0.00, output_field=FloatField())).get('resp')
            self.saldo = float(self.debt) - float(saldo)
            self.state = self.saldo > 0.00
            self.save()
        except:
            pass

    def toJSON(self):
        item = model_to_dict(self)
        item['sale'] = self.sale.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        item['debt'] = format(self.debt, '.2f')
        item['saldo'] = format(self.saldo, '.2f')
        return item

    class Meta:
        verbose_name = 'Cuenta por cobrar'
        verbose_name_plural = 'Cuentas por cobrar'
        default_permissions = ()
        permissions = (
            ('view_ctascollect', 'Can view Cuentas por cobrar'),
            ('add_ctascollect', 'Can add Cuentas por cobrar'),
            ('delete_ctascollect', 'Can delete Cuentas por cobrar'),
        )
        ordering = ['-id']


class PaymentsCtaCollect(models.Model):
    ctascollect = models.ForeignKey(CtasCollect, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Detalles')
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor')

    def __str__(self):
        return self.ctascollect.id

    def toJSON(self):
        item = model_to_dict(self, exclude=['ctascollect'])
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['valor'] = format(self.valor, '.2f')
        return item

    class Meta:
        verbose_name = 'Pago Cuenta por cobrar'
        verbose_name_plural = 'Pagos Cuentas por cobrar'
        default_permissions = ()
        ordering = ['-id']


class DebtsPay(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    debt = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    saldo = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    state = models.BooleanField(default=True)

    def __str__(self):
        return '{} / {} / ${}'.format(self.purchase.provider.name, self.date_joined.strftime('%Y-%m-%d'),
                                      format(self.debt, '.2f'))

    def validate_debt(self):
        try:
            saldo = self.paymentsdebtspay_set.aggregate(resp=Coalesce(Sum('valor'), 0.00, output_field=FloatField())).get('resp')
            self.saldo = float(self.debt) - float(saldo)
            self.state = self.saldo > 0.00
            self.save()
        except:
            pass

    def toJSON(self):
        item = model_to_dict(self)
        item['purchase'] = self.purchase.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        item['debt'] = format(self.debt, '.2f')
        item['saldo'] = format(self.saldo, '.2f')
        return item

    class Meta:
        verbose_name = 'Cuenta por pagar'
        verbose_name_plural = 'Cuentas por pagar'
        default_permissions = ()
        permissions = (
            ('view_debtspay', 'Can view Cuentas por pagar'),
            ('add_debtspay', 'Can add Cuentas por pagar'),
            ('delete_debtspay', 'Can delete Cuentas por pagar'),
        )
        ordering = ['-id']


class PaymentsDebtsPay(models.Model):
    debtspay = models.ForeignKey(DebtsPay, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Detalles')
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor')

    def __str__(self):
        return self.debtspay.id

    def toJSON(self):
        item = model_to_dict(self, exclude=['debtspay'])
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['valor'] = format(self.valor, '.2f')
        return item

    class Meta:
        verbose_name = 'Det. Cuenta por pagar'
        verbose_name_plural = 'Det. Cuentas por pagar'
        default_permissions = ()
        ordering = ['-id']


class TypeExpense(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Gasto'
        verbose_name_plural = 'Tipos de Gastos'
        ordering = ['id']


class Expenses(models.Model):
    typeexpense = models.ForeignKey(TypeExpense, verbose_name='Tipo de Gasto', on_delete=models.PROTECT)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Valor')

    def __str__(self):
        return self.desc

    def get_desc(self):
        if self.desc:
            return self.desc
        return 'Sin detalles'

    def toJSON(self):
        item = model_to_dict(self)
        item['typeexpense'] = self.typeexpense.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['valor'] = format(self.valor, '.2f')
        item['desc'] = self.get_desc()
        return item

    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ['id']


class Promotions(models.Model):
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    state = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Promoción'
        verbose_name_plural = 'Promociones'
        ordering = ['-id']


class PromotionsDetail(models.Model):
    promotion = models.ForeignKey(Promotions, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price_current = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    price_final = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def get_dscto_real(self):
        total_dscto = float(self.price_current) * float(self.dscto)
        n = 2
        return math.floor(total_dscto * 10 ** n) / 10 ** n

    def toJSON(self):
        item = model_to_dict(self, exclude=['promotion'])
        item['product'] = self.product.toJSON()
        item['price_current'] = format(self.price_current, '.2f')
        item['dscto'] = format(self.dscto, '.2f')
        item['total_dscto'] = format(self.total_dscto, '.2f')
        item['price_final'] = format(self.price_final, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle Promoción'
        verbose_name_plural = 'Detalle de Promociones'
        ordering = ['-id']


class Devolution(models.Model):
    saledetail = models.ForeignKey(SaleDetail, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    cant = models.IntegerField(default=0)
    motive = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.motive

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['saledetail'] = self.saledetail.toJSON()
        item['motive'] = 'Sin detalles' if len(self.motive) == 0 else self.motive
        return item

    class Meta:
        verbose_name = 'Devolución'
        verbose_name_plural = 'Devoluciones'
        default_permissions = ()
        permissions = (
            ('view_devolution', 'Can view Devoluciones'),
            ('add_devolution', 'Can add Devoluciones'),
            ('delete_devolution', 'Can delete Devoluciones'),
        )
        ordering = ['-id']

class PurchaseRequest(models.Model):
    date_joined = models.DateField(default=datetime.now)
    state = models.CharField(choices=state_request, max_length=50, default='Enviado')
    sucursal=models.ForeignKey(Sucursal, on_delete=models.PROTECT, null=True, blank=True)
    concepto = models.CharField(max_length=150, verbose_name='Concepto', null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT,null=True, blank=True )
    payment_condition = models.CharField(choices=payment_condition, max_length=150, default='Credito')
    end_credit = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    plazo = models.ForeignKey(Payment, on_delete=models.PROTECT, null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotaldos = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.provider.name
    

    def __str__(self):
        return self.concepto

    def nro(self):
        return format(self.id, '06d')
    
    def calculate_invoice_(self):
        subtotal = 0.00
        for d in self.purchaserequestdetail_set.all():
            subtotal += float(d.price)*int(d.cant)
        self.subtotal = subtotal
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.purchaserequestdetail_set.all():
                i.product.stock -= i.cant
                i.product.save()
                i.delete()
        except:
            pass
        super(PurchaseRequest, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['nro']=format(self.id, '06d')
        item['date_joined']=self.date_joined.strftime('%Y-%m-%d')
        item['sucursal']=self.sucursal.toJSON()
        item['end_credit'] = self.end_credit.strftime('%Y-%m-%d')
        item['provider'] = {} if self.provider is None else self.provider.toJSON()
        item['payment_condition'] = {'id': self.payment_condition, 'name': self.get_payment_condition_display()}
        item['subtotal'] = format(self.subtotal, '.2f')
        item['dscto'] = format(self.dscto, '.2f')
        item['total_dscto'] = format(self.total_dscto, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total_iva'] = format(self.total_iva, '.2f')
        item['subtotaldos'] = format(self.subtotaldos, '.2f')
        item['total'] = format(self.total, '.2f')
        item['plazo'] = {} if self.plazo is None else self.plazo.toJSON()

        return item





    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.purchaserequestdetail_set.filter(product_category_inventoried=True):
                i.product.stock += i.cant
                i.product.save()
                i.delete()
        except:
            pass
        super(PurchaseRequest, self).delete()    

    class Meta:
        verbose_name = 'Solicitud de Compra'
        verbose_name_plural = 'Solicitudes de Compra'    

        ordering = ['-id']

class PurchaseRequestDetail(models.Model):
    purchaserequest = models.ForeignKey(PurchaseRequest, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0) 
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['purchaserequest'])
        item['product']=self.product.toJSON()
        item['price']=format(self.price, '2f')
        item['subtotal']=format(self.subtotal, '.2f')
        return item 
    
    class Meta:
        verbose_name = 'Detalle de solicitud de Compra'
        verbose_name_plural = 'Detalle de solicitud de Compra'
        ordering = ['-id']

#------------------------------------------------------------------------------------------------

class PurchaseOrder(models.Model):
    reference=models.IntegerField(default=0)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    concepto = models.CharField(max_length=150,verbose_name='Concepto')
    payment_condition = models.CharField(choices=payment_condition, max_length=50, default='contado')
    data_joined=models.DateField(default=datetime.now)
    end_credit= models.DateField(default=datetime.now)
    state = models.CharField(choices=state_request, max_length=50, default='Enviado')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.provider.name
    
    def calculate_invoice(self):
        subtotal = 0.00
        for d in self.purchaseorderdetail_set.all():
            subtotal += float(d.price) * int(d.cant)
        self.subtotal = subtotal
        self.save()
    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.purchaserequestdetail_set.all():
                i.product.stock -= i.cant
        except:
            pass
        super(PurchaseOrder, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['nro']=format(self.id, '06d')
        item['date_joined']=self.date_joined.strftime('%Y-%m-%d')
        item['reference']=self.reference.toJSON()
        item['concepto']=self.concepto.toJSON()
        item['sucursal'] = self.sucursal.toJSON()
        item['state'] = self.state.toJSON()
        item['provider'] = self.provider.toJSON()
        item['payment_condition'] = {'id': self.payment_condition, 'name': self.get_payment_condition_display()}
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Ordenes de Compra'
        ordering = ['-id']

class PurchaseOrderDetail(models.Model):
    purchaseorder = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
       return self.product.name
    
    def toJSON(self):
        item= model_to_dict(self,)

        item['product']=self.product.toJSON()
        item['price']=format(self.price, '.2f')
        item['dscto']=format(self.dscto, '.2f')
        item['subtotal']=format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'
        ordering = ['-id']
    
class StockMovement(models.Model):
    date_joined = models.DateField(default=datetime.now)
    state = models.CharField(choices=state_transfer, max_length=100, default='Realizada')
    borigen =models.ForeignKey(Sucursal,on_delete=models.PROTECT, related_name="borigen_fixturetables", verbose_name="Bodega Origen")
    bodestino=models.ForeignKey(Sucursal,on_delete=models.PROTECT, related_name="bodestino_fixturetables", verbose_name="Bodega Destino")
    provider=models.ForeignKey(Provider, on_delete=models.PROTECT, null=True, blank=True)
    concepto = models.CharField(max_length=150, verbose_name='Concepto', null=True, blank=True)
    payment_condition = models.CharField(choices=payment_condition, max_length=50, default='credito')
    end_credit = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    plazo = models.ForeignKey(Payment, on_delete=models.PROTECT, null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_dscto = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total_iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotaldos = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.provider.name

    def nro(self):
        return format(self.id,'06d')

    def calculate_invoice(self):
        subtotal = 0.00
        for d in self.stockmovementdetail_set.all():
            subtotal += float(d.price)*int(d.cant)
        self.subtotal=subtotal
        self.save()
    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.stockmovement_set.all():
                i.product.stock -= i.cant
                i.product.save()
                i.delete()
        except:
            pass
        super(StockMovement, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['nro']=format(self.id, '06d')
        item['date_joined']=self.date_joined.strftime('%Y-%m-%d')
        item['borigen']=self.borigen.toJSON()
        item['bodestino']=self.bodestino.toJSON()
        item['end_credit'] = self.end_credit.strftime('%Y-%m-%d')
        item['provider'] = {} if self.provider is None else self.provider.toJSON()
        item['payment_condition'] = {'id': self.payment_condition, 'name': self.get_payment_condition_display()}
        item['subtotal'] = format(self.subtotal, '.2f')
        item['dscto'] = format(self.dscto, '.2f')
        item['total_dscto'] = format(self.total_dscto, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total_iva'] = format(self.total_iva, '.2f')
        item['subtotaldos'] = format(self.subtotaldos, '.2f')
        item['total'] = format(self.total, '.2f')
        item['plazo'] = {} if self.plazo is None else self.plazo.toJSON()

        return item

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.stockmovement_set.filter(product__category__inventoried=True):
                i.product.stock += i.cant
                i.product.save()
                i.delete()
        except:
            pass
        super(PurchaseRequest, self).delete()
       
    class Meta:
        verbose_name = 'Solicitud de Transferencia'
        verbose_name_plural = 'Solicitudes de Transferencia'
  
        ordering = ['-id'] 

class StockMovementDetail(models.Model):
    stockmovement = models.ForeignKey(StockMovement, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self,exclude=['stockmovement'])
        item['product']=self.product.toJSON()
        item['price']=format(self.price, '.2f')
        item['subtotal']=format(self.subtotal, '.2F')
        return item 
    
    class Meta:
        verbose_name = 'Detall de Solicitud de Transferencia'
        verbose_name_plural = 'Detalle de Solicitud de Transferencia'
        ordering = ['-id']


class Pricelist(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Titulo')
    dia = models.IntegerField(null=True, blank=True, verbose_name='Plazo de Pago')
    tiemp = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tiempo Diferido')
    desc = models.DecimalField(blank=True, default=0.00, max_digits=9, decimal_places=2, verbose_name='Descuento %' )
    tipo = models.CharField(max_length=100, choices=payment_condition, verbose_name='Tipo de Pago', blank=False, null=False)        

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['desc']=format(self.desc, '.2f')

        return item

    class Meta:
        verbose_name = 'Pricelist'
        verbose_name_plural = 'PriceList'
        ordering = ['-id']

class ProductBySucursal(models.Model):
    sucursal=models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.sucursal.name
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nro']=format(self.id, '06d')
        item['sucursal']={'id':self.sucursal, 'name':self.get_sucursal_display()}
        return item      

class ProductBySucursalDetail(models.Model):
    productbysucursal = models.ForeignKey(ProductBySucursal, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['productbysucursal'])
        item['product']=self.product.toJSON()
        item['price']=format(self.price, '.2f')
        item['pvp']=format(self.pvp, '.2f')
     
        return item
    
    class Meta:
        verbose_name = 'Lista de productos Stock'
        verbose_name_plural='Lista de Productos Stock'
        default_permissions=()
        ordering = ['-id']
