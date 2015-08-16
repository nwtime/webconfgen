(function() {
    'use strict';
    angular
        .module('uploads')
            .controller('UploadsController', [
                'UploadsService', '$log', '$q', '$timeout', '$mdToast',
                UploadsController
        ]);
    function UploadsController(UploadsService, $log, $q, $timeout, $mdToast) {
        var self = this;
        self.inputTimeout = null;
        self.inputUrl = null;
        self.outputTimeout = null;
        self.outputUrl = null;
        self.inputLoading = true;
        self.outputLoading = true;
        self.selectedTab = 1;
        self.fileRaw = fileRaw;
        self.isToastShown = true;
        self.fileUpload = fileUpload;
        self.uuid = window.location.toString().split('/')[3];

        function refreshUpload() {
            UploadsService
                .getUpload(self.uuid)
                    .then(function(response) {
                        self.upload = response.data;
                        checkRefreshInputFile();
                        checkRefreshOutputFile();
                    });
        }

        function refreshInputFile(content) {
            self.editorInput.setValue(content, -1);
            self.inputLoading = false;
        }

        function refreshOutputFile(content) {
            self.editorOutput.setValue(content, -1);
            self.outputLoading = false;
        }

        function checkRefreshInputFile() {
            if (self.upload.status === 'ER') {
                self.inputLoading = false;
                UploadsService
                    .getInputFile(self.upload)
                        .then(function(response) {
                            refreshInputFile(response.data);
                        });
                return;
            }
            if (self.upload.status == 'PR' && self.inputLoading === true) {
                UploadsService
                    .getInputFile(self.upload)
                        .then(function(response) {
                            refreshInputFile(response.data);
                        });
                return;
            }
            if (self.upload.input_file_url) {
                if (self.upload.input_file_url != self.inputUrl) {
                    self.inputLoading = true;
                    self.inputUrl = self.upload.input_file_url;
                    UploadsService
                        .getInputFile(self.upload)
                            .then(function(response) {
                                refreshInputFile(response.data);
                            });
                }
            } else {
                if (self.inputTimeout) {
                    $timeout.cancel(self.inputTimeout);
                }
                self.inputTimeout = $timeout(refreshUpload, 1000);
            }
        }

        function checkRefreshOutputFile() {
            if (self.upload.status === 'ER') {
                self.outputLoading = false;
                refreshOutputFile('Parser has failed. Try again later');
                return;
            }
            if (self.upload.status === 'RE' && self.outputLoading === true) {
                UploadsService
                    .getOutputFile(self.upload)
                        .then(function(response) {
                            refreshOutputFile(response.data);
                        });
                return;
            }
            if (self.upload.output_file_url) {
                if (self.upload.output_file_url != self.outputUrl) {
                    self.outputLoading = true;
                    self.outputUrl = self.upload.output_file_url;
                    UploadsService
                        .getOutputFile(self.upload)
                            .then(function(response) {
                                refreshOutputFile(response.data);
                            });
                }
            } else {
                if (self.outputTimeout) {
                    $timeout.cancel(self.outputTimeout);
                }
                self.outputTimeout = $timeout(refreshUpload, 1000);
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
        function showToast(content) {
            if (self.isToastShown === false) {
                $mdToast.show(
                    $mdToast.simple()
                        .content(content)
                        .position('top right')
                        .theme('default')
                );
                self.isToastShown = true;
            }
        }

        function fileUpload() {
            self.inputLoading = true;
            var content = self.editorInput.getValue();
            if (content === '') {
                self.isToastShown = false;
                showToast('No Content To Parse');
                return;
            }
            UploadsService
                .updateContent(content, self.upload)
                    .then(function(response) {
                        refreshUpload();
                    });
        }
        angular.element(document).ready(loadEditor);
    };
})();
