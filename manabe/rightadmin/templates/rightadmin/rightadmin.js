   // zTree 的参数配置，深入使用请参考 API 文档（setting 配置详解）
   var setting = {

   };
   // zTree 的数据属性，深入使用请参考 API 文档（zTreeNode 节点数据详解）
   var zNodes = [
        {name: "应用名称：{{ app.name }}", open:true, children: [
            {%for single_action in action %}
                {% ifnotequal single_action.name 'DEPLOY'%}
                    {name: "{{single_action.description}}",
                    url:"{% url 'rightadmin:admin_user' app_id=app.id action_id=single_action.id env_id=0 %}",
                    target:"myFrame"},
                {% endifnotequal %}
                {% ifequal single_action.name 'DEPLOY'%}
                    {name: "{{single_action.description}}", open:true, children: [
                        {%for single_env in env %}
                        {name: "{{ single_env }}环境",
                        url:"{% url 'rightadmin:admin_user' app_id=app.id action_id=single_action.id env_id=single_env.id %} ",
                        target:"myFrame"},
                        {% endfor %}
                    ]},
                {% endifequal %}
            {% endfor %}
        ]}
    ];
   $(document).ready(function(){
     //页面加载成功后,开始加载树形结构
   $.fn.zTree.init($("#treeDemo"), setting, zNodes);
   });
