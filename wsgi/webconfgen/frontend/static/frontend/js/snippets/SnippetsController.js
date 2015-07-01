(function() {
    'use strict';
    angular.module('snippets')
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
            self.editor.getSession().setMode('ace/mode/plain_text');
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
                    self.editor.setValue(self.content);
                });
        }
        function createFilterFor(query) {
            var lowercaseQuery = angular.lowercase(query);
            return function(element) {
                var lowercaseElement = angular.lowercase(element.name);
                if (self.selectedVersion === null) {
                    showVersionWarnToast();
                    return false;
                }
                if (self.mutex_list.indexOf(element.uuid) >= 0) {
                    return false;
                }
                var selectedVersion = self.selectedVersion.version;
                $log.debug(selectedVersion);
                if (element.version.indexOf(selectedVersion) >= 0) {
                    return lowercaseElement.indexOf(lowercaseQuery) === 0;
                } else {
                    return false;
                }
            };
        }
        function showVersionWarnToast() {
            if (self.isToastShown === false) {
                $mdToast.show(
                    $mdToast.simple()
                        .content('Select Version First')
                        .position('top right')
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
            self.selectedTab = 1;
            var fileReader = new FileReader();
            fileReader.onload = function(event) {
                var content = event.target.result;
                self.editor.setValue(content);
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
        angular.element(document).ready(loadEditor);
    };
})();
