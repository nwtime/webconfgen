(function() {
    'use strict';
    angular
        .module('uploads', ['ngMaterial'])
            .config(function($httpProvider) {
                $httpProvider.defaults.xsrfCookieName = 'csrftoken';
                $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            });
})();
