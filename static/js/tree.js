
   $(document).ready(function(){
     // opinionTree();
      brFun();
   });

   function opinionTree() {
   		var setting = {
    		edit: {
    			enable: false,
    		},
		    view: {
		    	showIcon: false,
		    	showLine: false,
		    	txtSelectedEnable: true,
		    	addDiyDom: addDiyDom
			},
			callback: {
				onClick: zTreeOnClick
			}
	    };	    
	    $.ajax({
			type : 'get',
			url : 'http://115.28.145.36:2000/index',
			dataType : 'json',
			// data : data,
			error : function() {

			},
			success : function(data, status, xhr) {
				// xhr.setHeader("Access-Control-Allow-Origin", "*");
				console.log(data);
				// for(var i in data.node){

				// }
				var treeObj = $.fn.zTree.init($("#opinionTree"), setting, data.node);
				
			}
		});
   }

	function zTreeOnClick(event, treeId, treeNode) {
		var tree = $.fn.zTree.getZTreeObj("opinionTree");
        if (treeNode.isParent) {
            var sNodes = tree.getSelectedNodes();
            if (!sNodes[0].open) {
                tree.expandNode(treeNode, true);
            } else {
               tree.expandNode(treeNode, false);
            }
            return false;
        } else {                            
            
        }
    }
    function brFun() {
    	// console.log(document.getElementById('opinionTree_1_span').innerHTML)
    	var a = $('#opinionTree');
    }
    function addDiyDom(treeId, treeNode) {  
        var spaceWidth = 5;  
        var switchObj = $("#" + treeNode.tId + "_switch"),  
        icoObj = $("#" + treeNode.tId + "_ico");  
        switchObj.remove();  
        icoObj.before(switchObj);  
  
        if (treeNode.level > 1) {  
            var spaceStr = "<span style='display: inline-block;width:" + (spaceWidth * treeNode.level)+ "px'></span>";  
            switchObj.before(spaceStr);  
        }  
       var spantxt=$("#" + treeNode.tId + "_span").html();
       
        if(spantxt.length>17){  
            spantxt=spantxt.substring(0,spantxt.indexOf("（"))+"<br>&nbsp&nbsp&nbsp"+spantxt.substring(spantxt.indexOf("（"));  
            $("#" + treeNode.tId + "_span").html(spantxt);  
        } 
    } 
