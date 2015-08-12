(function() {
    'use strict';
    angular
        .module('uploads')
            .controller('UploadsController', [
                'UploadsService', '$log', '$q', '$timeout',
                UploadsController
        ]);
    function UploadsController(UploadsService, $log, $q, $timeout) {
        var self = this;
        self.inputUrl = null;
        self.outputUrl = null;
        self.inputLoading = true;
        self.outputLoading = true;
        self.selectedTab = 1;
        self.fileRaw = fileRaw;
        self.fileUpload = fileUpload;
        self.uuid = window.location.toString().split('/')[3];

        function refreshUpload() {
            UploadsService
                .getUpload(self.uuid)
                    .then(function(response) {
                        self.upload = response.data;
                        refreshInputFile();
                        refreshOutputFile();
                    });
        }

        function refreshInputFile() {
            if (self.upload.input_file_url) {
                if (self.upload.input_file_url != self.inputUrl) {
                    self.inputLoading = true;
                    self.inputUrl = self.upload.input_file_url;
                    UploadsService
                        .getInputFile(self.upload)
                            .then(function(response) {
                                self.editorInput.setValue(response.data, -1);
                                self.inputLoading = false;
                            });
                }
            } else {
                $timeout(refreshUpload, 1000);
            }
        }

        function refreshOutputFile() {
            if (self.upload.output_file_url) {
                if (self.upload.output_file_url != self.outputUrl) {
                    self.outputLoading = true;
                    self.outputUrl = self.upload.output_file_url;
                    UploadsService
                        .getOutputFile(self.upload)
                            .then(function(response) {
                                self.editorOutput.setValue(response.data, -1);
                                self.outputLoading = false;
                            });
                }
            } else {
                $timeout(refreshUpload, 1000);
            }
        }

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
            refreshUpload();
        }

        function fileRaw() {
            var code = self.editorOutput.getValue();
            var blob = new Blob([code], {type: 'text/plain'});
            var url = URL.createObjectURL(blob);
            window.open(url, '_blank');
        }

        function fileUpload() {
            self.inputLoading = true;
            var content = self.editorInput.getValue();
            UploadsService
                .updateContent(content, self.upload)
                    .then(function(response) {});
        }
        angular.element(document).ready(loadEditor);
    };
})();
