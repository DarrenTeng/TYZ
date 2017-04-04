var app = angular.module('familyApp', ['ngGrid', 'ngRoute', 'ui.bootstrap', 'ngCookies', 'angularBootstrapNavTree', 'ngAnimate'], function ($httpProvider) {
	//// Use x-www-form-urlencoded Content-Type
	//  $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
	 
	//  /**
	//   * The workhorse; converts an object to x-www-form-urlencoded serialization.
	//   * @param {Object} obj
	//   * @return {String}
	//   */ 
	//  var param = function(obj) {
	//    var query = '', name, value, fullSubName, subName, subValue, innerObj, i;
	      
	//    for(name in obj) {
	//      value = obj[name];
	        
	//      if(value instanceof Array) {
	//        for(i=0; i<value.length; ++i) {
	//          subValue = value[i];
	//          fullSubName = name + '[' + i + ']';
	//          innerObj = {};
	//          innerObj[fullSubName] = subValue;
	//          query += param(innerObj) + '&';
	//        }
	//      }
	//      else if(value instanceof Object) {
	//        for(subName in value) {
	//          subValue = value[subName];
	//          fullSubName = name + '[' + subName + ']';
	//          innerObj = {};
	//          innerObj[fullSubName] = subValue;
	//          query += param(innerObj) + '&';
	//        }
	//      }
	//      else if(value !== undefined && value !== null)
	//        query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
	//    }
	      
	//    return query.length ? query.substr(0, query.length - 1) : query;
	//  };
	 
	//  // Override $http service's default transformRequest
	//  $httpProvider.defaults.transformRequest = [function(data) {
	//    return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
	//  }];
	}).config(function ($routeProvider) {
	    $routeProvider.when('/MyVMs', {
            controller: 'HomeCtrl',
            templateUrl: '../static/Resource/home.html',
            publicAccess: true
	    //}).when('/NewVm', {
	    //    controller: 'HomeCtrl',
	    //    templateUrl: '../static/Resource/home.html',
	    //    publicAccess: true,
	    //    mode: "create"
        }).when('/Management', {
            controller: 'ManageCtr',
            templateUrl: '../static/Resource/Management.html'
        }).otherwise({
            redirectTo: '/MyVMs'
        });
    }).filter('Count', function ($filter) {
        return function (input) {
            var total = 0;
            for (var i in input) {
                if (angular.isNumber(input[i])) {
                    total += input[i];
                }
                
            }
            total = $filter('number')(total,2);
            return total;
        };
    }).filter('CaclAll', function ($filter) {
        return function (input) {
            var total = 0;
            for (var i in input) {
                angular.forEach(input[i], function (key, index) {
                    if (angular.isNumber(input[i][index])) {
                        total += input[i][index];
                    }
                });
            }
            total = $filter('number')(total,2);
            return total;
        };
    }).filter('CaclClumn', function ($filter) {
        return function (input, item) {
            var total = 0;
            angular.forEach(input, function (data, index) {
                total += data[item];
            });
            if (isNaN(total)) {
                return '';
            }
            total = $filter('number')(total,2);
            return total;
        };
    }).filter('formatDate',function($filter){
    	return function(input,mode) {
			if(mode == 'staDay'){
				return $filter('date')(input, 'yyyy-MM-dd');
			} else if (mode == 'staYear') {
				return $filter('date')(input, 'yyyy');
			} else if (mode == 'staMonth') {
				return $filter('date')(input, 'yyyy-MM');
			} else{
				return $filter('date')(input, 'yyyy-MM-dd');
			}
		}
    });

app.service('messageService', ['$rootScope', function ($rootScope) {
    return {
        publish: function (name, parameters) {
            $rootScope.$emit(name, parameters);
        },
        subscribe: function (name, listener) {
            $rootScope.$on(name, listener);
        }

    };
}]);

