$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "{% url 'public:get-env' %}",
        dataType : "json",
        success: function(data) {
            console.log(data);
            $.each(data, function(index,value){
                $('#envSelect').append('<option value="' + index + '">' + value + '</option>');
            });
        },
        error : function(){
            alert("系统出现问题");
        }
    });
});


    $("#envChange").confirm({

        title: '确认!',
        content: function () {
            return "将选中的发布单切换到" + $("#envSelect").find("option:selected").text() + "环境?"
        },
        buttons: {
            confirm: function () {
                $("#envForm").submit();
            },
            cancel: function () {
            },
        }
    });

