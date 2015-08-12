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
                return $http.get('/api/uploads/' + uuid + '/mini/', {
                    cache: false
                });
            },
            getInputFile: function(upload) {
                return $http.get(upload.input_file_url, {
                    cache: true
                });
            },
            getOutputFile: function(upload) {
                return $http.get(upload.output_file_url, {
                    cache: true
                });
            },
            updateContent: function(content, upload) {
                return $http.put(upload.url, {
                    'version': upload.version,
                    'input_string': content
                });
            }
        };
    };
})();
