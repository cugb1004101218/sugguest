
   $(document).ready(function(){
      opinionTable();
   });
 

    function opinionTable() {

    	var columns = [
	            { 
	            	title: "姓名",
	            	width:'24%',
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
			
			var params = parseQuery(window.location.search.substring(1));

			if (typeof data.problem.problem == 'string') {
				var titleText = data.problem.problem;
				if(params.hasOwnProperty('index')){
					$('title').html(titleText);
				} else if(params.hasOwnProperty('query')){
					$('title').html(params.query + ' 代表/委员向最高检建了什么言?');
				} else {

					$('title').html('1267名代表委员建言检察工作' + numStrMap[params.father]);
				}
				if(titleText.indexOf("（") != -1){
					titleText = titleText.substring(0,titleText.indexOf("（"))+"<br><span class = 'h-smaller'>"+titleText.substring(titleText.indexOf("（"))+"</span>";
				}
				$('.container-fluid').prepend('<h4 align="center">'+titleText+'</h4>');
			}
			
			/*if (typeof data.problem.problem == 'string') {
				var titleText = data.problem.problem;
				$('title').html(titleText);
				if(titleText.indexOf("（") != -1){
					titleText = titleText.substring(0,titleText.indexOf("（"))+"<br><span class = 'h-smaller'>"+titleText.substring(titleText.indexOf("（"))+"</span>";
				}
				$('.container-fluid').prepend('<h4 align="center">'+titleText+'</h4>');
			}*/

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

    var parseQuery = function(query){
        var reg = /([^=&\s]+)[=\s]*([^=&\s]*)/g;
        var obj = {};
        while(reg.exec(query)){
	    obj[RegExp.$1] = RegExp.$2;
        }
        return obj;
    }

    var numStrMap = {1:'(一)',2:'(二)',3:'(三)',4:'(四)',5:'(五)',6:'(六)',7:'(七)',8:'(八)',9:'(九)',10:'(十)',11:'(十一)',12:'(十二)'};
	   
