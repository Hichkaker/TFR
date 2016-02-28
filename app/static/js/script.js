(function() {
    angular.module('app', ['smart-table']).config(function($interpolateProvider){
      $interpolateProvider.startSymbol('#|');
      $interpolateProvider.endSymbol('|#');
    })
    .controller('TableControl', ['$scope', '$filter', '$http', function ($scope, $filter, $http) {
      
        var table = [];

        $http.get('/volunteer').then(function(resp) {
            $scope.rowCollection = resp.data.volunteers;
        }),

        $scope.rowCollection = table;

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
