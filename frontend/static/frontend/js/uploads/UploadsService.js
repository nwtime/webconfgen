(function() {
    'use strict';
    angular
        .module('uploads')
            .service('UploadsService', [
                '$http',
                UploadsService
        ]);
    function UploadsService($http) {
        return {
            getUpload: function(uuid) {
                return $http.get('/api/uploads/' + uuid + '/mini/');
            },
            getFile: function(url) {
                return $http.get('');
            }
        };
    };
})();
