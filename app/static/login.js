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
}

function show_Login(){
    document.getElementById("setRegister").innerHTML = "";
    document.getElementById("login").style.color = "white";
    document.getElementById("switchLR").setAttribute("value","SignIn");
    document.form_login.action = "login";
    document.getElementById("forgetinfo").style.display = "block";
	 changebgimg();
}

function show_Register(){
	document.getElementById("setRegister").innerHTML = '<input onkeydown="switchline(event)" class="login-input all-radius" type="password" name="confirm" placeholder="confirm password:"/><br/><input onkeydown="switchline(event)" class="login-input all-radius" type="email" name="email" placeholder="your email"/><br/>';
    document.getElementById("login").style.color = "rgb(204,204,204)";
    document.getElementById("register").style.color = "white";
    document.getElementById("switchLR").setAttribute("value","Register");
    document.form_login.action = "register";
    document.getElementById("forgetinfo").style.display = "none";
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