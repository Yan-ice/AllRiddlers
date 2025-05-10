import json

json_file = None;
with open('ridd.json', 'r') as fil:
    json_file = json.load(fil)

name_list = []
first_night = []
other_night = []

for ch in json_file:
    key = ch['name']
    if '&' in key or ch['id'] == '_meta':
        continue;
    name_list.append(key)
    firstni = ''
    otherni = ''
    setup = False
    reminders = []
    if 'firstNight' in ch:
        firstnio = ch['firstNight']
        if firstnio > 0:
            firstni = ch['firstNightReminder']
            first_night.append((firstnio, key))

    if 'otherNight' in ch:
        othernio = ch['otherNight']
        if othernio > 0:
            if 'otherNightReminder' in ch:
                otherni = ch['otherNightReminder']
                other_night.append((othernio, key))
        
    if 'reminders' in ch:
        reminders = ch['reminders']

    if 'remindersGlobal' in ch:
        remindersGlobal = ch['remindersGlobal']

    if 'setup' in ch:
        setup = ch['setup']

    reminder_ = {
        'firstNightRemind': firstni,
        'otherNightRemind': otherni,
        'remindIcons': reminders,
        'remindIconsGlobal': reminders,
        'affectSetup': setup,
    }
    import json
    import os
    if os.path.exists(f'data/{key}'):
        with open(f'data/{key}/remind.json', 'w') as f:
            json.dump(reminder_, f, ensure_ascii=False)
        print(key)

first_night.sort(key=lambda x: x[0])
other_night.sort(key=lambda x: x[0])

# print(name_list)
with open('first_night_order.txt', 'w') as f:
    for a in first_night:
        f.write(a[1]+"\n")
with open('other_night_order.txt', 'w') as f:
    for a in other_night:
        f.write(a[1]+"\n")