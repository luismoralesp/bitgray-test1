/*create view reporte as select avg(abs(case when compras.precio is not null then productos.precio - compras.precio else 0 end)) as avg, max(abs(productos.precio - compras.precio)) as max, min(abs(productos.precio - compras.precio)) as min, count(compras.id) as compras, sum(case when compras.precio is null then productos.precio else compras.precio end ) as ganancias from productos join compras on productos.id = compras.id_producto;

create view compras_promedio as select avg(c) from (select count(id) as c from
compras group by UNIX_TIMESTAMP(fecha)/1000/60) as c;

*/
delimiter //
create trigger log_producto_in after insert on productos
	FOR EACH ROW
	begin
		insert into log 
			(fecha, descripcion) 
		values 
		(current_timestamp, concat('se agrego un nuevo producto con nombre ', new.producto));
	end;//

create trigger log_producto_up after update on productos
	FOR EACH ROW
	begin
		insert into log 
			(fecha, descripcion) 
		values 
		(current_timestamp, concat('se edito el producto con nombre ', old.producto));
	end;//

create trigger log_producto_del after delete on productos
	FOR EACH ROW
	begin
		insert into log 
			(fecha, descripcion) 
		values 
		(current_timestamp, concat('se borro el producto con nombre ', old.producto));
	end;//

/********************************/
create trigger log_cliente_in after insert on clientes
	FOR EACH ROW
	begin
		insert into log 
			(fecha, descripcion) 
		values 
		(current_timestamp, concat('se agrego un nuevo cliente con nombre ', new.nombres));
	end;//

create trigger log_cliente_up after update on clientes
	FOR EACH ROW
	begin
		insert into log 
			(fecha, descripcion) 
		values 
		(current_timestamp, concat('se edito el cliente con nombre ', old.nombres));
	end;//

create trigger log_cliente_del after delete on clientes
	FOR EACH ROW
	begin
		insert into log 
			(fecha, descripcion) 
		values 
		(current_timestamp, concat('se borro el cliente con nombre ', old.nombres));
	end;//

/******************/
create trigger log_sede_in after insert on sedes
	FOR EACH ROW
	begin
		insert into log 
			(fecha, descripcion) 
		values 
		(current_timestamp, concat('se agrego un nuevo sede con nombre ', new.sede));
	end;//

create trigger log_sede_up after update on sedes
	FOR EACH ROW
	begin
		insert into log 
			(fecha, descripcion) 
		values 
		(current_timestamp, concat('se edito la sede con nombre ', old.sede));
	end;//

create trigger log_sede_del after delete on sedes
	FOR EACH ROW
	begin
		insert into log 
			(fecha, descripcion) 
		values 
		(current_timestamp, concat('se borro la sede con nombre ', old.sede));
	end;//
/*********************/
create trigger log_compra_in after insert on compras
	FOR EACH ROW
	begin
		insert into log 
			(fecha, descripcion) 
		values 
		(current_timestamp, concat('se agrego un nuevo compra con id ', new.id));
	end;//

create trigger log_compra_up after update on compras
	FOR EACH ROW
	begin
		insert into log 
			(fecha, descripcion) 
		values 
		(current_timestamp, concat('se edito la compra con id ', old.id));
	end;//

create trigger log_compra_del after delete on compras
	FOR EACH ROW
	begin
		insert into log 
			(fecha, descripcion) 
		values 
		(current_timestamp, concat('se borro la compra con id ', old.id));
	end;//
delimiter ;