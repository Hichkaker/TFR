(function() {
    angular.module('app', []).config(function($interpolateProvider){
      $interpolateProvider.startSymbol('#|');
      $interpolateProvider.endSymbol('|#');
    })
    .controller('TableControl', ['$scope', '$filter', '$http', function ($scope, $filter, $http) {
        var vm = this
        vm.rowCollection = []
        var daysOfWeek = ['mon', 'tues', 'wed', 'thu', 'fri','sat', 'sun']
        
        $http.get('/volunteer').then(function(resp) {

           mappedData = resp.data.volunteers.map(function(volunteer, index) {
                var available = []
                for(var i = 0; i < daysOfWeek.length; i++) {
                    if (volunteer[daysOfWeek[i]] === true) {
                        available.push(daysOfWeek[i])
                    };
                };
                volunteer.availability = available
                return volunteer
            }); 
            console.log(mappedData);
            vm.rowCollection = mappedData           
        })
    }]);

}).call(this);
