function searchFunction() {
	var input, filter, list, l, a, i, txtValue;
	input = document.getElementById('myInput');
	filter = input.value.toUpperCase();
	list = document.getElementById("tag-list")
	l = document.getElementsByTagName('li');

	for (i = 0; i < l.length; i++){
		a = l[i];
		txtValue = a.textContent || a.innerText;
		if (txtValue.toUpperCase().indexOf(filter) > -1) {
			l[i].style.display = "";
		} else {
			l[i].style.display = "none";
		}	
		
	}
}