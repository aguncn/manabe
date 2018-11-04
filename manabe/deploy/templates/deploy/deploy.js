function getParallelOptions(sp_select_id){
    if (sp_select_id == "parallel_deploy" && $("#p_select_id").length <= 0) {
        html_str = '<select name="p_value"  id="p_select_id"  class="select"> \
                    +      <option selected value="1">1</option> \
                    +      <option value="2">2</option> \
                    +      <option value="3">3</option> \
                    +      <option value="4">4</option> \
                    +      <option value="5">5</option> \
                    +  </select>'
        $("#sp_select").after(html_str);
    }
    if (sp_select_id == "serial_deploy" && $("#p_select_id").length > 0) {
        $("#p_select_id").remove();
    }
}

$("#close_deploylogout").click(function(){
    $('#deploylogout').hide();
    window.location.reload();
});

$("#btn-deploy").click(function(evt){
    evt.preventDefault(); //阻止表单提交，只获取表单内数据
    var group_data = $("#serverForm").serialize();
    var _self = this;
    console.log(group_data);

    if (group_data.indexOf("serverSelect") == -1){
        $.Huimodalalert('<span  class="c-error">请确认所有选项正确！</span>',3000);
        return false;
    }

    $.ajax({
        url:'{% url "deploy:deploy-cmd" %}',
        type: 'post',
        data:{
            group_cmd: group_data,
        },
        dataType: 'json',
        beforeSend: function(){
            $('#btn-deploy').hide();
            deploy_version = $("#id_deploy_version").attr("deploy_version");
            app_name = $("#id_app_name").attr("app_name");
            mablog_url = $("#id_deploy_no").attr("mablog_url");
            deploy_no = parseInt($("#id_deploy_no").attr("deploy_no")) + 1;
            url = mablog_url + "/wslog/log_show/?app_name=" + app_name + "&deploy_version=" +  deploy_version + "&operation_no=" +  deploy_no +"&env_name=Demo"
            console.log(url);
            $('#iframe_log').attr('src', url);
            $('#deploylogout').show();
            console.log(group_data);
        },
        success: function(json){
            console.log(json);
        },
        error: function(){
        },
        complete: function(){
        }
    });
});

$("#btn-operate").click(function(evt){
    evt.preventDefault(); //阻止表单提交，只获取表单内数据
    var group_data = $("#serverForm").serialize();
    var _self = this;
    console.log(group_data);

    if (group_data.indexOf("serverSelect") == -1){
        $.Huimodalalert('<span  class="c-error">请确认所有选项正确！</span>',3000);
        return false;
    }

    $.ajax({
        url:'{% url "deploy:deploy-cmd" %}',
        type: 'post',
        data:{
            group_cmd: group_data,
        },
        dataType: 'json',
        beforeSend: function(){
            $('#btn-deploy').hide();
            env_name = $("#id_env").attr("env");
            app_name = $("#id_app_name").attr("app_name");
            mablog_url = $("#id_op_log_no").attr("mablog_url")
            op_log_no = parseInt($("#id_op_log_no").attr("op_log_no")) + 1;
            url = mablog_url + "/wslog/log_show/?app_name=" + app_name + "&deploy_version=Demo&operation_no=" +  op_log_no +"&env_name=" + env_name
            console.log(url);
            $('#iframe_log').attr('src', url);
            $('#deploylogout').show();
            console.log(group_data);
        },
        success: function(json){
            console.log(json);
        },
        error: function(){
        },
        complete: function(){
        }
    });
});