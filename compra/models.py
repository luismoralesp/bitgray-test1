from django.db import models
from django.core import validators

"""
	@name: Producto
	@author: Luis Miguel Morales Pajaro
	@business: bitgray
	Representa los productos disponibles en la tienda
"""
class Producto(models.Model):
	producto = models.CharField(max_length=40)
	precio   = models.PositiveIntegerField()
	descripcion = models.TextField()
	class Meta:
		db_table = "productos"
	#end class
#end class

"""
	@name: Cliente
	@author: Luis Miguel Morales Pajaro
	@business: bitgray
	Representa los clientes asociados a la tienda
"""
class Cliente(models.Model):
	documento = models.PositiveIntegerField()
	nombres = models.CharField(max_length=80)
	detalles = models.TextField()
	class Meta:
		db_table = "clientes"
	#end class
#end class

"""
	@name: Sede
	@author: Luis Miguel Morales Pajaro
	@business: bitgray
	Representa las sedes que tiene la tienda
"""
class Sede(models.Model):
	sede = models.CharField(max_length=40)
	direccion = models.TextField()
	class Meta:
		db_table = "sedes"
	#end class
#end class

"""
	@name: Compra
	@author: Luis Miguel Morales Pajaro
	@business: bitgray
	Representa las compras realizadas
"""
class Compra(models.Model):
	cliente = models.ForeignKey(Cliente, db_column="id_cliente")
	producto = models.ForeignKey(Producto, db_column="id_producto", null=True)
	sede = models.ForeignKey(Sede, db_column="id_sede", null=True, blank=True)
	precio = models.PositiveIntegerField(null=True, blank=True)

	class Meta:
		db_table = "compras"
	#end class

	def save(self, *args, **kwargs):
		if self.precio == None:
			self.precio = self.producto.precio
		#end if
		return super(Compra, self).save(*args, **kwargs)
	#end def

#end class

"""
	@name: Log
	@author: Luis Miguel Morales Pajaro
	@business: bitgray
	Representa las compras realizadas
"""
class Log(models.Model):
	fecha = models.DateTimeField(auto_now_add=True)
	descripcion = models.TextField()
	class Meta:
		db_table = "log"
	#end class
#end class


