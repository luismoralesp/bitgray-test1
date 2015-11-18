var controllers = angular.module('controllers', []);

controllers.controller('producto_controller', ['$scope', '$http',
	function ($scope, $http) {
		default_controller($scope, $http, '/compra/ws/producto/?format=json', [
			'producto',
			'precio',
			'descripcion'
		]);
	}
]);

controllers.controller('cliente_controller', ['$scope', '$http',
	function ($scope, $http) {
		default_controller($scope, $http, '/compra/ws/cliente/?format=json', [
			'documento',
			'nombres',
			'detalles'
		]);
	}
]);

controllers.controller('sede_controller', ['$scope', '$http',
	function ($scope, $http) {
		default_controller($scope, $http, '/compra/ws/sede/?format=json',[
			'sede',
			'direccion'
		]);
	}
]);

controllers.controller('compra_controller', ['$scope', '$http',
	function ($scope, $http) {
		default_controller($scope, $http, '/compra/ws/compra/?format=json', [
			'cliente',
			'producto',
			'sede',
			'precio'
		]);
		$http.get('/compra/ws/cliente/?format=json').success(function (data) {
			$scope.clientes = data.results;
		});
		$http.get('/compra/ws/producto/?format=json').success(function (data) {
			$scope.productos = data.results;
		});
		$http.get('/compra/ws/sede/?format=json').success(function (data) {
			$scope.sedes = data.results;
		});
	}
]);

controllers.controller('log_controller', ['$scope', '$http',
	function ($scope, $http) {
		default_controller($scope, $http, '/compra/ws/log/?format=json');
	}
]);

controllers.controller('factura_controller', ['$scope', '$http',
	function ($scope, $http) {
		$scope.buscar = function(){
			$http.get('/compra/ws/factura/?format=json&cliente__documento=' + $scope.documento).success(function(data){
				$scope.facturas = data.results;
				$scope.total_precio = data.total_precio;
				$scope.cliente = data.cliente;
			});
		};

		$scope.imprimir = function(){
			if ($scope.documento){
				window.open('pdf/' + $scope.documento + '/','_blank').focus();
			}
		};
	}
]);

function default_controller($scope, $http, url, default_obj){
	$http.get(url).success(function (data) {
		$scope.data = data;
	});
	$scope.clear = function(){
		$scope.obj = {};
		for (var i in default_obj){
			$scope.obj[default_obj[i]] = '';
		}
	};
	$scope.action = function(){
		var data = $scope.obj;
		for (var i in data){
			if (data[i] == ""){
				delete data[i];
			}
		}
		if ($scope.action_name === "Crear"){
			$http.post(url,data).success(function (data) {
				$http.get(url).success(function (data) {
					$scope.data = data;
					$scope.crear();
				});
			});
		}else
		if ($scope.action_name === "Editar"){
			$http.patch(url + '&id=' + $scope.action_id, data).success(function (data) {
				$http.get(url).success(function (data) {
					$scope.data = data;
					$scope.crear();
				});
			});
		}else{
			alert("not suported!");
		}
	};
	$scope.editar = function(p){
		$scope._id = "#" + p.id;
		$scope.action_id = p.id;
		$scope.obj = p;
		$scope.action_name = "Editar";
	};
	$scope.crear = function(){
		$scope.action_name = "Crear";
		$scope._id = "Nuevo";
		$scope.clear();
	};
	$scope.borrar = function(){
		var get = "";
		for (var i in $scope.delete_list){
			get += "&id=" + $scope.delete_list[i];
		}
		console.log(get);
		$http.delete(url + get).success(function (data) {
			$http.get(url).success(function (data) {
				$scope.data = data;
				$scope.clear();
			});
		});
	};

	$scope.prev = function(){
		if ($scope.data.previous){
			$http.get($scope.data.previous).success(function (data) {
				$scope.data = data;
			});
		}
	};
	$scope.next = function(){
		if ($scope.data.next){
			$http.get($scope.data.next).success(function (data) {
				$scope.data = data;
			});
		}
	};
	$scope.ckeck_delete_all = function (){
		$scope.delete_list = [];
		var all = document.querySelector("thead [type=checkbox]");
		var chks = document.querySelectorAll("tbody [type=checkbox]");
		for (var i in chks){
			chks[i].checked = all.checked;
			if (chks[i].checked && chks[i].value){
				$scope.delete_list.push(chks[i].value);
			}
		}
	};
	$scope.ckeck_delete = function (p){
		$scope.delete_list = [];
		var all = document.querySelector("thead [type=checkbox]");
		var chks = document.querySelectorAll("tbody [type=checkbox]");
		for (var i in chks){
			if (chks[i].checked && chks[i].value){
				$scope.delete_list.push(chks[i].value);
			}else{
				all.checked = false;
			}
		}
	};
	$scope.crear();
	$scope.clear();
	$scope.delete_list = [];
}