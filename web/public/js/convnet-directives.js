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

            function addjsonviewer(i){
                    snippet="<div><div id='mainView' ng-model='jsondata' ng-app='JSONedit' ng-init='jsondata=[{1:2},{3:4}]'>\
                        <div class='jsonView'>\
                            <json child='jsondata' default-collapsed='false' type='object'></json>\
                        </div>\
                    </div></div>"

                    return snippet

            }
            function test(){
                return "<div ng-model='mycustomdata'><p>{{mycustomdata.name}}</p></div>"
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
                                    <div class='row' id='"+handle.name+"'>\
                                    "+addjsonviewer(i)+"\
                                    </div>\
                                    </div>\
                                </div>\
                        </div>";
                layerdata=layerdata.replace(/&quot;/g, '"')
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
                var myEl = angular.element(document.querySelector( '#dummy' ));
                console.log("Hiiiii")
                console.log($compile(test())(scope))
                myEl.replaceWith($compile(addjsonviewer(0))(scope))
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
