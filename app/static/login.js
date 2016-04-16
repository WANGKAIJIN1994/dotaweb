var checknumber;
function obtaincheck(){
	var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
	if(!reg.test(form_login.email.value)){
		alert("please enter the right email");
		return false;
	}
	else{
		XMLHttp.sendRequest("POST","/sendmail","form_login.email.value");
		return true;
	}
}

function check(){
	if(form_login.username.value == ""){
		alert("please enter the username");
		return false;
	}

	if(form_login.password.value == ""){
		alert("please enter the password");
		return false;
	}

	if(document.getElementsByName("confirm")[0] != undefined){
		if(form_login.confirm.value != form_login.password.value){
			alert("The two passwords do not match");
			return false;
		}
	}

	if(document.getElementsByName("checknum")[0] != undefined){
		if(form_login.checknum.value != checknumber){
			alert("the checknumber is wrong!");
			return false;
		}
	}
}

function show_Login(){
    document.getElementById("setRegister").innerHTML = "";
    document.getElementById("login").style.color = "white";
    document.getElementById("switchLR").setAttribute("value","SignIn");
    document.getElementById("reset").setAttribute("value","FindPass");
    document.form_login.action = "login";
	 changebgimg();
}

function show_Register(){
	document.getElementById("setRegister").innerHTML = 
	'<input onkeydown="switchline(event)" class="login-input all-radius" type="password" name="confirm" placeholder="confirm password:"/><br/><input onkeydown="switchline(event)" class="login-input all-radius" type="email" name="email" placeholder="your email"/><br/><input onkeydown="switchline(event)" class="login-input all-radius" type="text" name="checknum" placeholder="checknumber"/><input type="button" id ="obtain" class="login-btn all-radius" value="Obtain" onclick="obtaincheck()" /><br/>'
    document.getElementById("login").style.color = "rgb(204,204,204)";
    document.getElementById("register").style.color = "white";
    document.getElementById("switchLR").setAttribute("value","Register");
    document.getElementById("reset").setAttribute("value","reset");
    document.form_login.action = "register";
    document.getElementsByName("checknum")[0].style.width = "180px";
    document.getElementsByName("checknum")[0].style.margin = "0 -210px 0 30px";
    changebgimg();
}

function FindPassword(){
	if (document.getElementById("reset").value == 'FindPass') {
		form_login.password.type = 'email';
		form_login.password.name = 'email';
		form_login.email.placeholder = 'please enter your email';
		form_login.reset.value = "AbtainPass";
		form_login.reset.onclick = function(){
		if(obtaincheck()){
			location.href = "/"
		}
		}
	};
	if (document.form_login.action == 'reset') {
		form_login.reset();
	};
}

function switchline(event){
	var keyCode = event.keyCode;
	if(keyCode == 13||keyCode == 39){
		var inputs = document.getElementsByName('form_login')[0].getElementsByTagName('input');
		var input = document.getElementsByName(document.activeElement.name)[0];
		var count = 0;
		(function(){
				for(; count < inputs.length; count++){
					if(input == inputs[count]){
						count++;
						break;
				}
			}
		})();
		inputs[count].focus();
		event.preventDefault();
	}
}

function changebgimg(){
	var bgin = parseInt(Math.random()*5+1);
	document.body.style.backgroundImage = "url(static/images/p_0"+bgin+".jpg)";
}

var XMLHttp = {
	XMLHttpRequestPool:[],
	getInstance:function(){
		for(var i=0;i<this.XMLHttpRequestPool.length;i++){
			if(this.XMLHttpRequestPool[i].readyState==0 || this.XMLHttpRequestPool[i].readyState==4){
				return this.XMLHttpRequestPool[i];
			}
		}
		this.XMLHttpRequestPool[this.XMLHttpRequestPool.length] = this.createXMLHttpRequest();
		return this.XMLHttpRequestPool[this.XMLHttpRequestPool.length-1];
	},
	createXMLHttpRequest:function(){
		if(window.XMLHttpRequest){
			var objXMLHttp=new XMLHttpRequest();
		}
		else{
			var MSXML = ['MSXML2.XMLHttp.5.0','MSXML2.XMLHttp.4.0','MSXML2.XMLHttp.3.0',
			'MSXML2.XMLHttp','Microsoft.XMLHttp'];
			for(var n=0;n<MSXML.length;n++){
				try{
					var objXMLHttp=new ActiveXObject(MSXML[n]);
					break;
				}
				catch(e){}
			}
		}
		if(objXMLHttp.readyState==null){
			objXMLHttp.readyState=0;
			objXMLHttp.addEventListener("load",function(){
				objXMLHttp.readyState =4;
				if(typeof objXMLHttp.onreadystatechange == "function"){
					objXMLHttp.onreadystatechange();
				}
			},false);
		}
		return objXMLHttp;
	},
	sendRequest:function(method,url,date){
		var objXMLHttp = this.getInstance();
		with(objXMLHttp){
			try{
				if(url.indexOf("?")>0){
					url += "&version="+Math.random();
				}
				else{
					url += "?version="+Math.random();
				}
				open(method,url,true);
				if(method=="POST"){
					setRequestHeader('Content-Type','application/x-www-form-urlencoded');
					send(date);
				}
				if(method=="GET"){
					send(null);
				}
				onreadystatechange = function(){
					if(objXMLHttp.readyState == 4 && (objXMLHttp.status == 200||objXMLHttp.status==304)){
						checknumber = objXMLHttp.responseText;
					}
				}
			}
			catch(e){alert(e);}
		}
	}
};