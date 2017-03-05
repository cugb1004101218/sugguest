
   $(document).ready(function(){
      opinionTable();
   });
 

    function opinionTable() {

    	var columns = [
	            { 
	            	title: "姓名",
	            	width:'22.5%',
	            	data: '[]',
	           		render:function ( data, type, full, meta ) {
	            		var text = data[0] + '<br>' +data[1] ;
      					return text;
    				}
    			},
	            { 
	            	title: "职务",
	            	width:'22.5%',
	            	data: [2]
	            },
	            { 
	            	title: "意见建议内容",
	            	data:[3] 
	            },
	            
	        ];
    	$.ajax({
		type : 'get',
		url : 'http://table.jcrb.com:8000/problem'+window.location.search,
		dataType : 'json',
		// data : {father:father,index:index},
		error : function() {

		},
		success : function(data, status, xhr) {
			if (typeof data.problem.problem == 'string') {
				var titleText = data.problem.problem;
				if(titleText.indexOf("（") != -1){
					titleText = titleText.substring(0,titleText.indexOf("（"))+"<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"+titleText.substring(titleText.indexOf("（"));
				}
				$('.container-fluid').prepend('<h1 align="center">'+titleText+'</h1>');
				$('title').html(titleText);
			}

			var table = $('#opinionTable').DataTable({
				ordering: false,
				searching: true,
				info: false,
				paging:false,
				lengthChange:false,
				data: data.suggest_list,
				columns: columns
			});

			$('#opinionTable_filter').find('label').contents().filter(function(){
					return this.nodeType == 3; }).remove();
			$('#opinionTable_filter').find('input').attr('class','form-control');
			$('#opinionTable_filter').find('input').attr('placeholder','输入姓名或关键字进行搜索');
			return table;
		}
	});
    }
	   
