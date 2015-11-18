from django.views.generic import TemplateView
from django.conf.urls import include, url
from views import router
import views

urlpatterns = [

	url(r'^ws/', include(router.urls)),
	url(r'', include('rest_framework.urls', namespace='rest_framework')),

	url(r'^$', TemplateView.as_view(template_name="compra/index.html")),

	url(r'pdf/(?P<documento>\d+)/', views.pdf),
	url(r'reporte/', views.reporte),

	url(r'^factura.html$',  TemplateView.as_view(template_name="compra/factura.html")),
	url(r'^producto.html$', TemplateView.as_view(template_name="compra/producto.html")),
	url(r'^cliente.html$', 	TemplateView.as_view(template_name="compra/cliente.html")),
	url(r'^sede.html$', 	TemplateView.as_view(template_name="compra/sede.html")),
	url(r'^compra.html$', 	TemplateView.as_view(template_name="compra/compra.html")),
	url(r'^log.html$', 		TemplateView.as_view(template_name="compra/log.html")),
]