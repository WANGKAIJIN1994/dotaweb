window.onload=function(){
	var nav = document.getElementById("nav-heard");
	var aA = nav.getElementsByTagName("a");
	for(var i=0;i<aA.length;i++){
		aA[i].onmouseover = function(){
			clearInterval(this.time);
			var This = this;
			This.time = setInterval(function(){
				This.style.width = This.offsetWidth+5+"px";
				if(This.offsetWidth>=160){
					clearInterval(This.time)
				}
			},30)
		}
		aA[i].onmouseout = function(){
			clearInterval(this.time);
			var This = this;
			This.time = setInterval(function(){
				This.style.width = This.offsetWidth-5+"px";
				if(This.offsetWidth<=120){
					This.style.width='120px';
					clearInterval(This.time)
				}
			},30)
		}
	}
}