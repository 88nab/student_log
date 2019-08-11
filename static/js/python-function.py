

def convert_to_seconds(timestamp):
	split_timestamp = timestamp
	string_minutes = timestamp.split('.')[0]
	string_seconds = timestamp.split('.')[1]
	minutes = int(string_minutes)
	seconds = int(string_seconds)

	if minutes ==0:
		return seconds
		
	else if minutes > 0:
		return (minutes * 60) + seconds
	