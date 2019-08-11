

function convertTimestamp(timestamp) {
	var input = timestamp;
	var string  = input.toString();
	var numberArray = string.split('.');
	var array = new  Array();
	array = numberArray;
	var minutes = array[0];
	var seconds= array[1];
	if (minutes==0) {
		return seconds;
	}
	else if (minutes>0) {
		var totalSeconds = ((minutes * 60) + seconds);
		return totalSeconds;

	}

}
