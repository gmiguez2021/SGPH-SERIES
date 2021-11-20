from django.urls import path

from core.pos.views.crm.company.views import CompanyUpdateView
from core.pos.views.crm.promotions.views import *
from core.pos.views.crm.sale.admin.views import *
from core.pos.views.crm.sale.client.views import SaleClientListView
from core.pos.views.frm.ctascollect.views import *
from core.pos.views.frm.debtspay.views import *
from core.pos.views.scm.product.views import *
from core.pos.views.scm.provider.views import *
from core.pos.views.scm.category.views import *
from core.pos.views.scm.purchase.views import *
from core.pos.views.frm.typeexpense.views import *
from core.pos.views.frm.expenses.views import *
from core.pos.views.crm.client.views import *
from core.pos.views.crm.sale.print.views import *
from core.pos.views.crm.devolution.views import *
from core.pos.views.scm.stockmovement.print.views import StockPrintMovementView
from core.pos.views.scm.stockmovement.view import StockMovementCreateView, StockMovementDeleteView, StockMovementListView
from core.pos.views.scm.sucursal.views import *
from core.pos.views.scm.brand.views import *
from core.pos.views.scm.exemplar.views import *
from core.pos.views.scm.payment.views import *
from core.pos.views.scm.purchaserequest.view import *
from core.pos.views.scm.purchaserequest.print.views import* 
from core.pos.views.scm.purchaseorder.print.views import *
from core.pos.views.scm.purchaseorder.views import *
from core.pos.views.scm.stockmovement.print.views import *
from core.pos.views.scm.stockmovement.view import *
from core.pos.views.scm.authorizepurchase.views import *
from core.pos.views.scm.authorizepurchase.print.views import *

