$(document).ready(function() {
    //指定PRD环境获取发布单数据
    $.ajax({
        type: "GET",
        url: "{% url 'deploy:get_deploy_count' %}?env=PRD",
        dataType : "json",
        success: function(data) {
            var xArray = []
            var yArray = []
            for (var item in data) {
                for (var i in data[item]) {
                    console.log(i, data[item][i])
                    xArray.push(i);
                    yArray.push(data[item][i]);
                }
            }
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('main_prd'));

            // 指定图表的配置项和数据
            var option = {
                title: {
                    //text: '30天'
                },
                grid:{
                    left:25,
                    top:20,
                    right:0,
                    bottom:25
                },
                tooltip: {},
                legend: {
                    data:['记录']
                },
                xAxis: {
                    data: xArray
                },
                yAxis: {},
                series: [{
                    name: '发布单',
                    type: 'line',
                    data: yArray
                }]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },
        error : function(){
            alert("系统出现问题");
        }
    });

    //指定TEST环境获取发布单数据
    $.ajax({
        type: "GET",
        url: "{% url 'deploy:get_deploy_count' %}?env=TEST",
        dataType : "json",
        success: function(data) {
            var xArray = []
            var yArray = []
            for (var item in data) {
                for (var i in data[item]) {
                    console.log(i, data[item][i])
                    xArray.push(i);
                    yArray.push(data[item][i]);
                }
            }
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('main_test'));

            // 指定图表的配置项和数据
            var option = {
                title: {
                    //text: '30天'
                },
                grid:{
                    left:25,
                    top:20,
                    right:0,
                    bottom:25
                },
                tooltip: {},
                legend: {
                    data:['记录']
                },
                xAxis: {
                    data: xArray
                },
                yAxis: {},
                series: [{
                    name: '发布单',
                    type: 'line',
                    data: yArray
                }]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },
        error : function(){
            alert("系统出现问题");
        }
    });

    //获取APP应用发布单数据
    $.ajax({
        type: "GET",
        url: "{% url 'deploy:get_app_deploy_count' %}",
        dataType : "json",
        success: function(data) {
            var xArray = []
            var yArray = []
            for (var item in data) {
                for (var i in data[item]) {
                    console.log(i, data[item][i])
                    xArray.push(i);
                    yArray.push(data[item][i]);
                }
            }
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('main_app'));

            // 指定图表的配置项和数据
            var option = {
                title: {
                    //text: '30天'
                },
                grid:{
                    left:25,
                    top:20,
                    right:0,
                    bottom:25
                },
                tooltip: {},
                legend: {
                    data:['记录']
                },
                xAxis: {
                    data: xArray
                },
                yAxis: {},
                series: [{
                    name: '发布单',
                    type: 'bar',
                    data: yArray
                }]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },
        error : function(){
            alert("系统出现问题");
        }
    });
});

