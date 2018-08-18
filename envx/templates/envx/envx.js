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
    {% for msg in messages %}
        $.Huimodalalert('<span {% if msg.tags %} class="{{ msg.tags }}"{% endif %}>{{ msg.message }}</span>',3000);
    {% endfor %}

    $("#envChange").click(function(e){
        e.preventDefault();
        $("#selectEnv").html($("#envSelect").find("option:selected").text());
         $("#modal-demo").modal("show");
    });

    $("#changeEnvModal").click(function(){
         $("#envForm").submit();
    });
});


