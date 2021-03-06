(function() {
    'use strict';
    angular
        .module('snippets')
            .controller('SnippetsController', [
                'SnippetsService', '$log', '$q', '$mdToast',
                SnippetsController
        ]);
    function SnippetsController(SnippetsService, $log, $q, $mdToast) {
        var self = this;
        self.selectedTab = 1;
        self.searchText = null;
        self.selectedSnippets = [];
        self.content = '';
        self.selectedVersion = null;
        self.checkRefreshContent = checkRefreshContent;
        self.getMatches = getMatches;
        self.fileImport = fileImport;
        self.fileRaw = fileRaw;
        self.fileUpload = fileUpload;
        self.mutex_list = [];
        self.snippetHash = hashToString(JSON.stringify(self.selectedSnippets));
        self.isToastShown = false;
        SnippetsService
            .loadAllSnippets()
                .then(function(response) {
                    self.snippets = [].concat(response.data);
                });
        SnippetsService
            .loadAllVersions()
                .then(function(response) {
                    self.versions = [].concat(response.data);
                });
        function loadEditor() {
            self.editor = ace.edit('editor');
            self.editor.setTheme('ace/theme/chrome');
            self.editor
                .getSession()
                    .setMode('ace/mode/plain_text');
        }
        function checkRefreshContent(selectedSnippets) {
            var currentHash = hashToString(JSON.stringify(self.selectedSnippets));
            if (currentHash != self.snippetHash) {
               self.snippetHash = currentHash;
               refreshContent(selectedSnippets);
            }
        }
        function refreshContent(selectedSnippets) {
            self.content = '';
            var warn = false;
            var promiceList = [];
            self.mutex_list = [];
            for (var i = selectedSnippets.length - 1; i >= 0; i--) {
                var snippet = selectedSnippets[i];
                promiceList.push(SnippetsService.loadRawSnippet(snippet));
                self.mutex_list = self.mutex_list.concat(snippet.mutually_exclusive.filter(function(element) {
                    return self.mutex_list.indexOf(element) < 0;
                }));
            }
            $q.all(promiceList)
                .then(function(responses) {
                    for (var i = responses.length - 1; i >= 0; i--) {
                        self.content += responses[i].data + '\r\n\r\n';
                    }
                    self.editor.setValue(self.content, -1);
                });
        }
        function createFilterFor(query) {
            var lowercaseQuery = angular.lowercase(query);
            return function(element) {
                var lowercaseElement = angular.lowercase(element.name);
                if (self.selectedVersion === null) {
                    // do not set the isToastShown here
                    showToast('Select Version First');
                    return false;
                }
                if (self.mutex_list.indexOf(element.uuid) >= 0) {
                    return false;
                }
                var selectedVersion = self.selectedVersion.version;
                if (element.version.indexOf(selectedVersion) >= 0) {
                    return lowercaseElement.indexOf(lowercaseQuery) === 0;
                } else {
                    return false;
                }
            };
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
        function getMatches(query) {
            if (query) {
                return self.snippets.filter(createFilterFor(query));
            } else {
                return self.snippets;
            }
        }
        function hashToString(s) {
            return s.split('').reduce(function(a, b) {
                a = ((a << 5) - a) + b.charCodeAt(0);
                return a & a;
            },0);
        }
        function fileImport(element) {
            var file = element.files[0];
            var fileReader = new FileReader();
            fileReader.onload = function(event) {
                var content = event.target.result;
                self.editor.setValue(content, -1);
                self.content = content;
            };
            fileReader.readAsText(file);
        }
        function fileRaw() {
            var code = self.editor.getValue();
            var blob = new Blob([code], {type: 'text/plain'});
            var url = URL.createObjectURL(blob);
            window.open(url, '_blank');
        }
        function fileUpload() {
            var content = self.editor.getValue();
            var version = self.selectedVersion;
            if (version === null) {
                self.isToastShown = false;
                showToast('Select Version First');
                return;
            }
            if (content === '') {
                self.isToastShown = false;
                showToast('No Content To Parse');
                return;
            }
            SnippetsService
                .postForParse(content, version.version)
                    .then(function(response) {
                        var uuid = response.data.uuid;
                        window.location = '/' + uuid;
                    });
        }
        angular.element(document).ready(loadEditor);
    };
})();
