<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" 
                    "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es">
<head>
	<script type="text/javascript" src="/static/js/jquery.js"></script>
	<script type="text/javascript" src="a.js"></script>
</head>
<body>
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
	<a href="/static/js/hola.html">JS Funciona?</a>
	<a href="hola.html">JS Funciona?</a>
	<div id="prepython">
		<input size="20" id="holainput" type="text"/>
		<input type="submit" name="clickkkkka" value="Ilkka" onclick="python('feo');"/>
	</div>
	<a href="#" onclick="javascript:python('feo')">Ilkka Simonson</a>
	<div id="python">
	</div>
	<div id="image">
		<img src="/images/alemania1.JPG" alt="Holaaaaaaaaaa" />
		<img src="/images2/alemania1.JPG" alt="Holaaaaaaaaaa2" />
		<img src="alemania1.JPG" alt="Holaaaaaaaaaa3" />
		<% for (int i = 0; i < 20; i++){%>
		<p>hola</p>
		<%}%>
		<p><%=request.getContext()%></p>
	</div>
</body>
</html>