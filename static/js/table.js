
   $(document).ready(function(){
      opinionTable();
   });
 

    function opinionTable() {
        var father = GetQueryString("father");
        var index = GetQueryString("index");
        var columns = [
                { title: "姓名",width:'22.5%' },
                { title: "职务"},
                { title: "意见建议内容" },
                
            ];
        $.ajax({
            type : 'get',
            url : 'http://115.28.145.36:2000/problem',
            dataType : 'json',
            data : {father:father,index:index},
            error : function() {

            },
            success : function(data, status, xhr) {
                // xhr.setHeader("Access-Control-Allow-Origin", "*");
                var titleText = data.problem.problem;
                titleText = titleText.substring(0,titleText.indexOf("（"))+"<br>"+titleText.substring(titleText.indexOf("（"));
                $('.container-fluid').prepend('<h4 align="center">'+titleText+'</h4>');
                var temp = data.suggest_list;
                for(var ob in temp){

                }
                console.log(data);
                var table = $('#opinionTable').DataTable({
                        searching: true,
                        info: false,
                        paging:false,
                        lengthChange:false,
                        columns: columns,
                        data: data.suggest_list
                    });
                $('#opinionTable_filter').find('label').contents().filter(function(){ 
                         return this.nodeType == 3; }).remove(); $('#opinionTable_filter').find('input').attr('class','form-control');
                $('#opinionTable_filter').find('input').attr('placeholder','输入姓名或关键字进行搜索');
                return table;
            }
        });
    }


function GetQueryString(name){
      var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
      var r = window.location.search.substr(1).match(reg);
      if(r!=null)return  decodeURI(r[2]); return null;
 }

       
