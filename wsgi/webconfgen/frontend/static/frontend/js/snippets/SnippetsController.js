(function() {
    'use strict';
    angular.module('snippets')
        .controller('SnippetsController', [
            'SnippetsService', '$log', '$q', '$mdBottomSheet',
            SnippetsController
        ]);
    function SnippetsController(SnippetsService, $log, $q, $mdBottomSheet) {
        var self = this;
        self.selectedTab = 0;
        self.searchText = null;
        self.selectedSnippets = [];
        self.content = '';
        self.checkRefreshContent = checkRefreshContent;
        self.getMatches = getMatches;
        self.fileImport = fileImport;
        self.fileRaw = fileRaw;
        self.snippetHash = hashToString(JSON.stringify(self.selectedSnippets));
        SnippetsService
            .loadAllSnippets()
                .then(function(snippets) {
                    self.snippets = [].concat(snippets);
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
                for (var i = selectedSnippets.length - 1; i >= 0; i--) {
                    SnippetsService.loadRawSnippet(selectedSnippets[i]).then(function(rawSnippet) {
                        self.content += '\r\n\r\n' + rawSnippet;
                        self.editor.setValue(self.content);
                    });
            }
        }
        function createFilterFor(query) {
            var lowercaseQuery = angular.lowercase(query);
            return function(element) {
                return angular.lowercase(element.name).indexOf(lowercaseQuery) === 0;
            };
        }
        function getMatches(query) {
            return query ? self.snippets.filter(createFilterFor(query)) : self.snippets;
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
