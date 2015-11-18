/**
* @name: Compra JS
* 
**/
var compra_app = angular.module('compra_app', [
	'ngRoute',
	'controllers'
]);

compra_app.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
});
