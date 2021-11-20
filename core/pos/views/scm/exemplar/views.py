import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import Exemplar, ExemplarForm
from core.security.mixins import PermissionMixin


class ExemplarListView(PermissionMixin, ListView):
    model = Exemplar
    template_name = 'scm/exemplar/list.html'
    permission_required = 'view_exemplar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('exemplar_create')
        context['title'] = 'Listado de Modelos'
        return context


class ExemplarCreateView(PermissionMixin, CreateView):
    model = Exemplar
    template_name = 'scm/exemplar/create.html'
    form_class = ExemplarForm
    success_url = reverse_lazy('exemplar_list')
    permission_required = 'add_exemplar'

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            name = self.request.POST['name'].strip()
            brand = self.request.POST['brand']
            if type == 'name' and len(brand):
                if Exemplar.objects.filter(name__iexact=name, brand_id=brand):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
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
        context['title'] = 'Nuevo registro de un Modelo'
        context['action'] = 'add'
        return context


class ExemplarUpdateView(PermissionMixin, UpdateView):
    model = Exemplar
    template_name = 'scm/exemplar/create.html'
    form_class = ExemplarForm
    success_url = reverse_lazy('exemplar_list')
    permission_required = 'change_exemplar'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            name = self.request.POST['name'].strip()
            brand = self.request.POST['brand']
            id = self.object.id
            if type == 'name' and len(brand):
                if Exemplar.objects.filter(name__iexact=name, brand_id=brand).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST.get('action', None)
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
        context['title'] = 'Edición de una Módelo'
        context['action'] = 'edit'
        return context


class ExemplarDeleteView(PermissionMixin, DeleteView):
    model = Exemplar
    template_name = 'scm/exemplar/delete.html'
    success_url = reverse_lazy('exemplar_list')
    permission_required = 'delete_exemplar'

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
