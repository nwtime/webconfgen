(function() {
    'use strict';
    angular
        .module('snippets', ['ngMaterial'])
            .config(function($httpProvider) {
                $httpProvider.defaults.xsrfCookieName = 'csrftoken';
                $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            });
})();
