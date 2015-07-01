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
                });
            },
            loadRawSnippet: function(snippet) {
                return $http.get(snippet.url + 'raw', {
                    cache: true
                });
            },
            loadAllVersions: function() {
                return $http.get('/api/versions/all', {
                    cache: true
                });
            },
            postForParse: function(content) {
                return $http.post();
            }
        };
    };
})();
