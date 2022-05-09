function navClick(element_id){
	console.log(element_id);
	var elmnt = document.getElementById(element_id);
	elmnt.scrollIntoView();
}



function scrollToTargetAdjusted(element_id){
	var element = document.getElementById(element_id);
	var headerOffset = document.getElementById('navbar').offsetHeight + 20;
	var elementPosition = element.getBoundingClientRect().top;
	var offsetPosition = elementPosition + window.pageYOffset - headerOffset;

	window.scrollTo({
		top: offsetPosition,
		behavior: "smooth"
	});   
}

function setState(status,element_id){
	var colors = ["rgb(220,220,220,0.5)","rgb(200,93,38,0.6)","rgb(76,190,108,0.9)"];
	document.getElementById(element_id).style.background = colors[status];
}
