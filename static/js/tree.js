
   $(document).ready(function(){
      opinionTree();
   });

   function opinionTree() {
   		var setting = {
    		edit: {
    			enable: true,
          showRemoveBtn: false,
          showRenameBtn: false
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
			url : 'http://table.jcrb.com:8000/index',
			dataType : 'json',
			// data : data,
			error : function() {

			},
			success : function(data, status, xhr) {
				console.log(data);
				var treeObj = $.fn.zTree.init($("#opinionTree"), setting, data.node);
        var a = $('#search-input')[0].style.display = 'block';
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
          window.location.href = treeNode.url;
      }
  }
  function addDiyDom(treeId, treeNode) {  
     var span=$("#" + treeNode.tId + "_span");
     var hand = '<svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="14px" height="10.72px" viewBox="0 0 16.847 12.902" enable-background="new 0 0 16.847 12.902" xml:space="preserve"> <path d="M9.968,1.525H9.239V0.771h0.753V1.5h0.728h0.753v0.753H10.72H9.968V1.525z M6.19,12.148h0.752v-0.752H6.19V12.148z M0,5.267 h0.751v-1.51H0V5.267z M12.99,3.751h0.753h0.752V2.998h-0.752h-0.749V2.259h-0.752h-0.753v0.754h0.753h0.748V3.751z M16.046,3.76 h-0.021h-0.751H14.5v0.752h0.774h0.751v6.09h-0.707h-0.753v0.752h0.753h0.707h0.046h0.776V3.76H16.046z M12.266,11.377v0.752h1.128 h1.127v-0.752h-1.127H12.266z M8.399,10.626V9.874h-1.49H5.418v0.745H5.416v0.752h0.752v-0.745h0.741H8.399z M7.614,8.337V7.585 H6.122h-1.49V8.33H4.63v1.552h0.753V8.337h0.739H7.614z M7.669,6.048V5.296H5.35H3.978H3.86H0.758v0.752h3.101v1.517h0.752V6.048 H5.35H7.669z M6.949,2.289h0.753V0.753h0.381h1.14V0h-1.14H6.945v0.753h0.004V2.289z M6.967,12.151v0.751h2.628h2.628v-0.751H9.595 H6.967z M10.692,3.747V2.995H8.474V2.267H7.722v0.728H5.721H0.748v0.752h4.973H10.692z"/></svg>';
      if(span.parent().hasClass('level0')){  
          var spantxt = span.html();
          spantxt=spantxt.substring(0,spantxt.indexOf("（"))+"<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<span class='font-smaller'>"+spantxt.substring(spantxt.indexOf("（"))
          + "</span>" + hand;  
          $("#" + treeNode.tId + "_span").html(spantxt);  
      } 
  } 

  $('.divSearch').click(function(){
      console.log(this);
      window.location.href = 'http://table.jcrb.com/table.html?query=' + $('.form-input').val();
  })
