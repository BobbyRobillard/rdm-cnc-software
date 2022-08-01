import time, requests, subprocess

while 1 > 0:
    try:
        gcode = requests.get("http://backoffice.rdminnovation.com/management/get-task")
        to_write = gcode.text.replace("<br />", "\n")
        to_write = gcode.text.replace("<br/>", "\n")
        if "$H" in to_write:
            print("Valid code collected, starting cut process")
            f = open("cnc_task.gcode", "w")
            f.write(to_write)
            f.close()
            subprocess.call(["mv", "./cnc_task.gcode", "/home/pi/Auto_Cut_Program"])
            subprocess.call(["sh", "/home/pi/Auto_Cut_Program/cut_bot.sh"])
            subprocess.call(["python", "/home/pi/Auto_Cut_Program/stop.py"])
        else:
            print("Just waiting for something to do...")
        time.sleep(3)
    except Exception as e:
        print("Eh, something funky is going on boss...")
        print(str(e))

# Get GCODE from server
# Store code to file on disk
# Execute cut bot script
