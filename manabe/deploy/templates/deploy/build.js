$(".buildBtn").click(function(e){
    $("#modal_app_name").html($(this).attr('app_name'));
    $("#modal_deploy_version").html($(this).attr('deploy_version'));
    var jenkins_job_console = '{{jenkins_url}}' + $(this).attr('jenkins_job') + '/lastBuild/console '
    $("#modal_jenkins_job").html($(this).attr('jenkins_job'));
    $("#modal_jenkins_url").html(jenkins_job_console);
     $("#modal-demo").modal("show");
});

function modal_close(){
	$("#modal-demo").modal("hide");
	location.reload();
}

$(".checkBtn").click(function(e){
    var app_name = $(this).attr('app_name');
    var deploy_version = $(this).attr('deploy_version');
    var check_url = '{{nginx_url}}/' + app_name + '/' + deploy_version + '/';
    openFullScreen(check_url)

});

function openFullScreen (url) {
    var name = arguments[1] ? arguments[1] : "_blank";
    var feature = "fullscreen=no,channelmode=no, titlebar=no, toolbar=no, scrollbars=no," +
         "resizable=yes, status=no, copyhistory=no, location=no, menubar=no,width=1000 " +
         "height=400, top=0, left=200";
    var newWin = window.open(url, name, feature);
}
$(".btn_gen_pkg").click(function(){
    var deploy_version = $("#modal_deploy_version").text();
    var app_name = $("#modal_app_name").text();
    var jenkins_job = $("#modal_jenkins_job").text();

    //使用 jquery的promise技术来实现前端和后端之间异步的顺序调用
    //第一步，将任务发送到jenkins
    var promiseJenkinsA = $.ajax({
        url:'{% url 'deploy:jenkins_build' %}',
        type: 'post',
        data:{
            deploy_version: deploy_version,
            jenkins_job: jenkins_job,
            app_name:app_name
        },
        dataType: 'json',
        beforeSend: function(){
            $(".btn_gen_pkg").attr("disabled","disabled");
             $(".btn_gen_pkg").hide();
            $("#build_progress").html("亲，正在编译，请耐心等候...<i class='fa fa-spinner fa-pulse fa-3x'></i>");
        },
         error: function (jqXHR, textStatus, errorThrown) {
            $("#build_progress").html("系统问题,请联系开发同事");
        },
        success: function(data){
            console.log(data);
        }
    });

    //第二步，获取jenkins job的任务状态，成功之后，更新状态和发布单
    var promiseJenkinsB = promiseJenkinsA.then(function(data){
        build_number = data['build_number']
        function showStatus() {
            $.ajax({
                url:'{% url 'deploy:jenkins_status' %}',
                type: 'post',
                data:{
                    jenkins_job: jenkins_job,
                    next_build_number: build_number
                },
                dataType: 'json',
                error: function (jqXHR, textStatus, errorThrown) {
                    $("#build_progress").html("系统问题,请联系开发同事!<i class='fa fa-ban fa-3x'></i>");
                },
                success: function(data){
                    //当编译成功，或失败之后，清除定时器, 成功了就使用ajax post更新发布单状态。
                    if (data['built_result'] == 'SUCCESS') {
                        clearInterval(intervalKey);
                        console.log(data['git_version'] + "update")
                        $.post(
                            "{% url 'deploy:update_deploypool_jenkins' %}",
                            {
                                git_version: data['git_version'],
                                deploy_version: deploy_version,
                                next_build_number: build_number,
                                app_name:app_name
                            },
                            function(data) {
                                if (data['return'] == 'success') {
                                    $("#build_progress").html(
                                    "<span class='label label-success radius'>完成编译, 编译次数："
                                    + data['build_number'] + "</span><i class='fa fa-check fa-3x'></i>");
                                } else {
                                    $("#build_progress").html(
                                    "<span class='label label-error radius'>编译成功, 更新发布单错误, 编译次数："
                                    + data['build_number'] + "</span><i class='fa fa-ban fa-3x'></i>");
                                }
                            }
                        );
                    }
                    if (data['built_result'] == 'FAILURE') {
                        clearInterval(intervalKey);
                        $("#build_progress").html(
                        "<span class='label label-error radius'>编译出错, 编译次数："
                        + json['build_number'] + "</span><i class='fa fa-ban fa-3x'></i>");
                    }
                }
            });
        }
        //第隔二秒，获取jenkins的编译进度
        intervalKey = setInterval(showStatus, 2000);
    });

});