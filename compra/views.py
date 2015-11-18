from django.db.models import Sum
from django.db.models import Case, Value, When, F
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import routers, viewsets, filters, generics, renderers
import models
import serializers
import cStringIO as StringIO
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

"""
	@name: ProductoViewSet
	@author: Luis Miguel Morales Pajaro
	@buisiness: bitgray

"""
class ProductoViewSet(viewsets.ModelViewSet):
	allowed_methods = ('GET', 'DELETE', 'POST', 'PATCH')
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('id','producto', 'precio',)
	queryset = models.Producto.objects.all()
	serializer_class = serializers.ProductoSerializer

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(ProductoViewSet, self).dispatch(*args, **kwargs)
	#end def

	def delete(self, request):
		id_value = self.request.GET.getlist('id', None)
		if id_value:
			self.get_queryset().filter(id__in=id_value).delete()
		else:
			self.filter_queryset(self.get_queryset()).delete()
		#end if
		return self.get(request)
	#end def

	def patch(self, request):
		try:
			patch = request.data
			self.filter_queryset(self.queryset).update(**patch)
		except Exception as e:
			print e
		#end escept
		return self.get(request)
	#end def

#end class

"""
	@name: ClienteViewSet
	@author: Luis Miguel Morales Pajaro
	@buisiness: bitgray

"""
class ClienteViewSet(viewsets.ModelViewSet):
	allowed_methods = ('GET', 'DELETE', 'POST', 'PATCH')
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('id','documento', 'nombres',)
	queryset = models.Cliente.objects.all()
	serializer_class = serializers.ClienteSerializer

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(ClienteViewSet, self).dispatch(*args, **kwargs)
	#end def

	def delete(self, request):
		id_value = self.request.GET.getlist('id', None)
		if id_value:
			self.get_queryset().filter(id__in=id_value).delete()
		else:
			self.filter_queryset(self.get_queryset()).delete()
		#end if
		return self.get(request)
	#end def

	def patch(self, request):
		try:
			patch = request.data
			self.filter_queryset(self.queryset).update(**patch)
		except Exception as e:
			print e
		#end escept
		return self.get(request)
	#end def
#end class

"""
	@name: SedeViewSet
	@author: Luis Miguel Morales Pajaro
	@buisiness: bitgray

"""
class SedeViewSet(viewsets.ModelViewSet):
	allowed_methods = ('GET', 'DELETE', 'POST', 'PATCH')
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('id','sede', 'direccion',)
	queryset = models.Sede.objects.all()
	serializer_class = serializers.SedeSerializer

	def delete(self, request):
		id_value = self.request.GET.getlist('id', None)
		if id_value:
			self.get_queryset().filter(id__in=id_value).delete()
		else:
			self.filter_queryset(self.get_queryset()).delete()
		#end if
		return self.get(request)
	#end def

	def patch(self, request):
		try:
			patch = request.data
			self.filter_queryset(self.queryset).update(**patch)
		except Exception as e:
			print e
		#end escept
		return self.get(request)
	#end def
#end class


"""
	@name: CompraViewSet
	@author: Luis Miguel Morales Pajaro
	@buisiness: bitgray

"""
class CompraViewSet(viewsets.ModelViewSet):
	allowed_methods = ('GET', 'DELETE', 'POST', 'PATCH')
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = ('id','cliente', 'producto', 'sede', 'precio')
	queryset = models.Compra.objects.filter(producto__isnull=False)
	serializer_class = serializers.CompraSerializer

	def delete(self, request):
		id_value = self.request.GET.getlist('id', None)
		if id_value:
			self.get_queryset().filter(id__in=id_value).delete()
		else:
			self.filter_queryset(self.get_queryset()).delete()
		#end if
		return self.get(request)
	#end def

	def patch(self, request):
		try:
			patch = request.data
			self.filter_queryset(self.queryset).update(**patch)
		except Exception as e:
			print e
		#end escept
		return self.get(request)
	#end def
#end class


