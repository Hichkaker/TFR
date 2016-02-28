(function() {
    angular.module('app', ['smart-table']).config(function($interpolateProvider){
      $interpolateProvider.startSymbol('#|');
      $interpolateProvider.endSymbol('|#');
    })
    .controller('TableControl', ['$scope', '$filter', '$http', function ($scope, $filter, $http) {
      
        var table = {content:null};

        $http.get('https://tfr2.herokuapp.com/volunteer').then(function(data) {
            return table.content = data;
        }),

        $scope.rowCollection = table.content;

    }]).directive('csSelect', function () {
    return {
        require: '^stTable',
        template: '<input type="checkbox"/>',
        scope: {
            row: '=csSelect'
        },
        link: function (scope, element, attr, ctrl) {

            element.bind('change', function (evt) {
                scope.$apply(function () {
                    ctrl.select(scope.row, 'multiple');
                });
            });

            scope.$watch('row.isSelected', function (newValue, oldValue) {
                if (newValue === true) {
                    element.parent().addClass('st-selected');
                } else {
                    element.parent().removeClass('st-selected');
                }
            });
        }
    };
});;

}).call(this);
