$(document).ready(function () {
    
    var doLogin = function () {
        
		 var username = $("#inputEmail").val();
	        var password = $("#inputPassword").val();

	        $.ajax({
	            type: "GET",
	            url: "Login/login",
	            async: false,
	            data: { username: username, password: password },
	            datatype: "json", //"xml", "html", "script", "json", "jsonp", "text".
	            beforeSend: function () {
	                //$("#msg").html("logining"); 
	            },
	            success: function (data) {
	                obj = $.parseJSON(data);
	                if (obj.success) {
	                	window.location.href = "home.html";
	                } else {
	                	$('#myModal').modal();
	                }
	            },
	            complete: function (XMLHttpRequest, textStatus) {
	                //alert(XMLHttpRequest.responseText);
	                //alert(textStatus);
	            },
	            error: function () {
	                //请求出错处理
	            }
	        });
	}
	
	$('#inputPassword').bind('keypress',function(event){
		if(event.keyCode == "13")    
        {
			doLogin();
        }
		
	});
	$("#login").click(doLogin);
});