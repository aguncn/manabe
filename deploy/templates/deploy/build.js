$(".buildBtn").click(function(e){
    $("#modal_app_name").html($(this).attr('app_name'));
    $("#modal_deploy_version").html($(this).attr('deploy_version'));
    var jenkins_job_console = '{{jenkins_url}}' + $(this).attr('jenkins_job') + '/lastBuild/console '
    $("#modal_jenkins_job").html("<a href=" + jenkins_job_console + " target='_blank'>" + $(this).attr('jenkins_job')+ "</a>");
     $("#modal-demo").modal("show");
});

$(".checkBtn").click(function(e){
    var app_name = $(this).attr('app_name');
    var deploy_version = $(this).attr('deploy_version');
    var check_url = '{{jenkins_url}}' + app_name + '/' + deploy_version + '/';
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
    var deploy_version = $(this).closest('#gen_pkg_id').attr('deploy_version');
    var loopcount = $(this).closest('#gen_pkg_id').attr('loopcount');
    var jenkins_url = $(this).attr('jenkins_url');
    var _self = this;

    promiseJenkins = $.ajax({
        url:'{% url 'deploy:jenkins_build' %}',
        type: 'post',
        data:{
            deploy_version: deploy_version,
        },
        dataType: 'json',
        beforeSend: function(){
        },
         error: function (jqXHR, textStatus, errorThrown) {
        },
        success: function(json){
        }
    });

});