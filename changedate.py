import json

with open("classdojo_output/tmpyjxu7q3i\data.json") as y:
    # Loading the json data
    data = json.load(y)
    # Opening the output file
    f = open('changedate.sh', 'w', encoding="utf8")
    for entry in data:
        for picture in entry["contents"]["attachments"]:
            parts = picture["path"].split('/')
            name = '_'.join(parts[3:]).replace('-', '_')
            if name[-3:] == "jpg":
                # Creating the output file line by line
                f.write("exiftool -AllDates=\""+entry["time"]+"\" classdojo_output/tmpyjxu7q3i\\"+name+"\n")
    # f.write(output)
    # Closing the output file
    f.close