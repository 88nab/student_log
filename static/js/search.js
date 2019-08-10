function searchFunction() {
	var input, filter, list1, list2, p, a, i, txtValue;
	input = document.getElementById('myInput');
	filter = input.value.toUpperCase();
	list1 = document.getElementById("tag-list")
	list2 = document.getElementById("sTag-list")
	p = document.getElementsByTagName('p');

	for (i = 0; i < p.length; i++){
		a = p[i];
		txtValue = a.textContent || a.innerText;
		if (txtValue.toUpperCase().indexOf(filter) > -1) {
			p[i].style.display = "";
		} else {
			p[i].style.display = "none";
		}	
		
	}
}