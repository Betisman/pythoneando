<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" 
                    "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
</head>
<body>
	<script type="text/javascript" src="<%=request.getContextPath()%>/jquery.js"></script>
	<script type="text/javascript" src="a.js"></script>
	<script type="text/javascript">
	function python(value){
	//a();
	$.ajax({
	url: 'ajax/?value='+value,
	type: 'GET',
	dataType: 'html',
	timeout: 1000,
	error: function(){
		alert('Error loading HTML document');
	},
	success: function(html){
	alert(value);
	$('#python').html('<p>'+html+'</p>');
}
});
}
	</script>
	<div id="prepython">
		<input size="20" id="holainput" type="text"/>
		<input type="submit" name="clickkkkka" value="Ilkka" onclick="python('feo');"/>
	</div>
	<a href="#" onclick="javascript:python('feo')">Ilkka Simonson</a>
	<div id="python">
	</div>
</body>
</html>