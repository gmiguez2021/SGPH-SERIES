import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView

from core.pos.forms import PurchaseForm, Purchase, PurchaseDetail,PurchaseRequestDetail, PurchaseRequest, Product, Provider, DebtsPay, ProviderForm, PurchaseRequestForm, StockMovement, StockMovementForm
from core.pos.models import StockMovementDetail
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin

from django.db.models import Q




class StockMovementListView(PermissionMixin, FormView):
    model = StockMovement
    template_name = 'scm/stockmovement/list.html'
    permission_required = 'view_stockmovement'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
            data = {}
            action = request.POST['action']
            try:
                if action == 'search':
                    data = []
                    start_date = request.POST['start_date']
                    end_date = request.POST['end_date']
                    search = StockMovement.objects.filter(Q(state='Realizada'))
                    if len(start_date) and len(end_date):
                        search = search.filter(date_joined__range=[start_date, end_date])
                    for i in search:
                        data.append(i.toJSON())
                elif action == 'search_detproducts':
                    print('entrali')
                    data = []
                    for det in StockMovementDetail.objects.filter(stockmovement_id=request.POST['id']):
                        data.append(det.toJSON())
                else:
                    data['error'] = 'No ha ingresado una opción'
            except Exception as e:
                data['error'] = str(e)
            return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('stockmovement_create')
        context['title'] = 'Solicitudes de Transferencia'
        return context
#--------------------------------------------------------------------------------------------------------------------------------------------------------------


class StockMovementCreateView(PermissionMixin, CreateView):
    model = StockMovement
    template_name = 'scm/stockmovement/create.html'
    form_class = StockMovementForm
    success_url = reverse_lazy('stockmovement_list')
    permission_required = 'add_stockmovement'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    print('entra compra')
                    stockmovement = StockMovement()
                    stockmovement.date_joined = request.POST['date_joined']
                    stockmovement.employee_id = request.user.id

                    print('d',stockmovement.date_joined)
                    #purchaserequest.reference = request.POST['reference']
                    stockmovement.state = "Realizada"
                    stockmovement.concepto = request.POST['concepto'] 
                    stockmovement.borigen_id = request.POST['borigen']
                    stockmovement.bodestino_id = request.POST['bodestino']
                    print('cv',stockmovement.borigen_id)
                    #purchaserequest.reference = request.POST['id']
                    #print('cvv',purchaserequest.reference)

                    stockmovement.save()
                    print('guarda solicitud')

                    for p in json.loads(request.POST['products']):
                        print('entra recorre solicitud')
                        print(json.loads(request.POST['products']))
                        prod = Product.objects.get(pk=p['id'])
                        det = StockMovementDetail()
                        #print('iiiid',purchaserequest.id)
                        det.stockmovement_id = stockmovement.id
                        print('ddc',det.stockmovement_id)
                        det.product_id = prod.id
                        det.cant = int(p['cant'])
                        print('ddcc',det.cant)
                        det.price = float(p['price'])

                        #det.price = float(p['price'])
                        #det.subtotal = det.cant * float(det.price)
                        det.save()

                        #det.product.stock += det.cant
                        det.product.save()

                    #purchaserequest.calculate_invoice()

            elif action == 'search_products':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                print('entra a buscar',term)
                search = Product.objects.filter(category__inventoried=True).exclude(id__in=ids).order_by('name')
                if len(term):
                    search = search.filter(name__icontains=term)
                    search = search[0:10]
                for p in search:
                    item = p.toJSON()
                    item['value'] = '{} / {}'.format(p.name, p.category.name)
                    data.append(item)
            
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Transferencia'
        context['action'] = 'add'
        return context

#--------------------------------------------------------------------------------------------------------------------------------------------------
class StockMovementDeleteView(PermissionMixin, DeleteView):
    model = StockMovement
    template_name = 'scm/stockmovement/delete.html'
    success_url = reverse_lazy('stockmovement_list')
    permission_required = 'delete_stockmovement'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context

        

          
      		       
            
                    
                    
     	       
     	          
     	               
     	          
     	          

	     	     
     	     
