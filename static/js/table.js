
   $(document).ready(function(){
      opinionTable();
   });
 

    function opinionTable() {

    	var columns = [
	            { title: "姓名",width:'22.3%' },
	            { title: "代表团/界别",width:'22.3%'},
	            { title: "职务",width:'22.3%'},
	            { title: "意见建议内容" },
	            
	        ];
    	$.ajax({
			type : 'get',
			url : 'http://table.jcrb.com:8000/problem'+window.location.search,
			dataType : 'json',
			// data : {father:father,index:index},
			error : function() {

			},
			success : function(data, status, xhr) {debugger
				// xhr.setHeader("Access-Control-Allow-Origin", "*");
				if(typeof data.problem.problem == 'object'){
                     var titleText = data.problem.problem.problem;
                     $('.container-fluid').prepend('<h4 align="center">关键词：'+titleText+'</h4>');
                                                                            
                 } else if (typeof data.problem.problem == 'string') {
                     var titleText = data.problem.problem;
                    // titleText = titleText.substring(0,titleText.indexOf("（"))+"<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"+titleText.substring(titleText.indexOf("（"));
                      $('.container-fluid').prepend('<h4 align="center">'+titleText+'</h4>');
                }
                var temp = data.suggest_list;
				console.log(data);
				var table = $('#opinionTable').DataTable({
                        ordering: false,
		    			searching: true,
		    			info: false,
		    			paging:false,
		    			lengthChange:false,
		    			columns: columns,
		    			data: data.suggest_list
		    		});

				$('#opinionTable_filter').find('label').contents().filter(function(){
                         return this.nodeType == 3; }).remove();
				$('#opinionTable_filter').find('input').attr('class','form-control');
				$('#opinionTable_filter').find('input').attr('placeholder','输入姓名或关键字进行搜索');
				return table;
			}
		});
    }
	   
