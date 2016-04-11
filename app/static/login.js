function check(){
	if(form_login.username.value == ""){
		alert("请输入用户名");
		return false;
	}

	if(form_login.password.value == ""){
		alert("请输入密码");
		return false;
	}

	if(document.getElementsByName("confirm")[0] != undefined){
		if(form_login.confirm.value != form_login.password.value){
			alert("两次输入的密码不一致");
			return false;
		}
	}
}

function show_Login(){
    document.getElementById("setRegister").innerHTML = "";
    document.getElementById("login").style.color = "white";
    document.getElementById("switchLR").setAttribute("value","登录");
    document.form_login.action = "login";
	 changebgimg();
}

function show_Register(){
	document.getElementById("setRegister").innerHTML = '<input onkeydown="switchline(event)" class="login-input all-radius" type="password" name="confirm" placeholder="确认密码:"/><br/>';
    document.getElementById("login").style.color = "rgb(204,204,204)";
    document.getElementById("register").style.color = "white";
    document.getElementById("switchLR").setAttribute("value","注册");
    document.form_login.action = "register";
    changebgimg();
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