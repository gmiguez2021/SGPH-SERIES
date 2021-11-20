import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import Sucursal, SucursalForm
from core.security.mixins import PermissionMixin


class SucursalListView(PermissionMixin, ListView):
    model = Sucursal
    template_name = 'scm/sucursal/list.html'
    permission_required = 'view_sucursal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('sucursal_create')
        context['title'] = 'Listado de Sucursales'
        return context


class SucursalCreateView(PermissionMixin, CreateView):
    model = Sucursal
    template_name = 'scm/sucursal/create.html'
    form_class = SucursalForm
    success_url = reverse_lazy('sucursal_list')
    permission_required = 'add_sucursal'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Sucursal.objects.filter(name__iexact=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Sucursal'
        context['action'] = 'add'
        return context


class SucursalUpdateView(PermissionMixin, UpdateView):
    model = Sucursal
    template_name = 'scm/sucursal/create.html'
    form_class = SucursalForm
    success_url = reverse_lazy('sucursal_list')
    permission_required = 'change_sucursal'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            id = self.get_object().id
            if type == 'name':
                if Sucursal.objects.filter(name__iexact=obj).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una Sucursal'
        context['action'] = 'edit'
        return context


class SucursalDeleteView(PermissionMixin, DeleteView):
    model = Sucursal
    template_name = 'scm/sucursal/delete.html'
    success_url = reverse_lazy('sucursal_list')
    permission_required = 'delete_sucursal'

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
