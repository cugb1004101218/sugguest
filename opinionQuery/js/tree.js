
   $(document).ready(function(){
      opinionTree();
   });

   function opinionTree() {debugger
   		var setting = {
    		edit: {
    			enable: false,
    		},
		    view: {
		    	showIcon: false,
			},
			callback: {
				// onClick: zTreeOnClick
			}
	    };	    
	    $.ajax({
			type : 'get',
			url : 'http://115.28.145.36:2000/index',
			dataType : 'json',
			// data : data,
			error : function() {

			},
			success : function(data, status, xhr) {debugger
				// xhr.setHeader("Access-Control-Allow-Origin", "*");
				console.log(data);
				var treeObj = $.fn.zTree.init($("#opinionTree"), setting, data.node);
			}
		});
   }