app.controller('NavbarCtrl', ['$scope', '$location', '$http', '$cookies', 'messageService', function ($scope, $location, $http, $cookies, messageService) {
    $scope.language = new LanguageUtility();
    $scope.init = function () {
        var loader = {
            method: 'GET',
            url: '/getCurrentUser'
        };

        $http(loader).success(function (resp) {
            if (resp.result) {
                $scope.username = resp.data.name;
            }
            else {
                alert(resp.error);
            }
        });
    }

    $scope.init();

    $scope.isActive = function (route) {
        if ($location.path().indexOf('/dropdown') == 0) {
            return route === '/dropdown';
        }
        return route === $location.path();
    };

    $scope.logoff = function () {
        var loader = {
            method: 'GET',
            url: '/user/signout'
        };

        $http(loader).success(function (data) {
            window.location.href = '/user/login';
            //if (!data.success) {
            //    alert("cuola");
            //} else {
            //    window.location.href = 'index.html';
            //}
        });

    };

    $scope.ChangePW = function () {
        $('#myModal').modal();
    };

    $scope.confirmchange = function () {
        if ($scope.UserPass == "") {
            $scope.isvilidate = true;
            $scope.ChangePW.ErrorMsg = "The old password can't be empty.";
            return;
        } else if ($scope.UserNewPass != $scope.UserconfirmPass) {
            $scope.isvilidate = true;
            $scope.ChangePW.ErrorMsg = "The confirm password is not same with the new password.";
            return;
        } else if ($scope.UserNewPass == $scope.UserPass) {
            $scope.isvilidate = true;
            $scope.ChangePW.ErrorMsg = "The new password can't be same with the old password.";
            return;
        } else {
            $scope.isvilidate = false;
        }
        var loader = {
            method: 'POST',
            url: '/user/changepassword',
            data: {
                oldpassword: $scope.UserPass,
                newpassword: $scope.UserNewPass
            }
        };

        $http(loader).success(function (data) {
            if (!data.result) {
                $scope.isvilidate = true;
                $scope.ChangePW.ErrorMsg = data.error;
                return;
            } else {
                $('#myModal').modal('hide');
            }
        });

    };

   // messageService.publish('newVM', {});

}]).controller('BottomNavbarCtrl', ['$scope', '$location', '$http', '$cookies', 'messageService', function ($scope, $location, $http, $cookies, messageService) {
    $scope.language = new LanguageUtility();
    $scope.init = function () {
        var loader = {
            method: 'GET',
            url: '/getCurrentUser'
        };

        $http(loader).success(function (resp) {
            if (resp.result) {
                $scope.username = resp.data.name;
            }
            else {
                alert(resp.error);
            }
        });
    }

    $scope.init();

    $scope.isActive = function (route) {
        if ($location.path().indexOf('/dropdown') == 0) {
            return route === '/dropdown';
        }
        return route === $location.path();
    };

    $scope.NavBarClick = function (itemName) {
        messageService.publish('NavBarClick', itemName);
    }

}]).controller('HomeCtrl', ['$scope', '$http', '$interval', 'messageService', function ($scope, $http, $interval, messageService) {

    $scope.language = new LanguageUtility();
    $scope.MyVDSList = [];
    $scope.showObject = null;
    $scope.MyVDSTemplateList = [];
    $scope.MyGuestOsNameList = [];
    $scope.MyOsVersionList = [];
    $scope.loadingKey = null;
    $scope.LanguageList = [];
    $scope.selected = null;
    
    $scope.loadUserVNList = function () {
        var loader = {
            method: 'GET',
            url: '/GetVMList'
        };

        $http(loader).success(function (resp) {
            if (resp.result) {
                $scope.MyVDSList = resp.data;
            } else {
                window.location.href = 'index.html';
            }
        });
    }

    $scope.selectedVMItem = [];
    $scope.gridOptions = {
        data: 'VMListData',
        columnDefs: [
            { field: 'NAME', displayName: 'NAME' },
            { field: 'STATUS', displayName: 'STATUS' },
            { field: 'LOCATION', displayName: 'LOCATION' },
            { field: 'DNS_NAME', displayName: 'DNS NAME' },
            { field: 'IP_ADDRESS', displayName: 'IP ADDRESS' }],
        selectedItems: $scope.selectedVMItem,
        multiSelect: false,
        init: function (grid, $scope) { $scope.gridOptions.selectItem(0, true); }

    };

    $scope.UpdateUserVMListCtrl = function () {
        var loader = {
            method: 'GET',
            url: '/GetVMList'
        };

        $http(loader).success(function (resp) {
            if (resp.result) {
                $scope.VMListData = new Array(resp.data.length)
                for (index = 0; index < resp.data.length; index++) {

                    $scope.VMListData[index] = {
                        NAME: resp.data[index].name,
                        STATUS: resp.data[index].status,
                        LOCATION: resp.data[index].ip,
                        DNS_NAME: resp.data[index].dns_name,
                        IP_ADDRESS: resp.data[index].ip
                    };
                };
                
            }
        })
    }

    $scope.MyVDSList = [];
    $scope.mode = "showList";// create, detail
    $scope.showObject = null;
    $scope.MyVDSTemplateList = [];
    $scope.MyGuestOsNameList = [];
    $scope.MyOsVersionList = [];
    $scope.loadingKey = null;
    $scope.LanguageList = [];
    $scope.loadUserVNList();
    $scope.UpdateUserVMListCtrl();

    $scope.createNew = function () {
        $scope.GetOsNameList();
        $scope.GetOsVersionList();
        $scope.GetLanguageList();
        $scope.mode = "create";
    }

    $scope.showDetail = function (Item) {

        $scope.mode = "detail";
        $scope.GetOsNameList();
        $scope.GetOsVersionList();
        $scope.GetLanguageList();
        $scope.showObject = Item;
        messageService.publish('changeStatus', Item.name);
    }
    $scope.changeStatus = function (Item) {

        $scope.selected = Item;
    }
    //add here
    $scope.GetOsNameList = function () {
        $http({
            method: "GET",
            url: "/api/GetOSList",
        }).then(function mySucces(resp) {
            $scope.MyGuestOsNameList = resp.data.data;   
            
        }, function myError(response) {
            $scope.myWelcome = response.statusText;
        });
    }

    $scope.GetLanguageList = function () {
        $http({
            method: "GET",
            url: "/api/GetLangList",
        }).then(function mySucces(resp) {
            $scope.LanguageList = resp.data.data;

        }, function myError(response) {
            $scope.myWelcome = response.statusText;
        });
    }

    $scope.GetOsVersionList = function () {
        $http({
            method: "GET",
            url: "/api/GetOSVersionList",
        }).then(function mySucces(resp) {
            $scope.MyOsVersionList = resp.data.data;

        }, function myError(response) {
            $scope.myWelcome = response.statusText;
        });
    }

    $scope.ShowList = function () {
        $scope.mode = "showList";
        $scope.loadUserVNList();
        //if ($scope.selected == null && $scope.MyVDSList != null)
        //{
        //    $scope.selected = $scope.MyVDSList[0];
        //}
    }

    $scope.ShowList();

    $scope.createNew = function () {
        $scope.mode = "create";
        $scope.GetOsNameList();
        $scope.GetOsVersionList();
        $scope.GetLanguageList();
        
    }

    $scope.showDetail = function (Item) {

        $scope.mode = "detail";
        $scope.GetOsNameList();
        $scope.GetOsVersionList();
        $scope.GetLanguageList();
        $scope.showObject = Item;
        messageService.publish('changeStatus', Item.name);
        $scope.selected = Item;
    }

    $scope.selectedRow = 0;
    $scope.changeStatus = function (Index) {
        $scope.selectedRow = Index;
    }
   
    $scope.version = function (Guest_Os) {
        if ($scope.Guest_Os == 'Windows 10 Enterprise 64-bit' ) {
            return true;
        }else
            if($scope.Guest_Os == 'Windows 10 Enterprise 32-bit'){
                return true;
            }else
                if($scope.Guest_Os =='Windows 10 Professional 64-bit'){
                    return true;
                }else
                    if ($scope.Guest_Os == 'Windows 10 Professional 32-bit') {
                        return true;
                    }
    }


    $scope.Guest_Os_Version = '5';
    $scope.CreateNewVirtualMachine = function () {
        if ($scope.Confirm_Password != $scope.Password) {
            alert("wrong password!");
        }

        $http({
            method: "POST",
            url: "/api/CreateNewVirtualMachine",

            data: {
                project_name: $scope.ProjectName,
                guest_os: $scope.Guest_Os,
                guest_os_version: $scope.Guest_Os_Version,
                language: $scope.GetLanguageList,
                dns_name: $scope.DNS_Name,
                domain_name: $scope.DomainNarr,
                vcpu: $scope.vCPU,
                memory: $scope.Memory,
                storage: $scope.Storage,
                user_name: $scope.User_Name,
                password: $scope.Password,
            }
        }).then(function mySucces(resp) {
            $scope.Back();
            if (resp.data.result) {
                $('#LoadModal').modal('static');
                $scope.loadCreateStatus(resp.data.data);
                
            }
        }, function myError(response) {
            $scope.myWelcome = response.statusText;
        });
    };

    $scope.Back = function () {
        $scope.ShowList();
    }

    $scope.CreateNewImage = function () {
        if ($scope.confirmPassword != $scope.VMPassword) {
            alert("wrong password!");
        }
        
        $http({
            method: "POST",
            url: "/api/vc/newvm",

            data: {
                proj_name: $scope.PrjName,
                dns_name: $scope.DNSName,
                img_name: $scope.Image,
                size: $scope.Size,
                user_name: $scope.VMUserName,
                password: $scope.VMPassword
            }
        }).then(function mySucces(resp) {
            if (resp.data.result) {
                $('#LoadModal').modal('static');
                $scope.loadCreateStatus(resp.data.data);
            }
        }, function myError(response) {
            $scope.myWelcome = response.statusText;
        });
    };
    $scope.loadCreateStatus = function (TaskID) {
        $scope.loadingKey = $interval(function () {
            $http({
                method: "POST",
                url: "/api/vc/gettaskstatus",
                data: {
                    task_id: TaskID
                }
            }).then(function mySucces(resp) {
                if (resp.data.result) {
                    var status = resp.data.data;
                    if (status == "Running") {

                    } else if (status == "Done") {
                        $interval.cancel($scope.loadingKey);
                        $('#LoadModal').modal('hide');
                        $scope.Back();
                    } else {
                        $interval.cancel($scope.loadingKey);
                        $('#CreateError').html(resp.data.error);
                        $scope.showPage();
                    }
                }
            }, function myError(response) {
                $scope.myWelcome = response.statusText;
            });
        }, 1000);

        
    };

    $scope.showPage = function () {
        document.getElementById("loader").style.display = "none";
        document.getElementById("myDiv").style.display = "block";
    };

    $scope.Gettemplates = function () {
        $http({
            method: "GET",
            url: "/api/vc/getalltemplates",
        }).then(function mySucces(resp) {
            if (resp.data.result) {
                $scope.MyVDSTemplateList = resp.data.data;
            }
        }, function myError(response) {
            $scope.myWelcome = response.statusText;
        });
    }

    $scope.DeleteVMItem = function (Item) {
        $http({
            method: "POST",
            url: "/delVMItem",
            data: {
                uuid: Item.uuid
            }
        }).then(function mySucces(resp) {
            if (resp.data.result) {
                $scope.ShowList();
                messageService.publish('refreshTree', null);
            }
            else {
                alert("Delete Failed!");
            }
        }, function myError(response) {
            alert("Communication Error!");
        });
    }
    $scope.newVMItem = function () {
        $http({
            method: "POST",
            url: "/newVMItem",

        }).then(function mySucces(resp) {
            if (resp.data.result) {
                $scope.ShowList();
                messageService.publish('refreshTree', null);
            }
            else {
                alert("add Failed!");
            }
        }, function myError(response) {
            alert("Communication Error!");
        });
    }

    $scope.MoveTo = function () {
        $('#MoveToModal').modal();
    }

    $scope.confirmMoveTo = function () {
        if ($scope.MoveToUserName == "") {
            $scope.MoveTo.isvilidate = true;
            $scope.MoveTo.ErrorMsg = "The user name can't be empty.";
            return;
        }

        var loader = {
            method: 'POST',
            url: '/moveTo',
            data: {
                uuid: $scope.selected.uuid,
                owner: $scope.MoveToUserName,
            }
        };

        $http(loader).success(function (resp) {
            if (!resp.result) {
                $scope.MoveTo.isvilidate = true;
                $scope.MoveTo.ErrorMsg = resp.error;
                return;
            } else {
                $('#MoveToModal').modal('hide');
                $scope.Back();
            }
        });
    }

    // navigation bar message handling
    messageService.subscribe('NavBarClick', function (event, parameters) {
        switch (parameters)
        {
            case $scope.language.New:
                $scope.createNew();
                break;
            case $scope.language.Connect:
                break;
            case $scope.language.MoveTo:
                $scope.MoveTo();
                break;
            case $scope.language.Delete:
                $scope.DeleteVMItem($scope.selected);
                break;
            default:
                break;
        }
    });
    // abn tree click message handling
    messageService.subscribe('user_clicks_branch', function (event, parameters) {
        switch (parameters) {
            case 'Virtual Machines':
                $scope.ShowList();
                break;
            case 'SQL Databases':
                break;
            default:
                for (var i = 0; i < $scope.MyVDSList.length; i++)
                {
                    if ($scope.MyVDSList[i].name == parameters)
                        $scope.showDetail($scope.MyVDSList[i]);
                }
                break;
        }
        
    });
}]).controller('ManageCtr', function ($scope, $http) {

}).controller('AbnTestController', function ($scope, $timeout, $http, $location, messageService) {
    $scope.language = new LanguageUtility();
    $scope.loadUserVNList = function () {
        var loader = {
            method: 'GET',
            url: '/GetVMList'
        };

        $http(loader).success(function (resp) {
            if (resp.result) {
                $scope.MyVDSList = resp.data;
                b = $scope.my_tree.get_first_branch();
                $scope.my_tree.delete_branch_children(b);
                for (var i = 0; i < $scope.MyVDSList.length; i++) {
                    $scope.my_tree.add_branch(b, {
                        label: $scope.MyVDSList[i].name,
                        data: {
                        },
                    });

                }
            } else {
                window.location.href = 'index.html';
            }
        });
    }
    $scope.MyVDSList = [];
    
    var apple_selected, tree, treedata_avm, treedata_geography;
    $scope.my_tree_handler = function (branch) {
        messageService.publish('user_clicks_branch', branch.label);
    };
    apple_selected = function (branch) {
        return $scope.output = "APPLE! : " + branch.label;
    };
    treedata_avm = [
      {
          label: $scope.language.VirtualMachines,
          children: [
          ],

      }, {
          label: $scope.language.SQLDatabases,
          data: {
              definition: "This new feature will be added in the upcoming release.",
              data_can_contain_anything: true
          },
          onSelect: function (branch) {
              return $scope.output = "SQL Databases: " + branch.data.definition;
          },
          children: [
            {
                label: 'MyDB1'
            }
          ]
      }, 
    ];
    treedata_geography = [
      {
          label: 'North America',
          children: [
            {
                label: 'Canada',
                children: ['Toronto', 'Vancouver']
            }, {
                label: 'USA',
                children: ['New York', 'Los Angeles']
            }, {
                label: 'Mexico',
                children: ['Mexico City', 'Guadalajara']
            }
          ]
      }, {
          label: 'South America',
          children: [
            {
                label: 'Venezuela',
                children: ['Caracas', 'Maracaibo']
            }, {
                label: 'Brazil',
                children: ['Sao Paulo', 'Rio de Janeiro']
            }, {
                label: 'Argentina',
                children: ['Buenos Aires', 'Cordoba']
            }
          ]
      }
    ];
    $scope.my_data = treedata_avm;
    $scope.try_changing_the_tree_data = function () {
        if ($scope.my_data === treedata_avm) {
            return $scope.my_data = treedata_geography;
        } else {
            return $scope.my_data = treedata_avm;
        }
    };
    $scope.my_tree = tree = {};
    $scope.try_async_load = function () {
        $scope.my_data = [];
        $scope.doing_async = true;
        return $timeout(function () {
            if (Math.random() < 0.5) {
                $scope.my_data = treedata_avm;
            } else {
                $scope.my_data = treedata_geography;
            }
            $scope.doing_async = false;
            return tree.expand_all();
        }, 1000);
    };
    $scope.loadUserVNList();
    // li click message handling
    messageService.subscribe('changeStatus', function (event, parameters) {
        temptree = $scope.my_tree.get_first_branch();
        
        do {
            if (temptree.label == parameters) {
                $scope.my_tree.select_branch(temptree);
                break;
            }
            temptree = $scope.my_tree.get_next_branch(temptree);
        } while (tree != null)

    });
    messageService.subscribe('refreshTree', function (event, parameters) {
        $scope.loadUserVNList();
    });
    /*return $scope.try_adding_a_branch = function () {
        var b;
        b = tree.get_selected_branch();
        return tree.add_branch(b, {
            label: 'New Branch',
            data: {
                something: 42,
                "else": 43
            }
        });
    };
    $scope.user_clicks_branch = function (branch) {
        messageService.publish('user_clicks_branch', branch.label);
    }*/
    
});

