   var app = angular.module('JSONedit');

    app.factory('socket', ['$rootScope', function($rootScope) {
        var socket = io.connect();

        return {
            on: function(eventName, callback) {
                socket.on(eventName, callback);
            },
            emit: function(eventName, data) {
                socket.emit(eventName, data);
            }
        };
    }]);


    app.directive('dagreChart', function($compile) {
        function funclink(scope, element, attrs) {
            var stringName = "Text";
            var objectName = "Object";
            var arrayName = "Array";
            var refName = "Reference";
            var boolName = "Boolean";
            var numberName = "Number";

            scope.valueTypes = [stringName, objectName, arrayName, refName, boolName, numberName];
            scope.sortableOptions = {
                axis: 'y'
            };
            if (scope.$parent.defaultCollapsed === undefined) {
                scope.collapsed = false;
            } else {
                scope.collapsed = scope.defaultCollapsed;
            }
            if (scope.collapsed) {
                scope.chevron = "glyphicon-chevron-right";
            } else {
                scope.chevron = "glyphicon-chevron-down";
            }
            

            //////
            // Helper functions
            //////

            var getType = function(obj) {
                var type = Object.prototype.toString.call(obj);
                if (type === "[object Object]") {
                    return "Object";
                } else if(type === "[object Array]"){
                    return "Array";
                } else if(type === "[object Boolean]"){
                    return "Boolean";
                } else if(type === "[object Number]"){
                    return "Number";
                } else {
                    return "Literal";
                }
            };
            var isNumber = function(n) {
              return !isNaN(parseFloat(n)) && isFinite(n);
            };
            scope.getType = function(obj) {
                return getType(obj);
            };
            scope.toggleCollapse = function() {
                if (scope.collapsed) {
                    scope.collapsed = false;
                    scope.chevron = "glyphicon-chevron-down";
                } else {
                    scope.collapsed = true;
                    scope.chevron = "glyphicon-chevron-right";
                }
            };
            scope.moveKey = function(obj, key, newkey) {
                //moves key to newkey in obj
                if (key !== newkey) {
                    obj[newkey] = obj[key];
                    delete obj[key];
                }
            };
            scope.deleteKey = function(obj, key) {
                if (getType(obj) == "Object") {
                    if( confirm('Delete "'+key+'" and all it contains?') ) {
                        delete obj[key];
                    }
                } else if (getType(obj) == "Array") {
                    if( confirm('Delete "'+obj[key]+'"?') ) {
                        obj.splice(key, 1);
                    }
                } else {
                    console.error("object to delete from was " + obj);
                }
            };
            scope.addItem = function(obj) {
                if (getType(obj) == "Object") {
                    // check input for key
                    if (scope.keyName == undefined || scope.keyName.length == 0){
                        alert("Please fill in a name");
                    } else if (scope.keyName.indexOf("$") == 0){
                        alert("The name may not start with $ (the dollar sign)");
                    } else if (scope.keyName.indexOf("_") == 0){
                        alert("The name may not start with _ (the underscore)");
                    } else {
                        if (obj[scope.keyName]) {
                            if( !confirm('An item with the name "'+scope.keyName
                                +'" exists already. Do you really want to replace it?') ) {
                                return;
                            }
                        }
                        if (scope.valueType == numberName && !isNumber(scope.valueName)){
                            alert("Please fill in a number");
                            return;
                        }
                        // add item to object
                        switch(scope.valueType) {
                            case stringName: obj[scope.keyName] = scope.valueName ? scope.valueName : "";
                                            break;
                            case numberName: obj[scope.keyName] = scope.possibleNumber(scope.valueName);
                                             break;
                            case objectName:  obj[scope.keyName] = {};
                                            break;
                            case arrayName:   obj[scope.keyName] = [];
                                            break;
                            case refName: obj[scope.keyName] = {"Reference!!!!": "todo"};
                                            break;
                            case boolName: obj[scope.keyName] = false;
                                            break;
                        }
                        //clean-up
                        scope.keyName = "";
                        scope.valueName = "";
                        scope.showAddKey = false;
                    }
                } else if (getType(obj) == "Array") {
                    if (scope.valueType == numberName && !isNumber(scope.valueName)){
                        alert("Please fill in a number");
                        return;
                    }
                    // add item to array
                    switch(scope.valueType) {
                        case stringName: obj.push(scope.valueName ? scope.valueName : "");
                                        break;
                        case numberName: obj.push(scope.possibleNumber(scope.valueName));
                                         break;
                        case objectName:  obj.push({});
                                        break;
                        case arrayName:   obj.push([]);
                                        break;
                        case boolName:   obj.push(false);
                                        break;
                        case refName: obj.push({"Reference!!!!": "todo"});
                                        break;
                    }
                    scope.valueName = "";
                    scope.showAddKey = false;
                } else {
                    console.error("object to add to was " + obj);
                }
            };
            scope.possibleNumber = function(val) {
                return isNumber(val) ? parseFloat(val) : val;
            };


            // Rest Ends
            function jsondisplay(handle,i){
                var stringName = "Text";
                var objectName = "Object";
                var arrayName = "Array";
                var refName = "Reference";
                var boolName = "Boolean";
                var numberName = "Number";

                var switchTemplate = 
                    '<span ng-switch on="getType(val)" >'
                        + '<json ng-switch-when="Object" child="val" type="object" default-collapsed="defaultCollapsed"></json>'
                        + '<json ng-switch-when="Array" child="val" type="array" default-collapsed="defaultCollapsed"></json>'
                        + '<span ng-switch-when="Boolean" type="boolean">'
                            + '<input type="checkbox" ng-model="val" ng-model-onblur ng-change="child[key] = val">'
                        + '</span>'
                        + '<span ng-switch-when="Number" type="number"><input type="text" ng-model="val" '
                            + 'placeholder="0" ng-model-onblur ng-change="child[key] = possibleNumber(val)"/>'
                        + '</span>'
                        + '<span ng-switch-default class="jsonLiteral"><input type="text" ng-model="val" '
                            + 'placeholder="Empty" ng-model-onblur ng-change="child[key] = val"/>'
                        + '</span>'
                    + '</span>';

                var addItemTemplate = 
                '<div ng-switch on="showAddKey" class="block" >'
                    + '<span ng-switch-when="true">';
                        if (scope.type == "object"){
                           // input key
                            addItemTemplate += '<input placeholder="Name" type="text" ui-keyup="{\'enter\':\'addItem(child)\'}" '
                                + 'class="form-control input-sm addItemKeyInput" ng-model="$parent.keyName" /> ';
                        }
                        addItemTemplate += 
                        // value type dropdown
                        '<select ng-model="$parent.valueType" ng-options="option for option in valueTypes" class="form-control input-sm"'
                            + 'ng-init="$parent.valueType=\''+stringName+'\'" ui-keydown="{\'enter\':\'addItem(child)\'}"></select>'
                        // input value
                        + '<span ng-show="$parent.valueType == \''+stringName+'\'"> : <input type="text" placeholder="Value" '
                            + 'class="form-control input-sm addItemValueInput" ng-model="$parent.valueName" ui-keyup="{\'enter\':\'addItem(child)\'}"/></span> '
                        + '<span ng-show="$parent.valueType == \''+numberName+'\'"> : <input type="text" placeholder="Value" '
                            + 'class="form-control input-sm addItemValueInput" ng-model="$parent.valueName" ui-keyup="{\'enter\':\'addItem(child)\'}"/></span> '
                        // Add button
                        + '<button type="button" class="btn btn-primary btn-sm" ng-click="addItem(child)">Add</button> '
                        + '<button type="button" class="btn btn-default btn-sm" ng-click="$parent.showAddKey=false">Cancel</button>'
                    + '</span>'
                    + '<span ng-switch-default>'
                        // plus button
                        + '<button type="button" class="addObjectItemBtn" ng-click="$parent.showAddKey = true"><i class="glyphicon glyphicon-plus"></i></button>'
                    + '</span>'
                + '</div>';


                var template = '<i ng-click="toggleCollapse()" class="glyphicon" ng-class="chevron"></i>'
                    + '<span class="jsonItemDesc">'+objectName+'</span>'
                    + '<div class="jsonContents" ng-hide="collapsed">'
                        // repeat
                        + '<span class="block" ng-hide="key.indexOf(\'_\') == 0" ng-repeat="(key, val) in mycustomdata.layer['+i+']">'
                            // object key
                            + '<span class="jsonObjectKey">'
                                + '<input class="keyinput" type="text" ng-model="newkey" ng-init="newkey=key" '
                                    + 'ng-blur="moveKey(mycustomdata.layer['+i+'], key, newkey)"/>'
                                // delete button
                                + '<i class="deleteKeyBtn glyphicon glyphicon-trash" ng-click="deleteKey(mycustomdata.layer['+i+'], key)"></i>'
                            + '</span>'
                            // object value
                            + '<span class="jsonObjectValue">' + switchTemplate + '</span>'
                        + '</span>'
                        // repeat end
                        + addItemTemplate
                    + '</div>';
                return template

            }


            function processLayer(handle,i){
                console.log(handle.name+" %%%% "+handle.window )
                console.log(handle.window)
                collapse=""
                title="_open"
                if(String(handle.window)=="close"){
                    console.log(handle.name+" %%%% INSIDE "+handle.window )
                    collapse=" collapse";
                    title="_close"
                }
                layerdata="<div class='panel panel-default'> \
                         <div class='panel-heading' role='tab' id='headingOne'>\
                            <h4 class='panel-title'> \
                            <button ng-click=&quot;myfunc('"+handle.name+"')&quot;>hii"+title+"</button>\
                            <a role='button' click='myfunc("+handle.name+")'> \
                            "+handle.name+title+"\
                            </a>\
                          <i class='fa fa-plus'></i>\
                            </h4>\
                         </div>\
                             <div id='collapseOne' class='panel-collapse"+collapse+"' role='tabpanel' aria-labelledby='headingOne'>\
                                <div class='panel-body'>\
                                <div id='mainView' ng-controller='MainViewCtrl'>\
                                    <div class='jsonView'>\
                                            <json child='mycustomdata.layer[0]'  default-collapsed='false' type='object'></json>\
                                        </div>\
                                    </div>\
                                </div>\
                            </div>\
                      </div>";
                layerdata=layerdata.replace(/&quot;/g, '"')
                console.log(layerdata)
                return layerdata

            }

            function updategraph(data_updated) {
                // Create the input graph
                d3.select(element[0]).select('svg').remove();
                var svg = d3.select(element[0])
                    .append('svg')
                    .attr("id", "svg-canvas")
                    .attr("width", 700)
                    .attr("height", 2000)
                svgGroup = svg.append("g");

                var g = new dagreD3.graphlib.Graph()
                    .setGraph({})
                    .setDefaultEdgeLabel(function() {
                        return {};
                        });

            
                node_dict = JSON.parse('{}')
                for (i = 0; i < data_updated.layer.length; i++) {
                    node_dict[data_updated.layer[i].name] = i
                    status = "unkown"
                    if ('status' in data_updated.layer[i]) {
                        status = data_updated.layer[i].status.toLowerCase()
                    }
                    processedLabel=processLayer(data_updated.layer[i],i)
                    g.setNode(i, {
                        label: processedLabel,
                        class: status,
                        labelType : 'html',
                        style: "font-family: 'Tangerine', serif;"
                    })
                }
                console.log('here')
                console.log(g)  
                g.nodes().forEach(function(v) {
                    var node = g.node(v);
                    // Round the corners of the nodes
                    node.rx = node.ry = 5;
                });
                for (i = 0; i < data_updated.layer.length; i++) {
                    console.log(data_updated.layer[i].name+" "+data_updated.layer[i].window);
                    if('bottom' in data_updated.layer[i]){
                    for (j = 0; j < data_updated.layer[i].bottom.length; j++) {
                        console.log(data_updated.layer[i].bottom[j])
                        if (data_updated.layer[i].bottom[j] != "") {
                            g.setEdge(node_dict[data_updated.layer[i].bottom[j]],i);
                            console.log(node_dict[data_updated.layer[i].bottom[j]])
                        }
                    }
                    }
                }
                console.log(g)
                // Create the renderer
                var render = new dagreD3.render();
                // Run the renderer. This is what draws the final graph.
                render(svgGroup, g);
                // Center the graph
                var xCenterOffset = (svg.attr("width") - g.graph().width) / 2;
                svgGroup.attr("transform", "translate(" + xCenterOffset + ", 20)");
                svg.attr("height", g.graph().height + 40);
                for (i = 0; i < data_updated.layer.length; i++) {
                    if('bottom' in data_updated.layer[i]){
                        for (j = 0; j < data_updated.layer[i].bottom.length; j++) {
                            console.log(data_updated.layer[i].bottom[j])
                        }
                    }
                }
            }
            updategraph(scope.mycustomdata)   
            var e= $compile(element.contents())(scope);
            //element.replaceWith(e) 
           console.debug(scope)
            scope.$watch('mycustomdata', function(newValue, oldValue) {
                updategraph(scope.mycustomdata)
                var e= $compile(element.contents())(scope);
                //element.replaceWith(e) 
                //console.log("&&&&&&&&&&&&&&&&")
                //d3.select('.aa123').remove();
                //d3.select(".aa123").append(element.html())
            },true)

        }
        return {
            link: funclink,
            restrict: 'E',
            controller: 'myCtrl',
            bindToController: true,
            scope: {
                mycustomdata: '=',
                myfunc: '&'
            },
            replace: true

        };
    });

       $('.panel-collapse').on('show.bs.collapse', function () {
          $(this).parent('.panel').find('.fa-minus').show();
          $(this).parent('.panel').find('.fa-plus').hide();
        })
        $('.panel-collapse').on('hide.bs.collapse', function () {
          $(this).parent('.panel').find('.fa-minus').hide();
          $(this).parent('.panel').find('.fa-plus').show();

        })


    app.controller('myCtrl', function($scope, $http,$timeout,socket) {
        var rawdata = {"layer": [{"input_param": {"shape": [{"dim": [64, 1, 28, 28]}]}, "top": ["data"], "type": "Input", "name": "data"}, {"name": "conv1", "bottom": ["data"], "top": ["conv1"], "param": [{"lr_mult": 1.0}, {"lr_mult": 2.0}], "convolution_param": {"weight_filler": {"type": "xavier"}, "stride": [1], "bias_filler": {"type": "constant"}, "kernel_size": [5], "num_output": 20}, "type": "Convolution"}, {"pooling_param": {"stride": 2, "kernel_size": 2, "pool": 0}, "top": ["pool1"], "type": "Pooling", "name": "pool1", "bottom": ["conv1"]}, {"name": "conv2", "bottom": ["pool1"], "top": ["conv2"], "param": [{"lr_mult": 1.0}, {"lr_mult": 2.0}], "convolution_param": {"weight_filler": {"type": "xavier"}, "stride": [1], "bias_filler": {"type": "constant"}, "kernel_size": [5], "num_output": 50}, "type": "Convolution"}, {"pooling_param": {"stride": 2, "kernel_size": 2, "pool": 0}, "top": ["pool2"], "type": "Pooling", "name": "pool2", "bottom": ["conv2"]}, {"name": "ip1", "bottom": ["pool2"], "inner_product_param": {"weight_filler": {"type": "xavier"}, "bias_filler": {"type": "constant"}, "num_output": 500}, "top": ["ip1"], "param": [{"lr_mult": 1.0}, {"lr_mult": 2.0}], "type": "InnerProduct"}, {"top": ["ip1"], "type": "ReLU", "name": "relu1", "bottom": ["ip1"]}, {"name": "ip2", "bottom": ["ip1"], "inner_product_param": {"weight_filler": {"type": "xavier"}, "bias_filler": {"type": "constant"}, "num_output": 10}, "top": ["ip2"], "param": [{"lr_mult": 1.0}, {"lr_mult": 2.0}], "type": "InnerProduct"}, {"top": ["prob"], "type": "Softmax", "name": "prob", "bottom": ["ip2"]}], "name": "LeNet"}
        for (layeridx in rawdata.layer){
            rawdata.layer[layeridx].window="close";
        }
        $scope.mycustomdata=rawdata
        $scope.myfunc= function (layername){
            console.log('aaaaaaaaa')
            console.log($scope.mycustomdata)
            rawdata=$scope.mycustomdata
        for (layeridx in rawdata.layer){
            if(rawdata.layer[layeridx].name==layername){
                if(rawdata.layer[layeridx].window=="close"){
                    $scope.mycustomdata.layer[layeridx].window="open"
                }else{
                    $scope.mycustomdata.layer[layeridx].window="close"
                }
            }

        }

        }
        //$scope.myfunc("hello")
        /*
        socket.on('chat message', function(data) {
            //console.log(data)
            $scope.$apply(function() {
                $scope.mycustomdata = JSON.parse(data)
            });
        });

        $scope.mycustomdata = {
            "layer": []
        };
        $http.get("/data")
            .then(function(response) {
                $scope.mycustomdata = response.data;
            });

        $scope.increaseCounter = function() {
            //$scope.mycustomdata=JSON.parse('{}')
            $http.get("/data")
                .then(function(response) {
                    $scope.mycustomdata = response.data;
                });

        };
        $scope.$watch('mycustomdata', function(newValue, oldValue) {
            console.log('newvalue', newValue)
        })
        */

    })
