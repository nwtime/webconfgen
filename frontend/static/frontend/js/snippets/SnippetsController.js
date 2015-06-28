(function() {
    'use strict';
    angular.module('snippets')
        .controller('SnippetsController', [
            'SnippetsService', '$log', '$q',
            SnippetsController
        ]);
    function SnippetsController(SnippetsService, $log, $q) {
        var self = this;
        self.searchText = null;
        self.selectedSnippets = [];
        self.content = '';
        self.item = null;
        self.checkRefreshContent = checkRefreshContent;
        self.getMatches = getMatches;
        self.snippetHash = hashToString(JSON.stringify(self.selectedSnippets));
        SnippetsService
            .loadAllSnippets()
                .then(function(snippets) {
                    self.snippets = [].concat(snippets);
                });
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
                        editor.setValue(self.content);
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
    };
})();
