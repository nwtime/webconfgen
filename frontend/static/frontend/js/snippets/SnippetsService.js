(function() {
    'use strict';
    angular.module('snippets')
        .service('SnippetsService', [
            '$http',
            SnippetsService
        ]);
    function SnippetsService($http) {
        return {
            loadAllSnippets: function() {
                return $http.get('/api/snippets/all', {
                    cache: true
                }).then(function(response) {
                        return response.data;
                });
            },
            loadRawSnippet: function(snippet) {
                return $http.get(snippet.url + 'raw', {
                    cache: true
                }).then(function(response) {
                    return response.data;
                });
            }
        };
    };
})();
