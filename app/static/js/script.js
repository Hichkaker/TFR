(function() {
    angular.module('app', []).config(function($interpolateProvider){
      $interpolateProvider.startSymbol('#|');
      $interpolateProvider.endSymbol('|#');
    })
    .controller('TableControl', TableControl);

    TableControl.$inject = ['$scope', '$filter', '$http']
    function TableControl ($scope, $filter, $http) {
        var vm = this
        vm.rowCollection = []
        var daysOfWeek = ['mon', 'tue', 'wed', 'thu', 'fri','sat', 'sun']
        
        $http.get('/volunteer').then(function(resp) {

           mappedData = resp.data.volunteers.map(function(volunteer, index) {
                var available = []
                for(var i = 0; i < daysOfWeek.length; i++) {
                    if (volunteer[daysOfWeek[i]] === true) {
                        available.push(daysOfWeek[i])
                    };
                };
                volunteer.availability = available.join(', ')
                return volunteer
            }); 
            console.log(mappedData);
            vm.rowCollection = mappedData   

        })

        selectedVolunteers = function(volunteer){
             if (volunteer.dispatch) {
                return true
             } else {
                return false
             }
        }

        vm.submit = function(volunteers, project){
            var selected = volunteers.filter(selectedVolunteers)
                .map(function(volunteer){
                    return volunteer.id
                });
            if (!project) {
                project = {
                    name: "default",
                    description: "something",
                    tools: "shovel",
                    day: "Sunday",
                    organization: "Mozilla"
                }
            }
            var data = {project: project, volunteers:selected}
            console.log('post up', data);
            $http.post('/project/new', data).then(function(resp) {
            })
        }
    }
}).call(this);
