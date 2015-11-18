from rest_framework import serializers
import models

"""
	@name: ProductoSerializer
	@author: Luis Miguel Morales Pajaro
	@buisiness: bitgray

"""
class ProductoSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Producto
		fields = ['id', 'producto', 'precio', 'descripcion', ]
	#end class
#end class

"""
	@name: ClienteSerializer
	@author: Luis Miguel Morales Pajaro
	@buisiness: bitgray

"""
class ClienteSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Cliente
		fields = ['id', 'documento', 'nombres', 'detalles', ]
	#end class
#end class

"""
	@name: SedeSerializer
	@author: Luis Miguel Morales Pajaro
	@buisiness: bitgray

"""
class SedeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Sede
		fields = ['id', 'sede', 'direccion', ]
	#end class
#end class

"""
	@name: CompraSerializer
	@author: Luis Miguel Morales Pajaro
	@buisiness: bitgray

"""
class CompraSerializer(serializers.HyperlinkedModelSerializer):
	cliente = serializers.PrimaryKeyRelatedField(queryset=models.Cliente.objects)
	producto = serializers.PrimaryKeyRelatedField(queryset=models.Producto.objects)
	sede = serializers.PrimaryKeyRelatedField(queryset=models.Sede.objects, required=False)
	cliente_nombres = serializers.SerializerMethodField('calc_cliente_nombres')
	producto_producto = serializers.SerializerMethodField('calc_producto_producto')
	sede_sede = serializers.SerializerMethodField('calc_sede_sede')

	def calc_cliente_nombres(self, obj):
		return obj.cliente.nombres
	#end def

	def calc_producto_producto(self, obj):
		return obj.producto.producto
	#end def

	def calc_sede_sede(self, obj):
		if obj.sede:
			return obj.sede.sede
	#end def

	def create(self, validated_data):
		cliente = validated_data.pop('cliente')
		producto = validated_data.pop('producto')
		if 'sede' in validated_data:
			sede = validated_data.pop('sede')
		else:
			sede = None
		#end def

		compra = models.Compra.objects.create(cliente=cliente, producto=producto, sede=sede, **validated_data)
		return compra
	#end def

	def get_validation_exclusions(self):
		exclusions = super(CompraSerializer, self).get_validation_exclusions()
		return exclusions + ['sede']
	#end def

	class Meta:
		model = models.Compra
		fields = ['id', 'cliente', 'cliente_nombres', 'producto', 'producto_producto', 'sede', 'sede_sede', 'precio', ]
	#end class
#end class

"""
	@name: LogSerializer
	@author: Luis Miguel Morales Pajaro
	@buisiness: bitgray

"""
class LogSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Log
		fields = ['id', 'fecha', 'descripcion', ]
	#end class
#end class

"""
	@name: FacturaSerializer
	@author: Luis Miguel Morales Pajaro
	@buisiness: bitgray

"""
class FacturaSerializer(serializers.HyperlinkedModelSerializer):
	producto = ProductoSerializer()
	sede = SedeSerializer()
	cliente = ClienteSerializer()
	precio = serializers.SerializerMethodField('calc_precio')

	def calc_precio(self, obj):
		if obj.precio:
			return obj.precio
		if obj.producto:
			return obj.producto.precio
		return None
	#end def

	class Meta:
		model = models.Compra
		fields = ['id', 'producto', 'sede', 'precio', 'cliente']
	#end class
#end class