urlpatterns = [
    # SCM
    # brand
    path('scm/brand/', BrandListView.as_view(), name='brand_list'),
    path('scm/brand/add/', BrandCreateView.as_view(), name='brand_create'),
    path('scm/brand/update/<int:pk>/', BrandUpdateView.as_view(), name='brand_update'),
    path('scm/brand/delete/<int:pk>/', BrandDeleteView.as_view(), name='brand_delete'),
    # exemplar
    path('scm/exemplar/', ExemplarListView.as_view(), name='exemplar_list'),
    path('scm/exemplar/add/', ExemplarCreateView.as_view(), name='exemplar_create'),
    path('scm/exemplar/update/<int:pk>/', ExemplarUpdateView.as_view(), name='exemplar_update'),
    path('scm/exemplar/delete/<int:pk>/', ExemplarDeleteView.as_view(), name='exemplar_delete'),
    # provider
    path('scm/provider/', ProviderListView.as_view(), name='provider_list'),
    path('scm/provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('scm/provider/update/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('scm/provider/delete/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
    #payment
    path('scm/payment/', PaymentListView.as_view(), name='payment_list'),
    path('scm/payment/add/', PaymentCreateView.as_view(), name='payment_create'),
    path('scm/payment/update/<int:pk>/', PaymentUpdateView.as_view(), name='payment_update'),
    path('scm/payment/delete/<int:pk>/', PaymentDeleteView.as_view(), name='payment_delete'),


    # sucursal
    path('scm/sucursal/', SucursalListView.as_view(), name='sucursal_list'),
    path('scm/sucursal/add/', SucursalCreateView.as_view(), name='sucursal_create'),
    path('scm/sucursal/update/<int:pk>/', SucursalUpdateView.as_view(), name='sucursal_update'),
    path('scm/sucursal/delete/<int:pk>/', SucursalDeleteView.as_view(), name='sucursal_delete'),
    # category
    path('scm/category/', CategoryListView.as_view(), name='category_list'),
    path('scm/category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('scm/category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('scm/category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # product
    path('scm/product/', ProductListView.as_view(), name='product_list'),
    path('scm/product/add/', ProductCreateView.as_view(), name='product_create'),
    path('scm/product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('scm/product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('scm/product/stock/adjustment/', ProductStockAdjustmentView.as_view(), name='product_stock_adjustment'),
    path('scm/product/export/excel/', ProductExportExcelView.as_view(), name='product_export_excel'),
    # purchase
    path('scm/purchase/', PurchaseListView.as_view(), name='purchase_list'),
    path('scm/purchase/add/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('scm/purchase/delete/<int:pk>/', PurchaseDeleteView.as_view(), name='purchase_delete'),

    #purchaserequest

    path('scm/purchaserequest/', PurchaseRequestListView.as_view(), name='purchase_list'),
    path('scm/purchaserequest/add/', PurchaseRequestCreateView.as_view(), name='purchaserequest_create'),
    path('scm/purchaserequest/delete/<int:pk>/', PurchaseRequestDeleteView.as_view(), name='purchaserequest_delete'),
    path('scm/purchaserequest/print/request/<int:pk>/', PurchasePrintRequestView.as_view(), name='purchase_print_purchase'),

    #purchaseorder
    path('scm/purchaseorder/', PurchaseOrderListView.as_view(), name='purchaseorder_list'),
    path('scm/purchaseorder/add/', PurchaseOrderCreateView.as_view(), name='purchaseorder_create'),
    path('scm/purchaseorder/delete/<int:pk>/', PurchaseOrderDeleteView.as_view(), name='purchaseorder_delete'),
    path('scm/purchaseorder/update/<int:pk>/', PurchaseAdminUpdateView.as_view(), name='purchaseorder_update'),
    path('scm/purchaseorder/print/request/<int:pk>/', PurchaseOrderPrintRequestView.as_view(), name='purchaseorder_print_purchase'),

    #stockmovement
    path('scm/stockmovement/', StockMovementListView.as_view(), name='stockmovement_list'),
    path('scm/stockmovement/add/', StockMovementCreateView.as_view(), name='stockmovement_create'),
    path('scm/stockmovement/delete/<int:pk>/', StockMovementDeleteView.as_view(), name='stockmovement_delete'),
    path('scm/stockmovement/print/request/<int:pk>/', StockPrintMovementView.as_view(), name='stockmovement_print_stockmovement'),



    #authorizepurchase
    path('scm/authorizepurchase/', AuthorizePurchaseListView.as_view(), name='authorizepurchase_list'),
    path('scm/authorizepurchase/add/', AuthorizePurchaseCreateView.as_view(), name='authorizepurchase_create'),
    path('scm/authorizepurchase/delete/<int:pk>/', AuthorizePurchaseDeleteView.as_view(), name='authorizepurchase_delete'),
    path('scm/authorizepurchase/update/<int:pk>/', AuthorizePurchaseUpdView.as_view(), name='authorizepurchase_update'),
    path('scm/authorizepurchase/print/request/<int:pk>/', AuthorizePurchasePrintRequestView.as_view(), name='authorizepurchase_print_purchase'),

    # FRM
    # type_expensexs
    path('frm/type/expense/', TypeExpenseListView.as_view(), name='typeexpense_list'),
    path('frm/type/expense/add/', TypeExpenseCreateView.as_view(), name='typeexpense_create'),
    path('frm/type/expense/update/<int:pk>/', TypeExpenseUpdateView.as_view(), name='typeexpense_update'),
    path('frm/type/expense/delete/<int:pk>/', TypeExpenseDeleteView.as_view(), name='typeexpense_delete'),
    # expenses
    path('frm/expenses/', ExpensesListView.as_view(), name='expenses_list'),
    path('frm/expenses/add/', ExpensesCreateView.as_view(), name='expenses_create'),
    path('frm/expenses/update/<int:pk>/', ExpensesUpdateView.as_view(), name='expenses_update'),
    path('frm/expenses/delete/<int:pk>/', ExpensesDeleteView.as_view(), name='expenses_delete'),
    # debtspay
    path('frm/debts/pay/', DebtsPayListView.as_view(), name='debtspay_list'),
    path('frm/debts/pay/add/', DebtsPayCreateView.as_view(), name='debtspay_create'),
    path('frm/debts/pay/delete/<int:pk>/', DebtsPayDeleteView.as_view(), name='debtspay_delete'),
    # ctascollect
    path('frm/ctas/collect/', CtasCollectListView.as_view(), name='ctascollect_list'),
    path('frm/ctas/collect/add/', CtasCollectCreateView.as_view(), name='ctascollect_create'),
    path('frm/ctas/collect/delete/<int:pk>/', CtasCollectDeleteView.as_view(), name='ctascollect_delete'),
    # CRM
    # company
    path('crm/company/update/', CompanyUpdateView.as_view(), name='company_update'),
    # promotions
    path('crm/promotions/', PromotionsListView.as_view(), name='promotions_list'),
    path('crm/promotions/add/', PromotionsCreateView.as_view(), name='promotions_create'),
    path('crm/promotions/update/<int:pk>/', PromotionsUpdateView.as_view(), name='promotions_update'),
    path('crm/promotions/delete/<int:pk>/', PromotionsDeleteView.as_view(), name='promotions_delete'),
    # client
    path('crm/client/', ClientListView.as_view(), name='client_list'),
    path('crm/client/add/', ClientCreateView.as_view(), name='client_create'),
    path('crm/client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('crm/client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('crm/client/update/profile/', ClientUpdateProfileView.as_view(), name='client_update_profile'),
    # sale/admin
    path('crm/sale/admin/', SaleAdminListView.as_view(), name='sale_admin_list'),
    path('crm/sale/admin/add/', SaleAdminCreateView.as_view(), name='sale_admin_create'),
    path('crm/sale/admin/delete/<int:pk>/', SaleAdminDeleteView.as_view(), name='sale_admin_delete'),
    path('crm/sale/print/voucher/<int:pk>/', SalePrintVoucherView.as_view(), name='sale_print_ticket'),
    path('crm/sale/client/', SaleClientListView.as_view(), name='sale_client_list'),
    # devolution
    path('crm/devolution/', DevolutionListView.as_view(), name='devolution_list'),
    path('crm/devolution/add/', DevolutionCreateView.as_view(), name='devolution_create'),
    path('crm/devolution/delete/<int:pk>/', DevolutionDeleteView.as_view(), name='devolution_delete'),
]
