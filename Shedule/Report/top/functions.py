from datetime import datetime, timedelta


def GetPartOfTime(obj, position):
	#obj - date.time
	#pos: 0 - hours, 1 - minutes, 2 - seconds
	return int(str(obj).split(":")[position])