"""
	@name: LogViewSet
	@author: Luis Miguel Morales Pajaro
	@buisiness: bitgray

"""
class LogViewSet(viewsets.ModelViewSet):
	allowed_methods = ('GET', 'DELETE', 'POST', 'PATCH')
	filter_backends = (filters.DjangoFilterBackend,)
	queryset = models.Log.objects.all()
	serializer_class = serializers.LogSerializer

	def delete(self, request):
		id_value = self.request.GET.getlist('id', None)
		if id_value:
			self.get_queryset().filter(id__in=id_value).delete()
		else:
			self.filter_queryset(self.get_queryset()).delete()
		#end if
		return self.get(request)
	#end def

	def patch(self, request):
		try:
			patch = request.data
			self.filter_queryset(self.queryset).update(**patch)
		except Exception as e:
			print e
		#end escept
		return self.get(request)
	#end def
#end class

"""
	@name: FacturaViewSet
	@author: Luis Miguel Morales Pajaro
	@buisiness: bitgray

"""
class CustomJSONRenderer(renderers.JSONRenderer):
	def render(self, data, accepted_media_type=None, renderer_context=None):
		data_new = {}
		data_new['total_precio'] = renderer_context['total_precio']
		data_new['cliente'] = renderer_context['cliente']
		data_new['results'] = data
		return super(CustomJSONRenderer, self).render(data_new, accepted_media_type, renderer_context)
	#end def
#end class

class FacturaViewSet(viewsets.ModelViewSet):
	allowed_methods = ('GET',)
	filter_backends = (filters.DjangoFilterBackend,)
	queryset = models.Compra.objects.filter(producto__isnull=False)
	filter_fields = ('cliente__documento',)
	serializer_class = serializers.FacturaSerializer
	renderer_classes = (renderers.BrowsableAPIRenderer, CustomJSONRenderer)
	pagination_class = None

	def get_renderer_context(self):
		context = super(FacturaViewSet, self).get_serializer_context()
		filtered = self.filter_queryset(self.queryset)
		total_precio = filtered.aggregate(total_precio=Sum(
				Case(
					When(precio=None, then=F('producto__precio')),
					default=F('precio')
				)
			)
		).values()
		first = filtered.first()
		if first:
			context['cliente'] = first.cliente.nombres
		else:
			context['cliente'] = ''
		#end if
		if len(total_precio):
			context['total_precio'] = total_precio[0]
		else:
			context['total_precio'] = 0
		#end def
		return context
	#end def
#end class

def render_to_pdf(template_src, context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context)
	result = StringIO.StringIO()

	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
#end def

from django.shortcuts import get_object_or_404

def pdf(request, documento):
	facturas = models.Compra.objects.filter(cliente__documento=documento, producto__isnull=False)
	first = get_object_or_404(facturas.filter()[:1])
	total_precio = facturas.aggregate(total_precio=Sum(
			Case(
				When(precio=None, then=F('producto__precio')),
				default=F('precio')
			)
		)
	).values()

	facturas = facturas.annotate(
		calc_precio=Case(
			When(precio=None, then=F('producto__precio')),
			default=F('precio')
		),
		producto_producto=F('producto__producto'),
		sede_sede=F('sede__sede')
	).values()
	return render_to_pdf('compra/pdf.html',{
		'pagesize':'A4',
		'documento':documento,
		'facturas': facturas, 
		'total_precio': total_precio[0], 
		'cliente':first.cliente.nombres
	})
#end def

from django.db import connection

def reporte(request):
	cursor = connection.cursor()
	cursor.execute('select * from reporte')
	reporte = cursor.fetchall()
	cursor.execute('select * from prom')
	prom = cursor.fetchall()
	
	return render_to_pdf('compra/reporte.html',{
		'pagesize':'A4',
		'reporte': reporte[0],
		'prom': prom[0][0]
	})
#end def

def home(request):
	user = authenticate(username='admin', password='123456')
	login(request, user)
	return redirect('/compra/')
#end def

router = routers.DefaultRouter()

router.register(r'producto', ProductoViewSet)
router.register(r'cliente', ClienteViewSet)
router.register(r'sede', SedeViewSet)
router.register(r'compra', CompraViewSet)
router.register(r'log', LogViewSet)
router.register(r'factura', FacturaViewSet)