function navClick(element_id){
	console.log(element_id);
	var elmnt = document.getElementById(element_id);
	elmnt.scrollIntoView();
}



function scrollToTargetAdjusted(element_id){
	var element = document.getElementById(element_id);
	var headerOffset = width = document.getElementById('navbar').offsetHeight + 20;
	var elementPosition = element.getBoundingClientRect().top;
	var offsetPosition = elementPosition + window.pageYOffset - headerOffset;

	window.scrollTo({
		top: offsetPosition,
		behavior: "smooth"
	});   
}
