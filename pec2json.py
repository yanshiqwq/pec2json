import sys, json
motion_types = ["linear", "sineOut", "sineIn", "quadOut", "quadIn", "linear", "linear", "cubicOut", "cubicIn", "quartIn", "quartOut", "linear", "linear", "quintOut", "quintIn", "expoOut", "expoIn", "cricOut", "cricIn", "backOut", "backIn", "easeInOutCirc", "easeInOutBack", "elasticOut", "elasticIn", "bounceOut", "bounceIn", "linear", "linear"]
data = {"timing": {"offset": 0, "bpmList": []}, "judgeLineList": []}
construct = {"id": 0, "type": "construct", "startTime": 0, "endTime": 1919810, "properties": {"x": 0, "y": -0.3, "angle": 0, "alpha": 1, "speed": 0.01}}
events = {}
notes = {}
f = open(sys.argv[1], 'r', encoding = 'utf-8')
first_line = True
bpm_count = 0
event_count = 1
note_count = 0
note_info = 0
for line in f.readlines():
	line = line.replace("\n", "")
	if first_line == True:
		data["timing"]["offset"] = int(line) - 40
		first_line = False
	if note_info == 1:
		note_info = 0
		speed = line[2:]
		note = '{"id": ' + str(note_count) + ', "type": "' + type + '", "startTime": ' + str(start) + ', "endTime": ' + str(end) + ', "relativeX": ' + str(relativex) + ', "side": ' + str(side) + ', "speed": ' + speed + ', "isFake": ' + fake + '}'
		note_json = json.loads(note)
		try:
			notes[str(line_id)].append(note_json)
		except KeyError:
			notes.setdefault(str(line_id), [])
			notes[str(line_id)].append(note_json)
	if line[0: 2] == "bp":
		line_group = line.split( )
		bpm_json = json.loads('{"id":' + str(bpm_count) + ',"time": ' + line_group[1] + ',"bpm": ' + line_group[2] + '}')
		data["timing"]["bpmList"].append(bpm_json)
		bpm_count += 1
	if line[0: 1] == "c":
		line_group = line[1:].split( )
		line_id = line_group[1]
		try:
			event_id = len(events[str(line_id)])
		except KeyError:
			event_id = 1
		start = float(line_group[2]) * 72
		if line_group[0] == "v":
			type = "speed"
			end = start
			event = '{"id":' + str(event_id) + ',"type":"' + type + '","startTime":' + str(start) + ',"endTime":' + str(end) + ',"properties":{"speed":' + str(float(line_group[3]) / 1500) + ', "ease": "jump"}}'
		elif line_group[0] == "p":
			type = "move"
			end = start
			x = (float(line_group[3]) - 1024.000) / 1024
			y = (float(line_group[4]) - 700.000) / 700
			event = '{"id":' + str(event_id) + ',"type":"' + type + '","startTime":' + str(start) + ',"endTime":' + str(end) + ',"properties":{"x":' + str(x) + ',"y": ' + str(y) + ', "ease": "jump"}}'
		elif line_group[0] == "d":
			type = "rotate"
			end = start
			event = '{"id":' + str(event_id) + ',"type":"' + type + '","startTime":' + str(start) + ',"endTime":' + str(end) + ',"properties":{"angle":' + line_group[3] + ', "ease": "jump"}}'
		elif line_group[0] == "a":
			type = "fade"
			end = start
			if line_group[3] == "255":
				alpha = 1
			else:
				alpha = float(line_group[3]) / 256
			event = '{"id":' + str(event_id) + ',"type":"' + type + '","startTime":' + str(start) + ',"endTime":' + str(end) + ',"properties":{"alpha":' + str(alpha) + ', "ease": "jump"}}'
		elif line_group[0] == "m":
			type = "move"
			end = float(line_group[3]) * 72
			motion = motion_types[int(line_group[6])]
			x = (float(line_group[4]) - 1024.000) / 1024
			y = (float(line_group[5]) - 700.000) / 700
			event = '{"id":' + str(event_id) + ',"type":"' + type + '","startTime":' + str(start) + ',"endTime":' + str(end) + ',"properties":{"x":' + str(x) + ',"y": ' + str(y) + ', "ease": "' + motion + '"}}'
		elif line_group[0] == "r":
			type = "rotate"
			end = float(line_group[4]) * 72
			motion = motion_types[int(line_group[5])]
			event = '{"id":' + str(event_id) + ',"type":"' + type + '","startTime":' + str(start) + ',"endTime":' + str(end) + ',"properties":{"angle":' + line_group[3] + ', "ease": "' + motion + '"}}'
		elif line_group[0] == "f":
			type = "fade"
			end = float(line_group[3]) * 72
			if line_group[4] == "255":
				alpha = 1
			else:
				alpha = float(line_group[4]) / 256
			event = '{"id":' + str(event_id) + ',"type":"' + type + '","startTime":' + str(start) + ',"endTime":' + str(end) + ',"properties":{"alpha":' + str(alpha) + ', "ease": "linear"}}'
		event_json = json.loads(event)
		try:
			events[str(line_id)].append(event_json)
		except KeyError:
			events.setdefault(str(line_id), [])
			events[str(line_id)].append(construct)
			events[str(line_id)].append(event_json)
		event_count += 1
	if line[0: 1] == "n":
		note_info = 1
		line_group = line[1:].split( )
		line_id = line_group[1]
		start = float(line_group[2]) * 72
		if line_group[0] == "1":
			type = "click"
			end = start
			if line_group[4] == "2":
				side = -1
			else:
				side = 1
			if line_group[5] == "1":
				fake = "true"
			else:
				fake = "false"
			relativex = float(line_group[2]) / 1024
		if line_group[0] == "2":
			type = "hold"
			end = float(line_group[2]) * 72
			if line_group[5] == "2":
				side = -1
			else:
				side = 1
			if line_group[6] == "1":
				fake = "true"
			else:
				fake = "false"
			relativex = float(line_group[3]) / 1024
		if line_group[0] == "3":
			type = "flick"
			end = start
			if line_group[4] == "2":
				side = -1
			else:
				side = 1
			if line_group[5] == "1":
				fake = "true"
			else:
				fake = "false"
			relativex = float(line_group[2]) / 1024
		if line_group[0] == "4":
			type = "drag"
			end = start
			if line_group[4] == "2":
				side = -1
			else:
				side = 1
			if line_group[5] == "1":
				fake = "true"
			else:
				fake = "false"
			relativex = float(line_group[2]) / 1024
		note_count += 1
f.close()
for eventzip,notezip in zip(events.items(),notes.items()):
	line_count,event = eventzip
	note_count,note = notezip
	line = json.loads('{"noteList": [], "eventList": [], "id": ' + str(line_count) + '}')
	line["eventList"] = event
	line["noteList"] = note
	data["judgeLineList"].append(line)
#print(json.dumps(data, sort_keys=True, indent=4, separators=(', ', ': ')))
print(json.dumps(data))