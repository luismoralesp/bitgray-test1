/**
* @name: Compra JS
* 
**/

compra_app.config(['$routeProvider','$locationProvider', '$httpProvider',
    function($routeProvider, $locationProvider, $httpProvider){
		console.log($httpProvider);
		$httpProvider.defaults.headers.common.Authorization = 'Token 1';
		$routeProvider.
			when('/factura', {
				templateUrl: 'factura.html',
				controller: 'factura_controller'
			}).
			when('/producto', {
				templateUrl: 'producto.html',
				controller: 'producto_controller'
			}).
			when('/cliente', {
				templateUrl: 'cliente.html',
				controller: 'cliente_controller'
			}).
			when('/sede', {
				templateUrl: 'sede.html',
				controller: 'sede_controller'
			}).
			when('/compra', {
				templateUrl: 'compra.html',
				controller: 'compra_controller'
			}).
			when('/log', {
				templateUrl: 'log.html',
				controller: 'log_controller'
			}).
			otherwise({
				redirectTo: '/producto'
			});
	}
]);