(function() {
    'use strict';
    angular
        .module('uploads')
            .controller('UploadsController', [
                'UploadsService', '$log', '$q',
                UploadsController
        ]);
    function UploadsController(UploadsService, $log, $q) {
        var self = this;
        var currentUUID = window.location.toString().split('/')[3];
        UploadsService
            .getUpload(currentUUID)
                .then(function(response) {
                    self.upload = response.data;
                    $log.debug(self.upload.version);
                });
        function loadEditor() {
            self.editorInput = ace.edit('editor_input');
            self.editorInput.setTheme('ace/theme/chrome');
            self.editorInput
                .getSession()
                    .setMode('ace/mode/plain_text');
            self.editorOutput = ace.edit('editor_output');
            self.editorOutput.setTheme('ace/theme/chrome');
            self.editorOutput
                .getSession()
                    .setMode('ace/mode/plain_text');
        }
        angular.element(document).ready(loadEditor);
    };
})();
