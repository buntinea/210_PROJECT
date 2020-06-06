this readMe file is to help how to run the files in the "210_PROJECT" repo.

This repo consists of 3 files; 
	Argon_code (c++)*
	arduinoSlave.ino (c++)
	raspberryGUI.py (python)

* note that the "Argon_code" isn't a file like the other two, so the contents must be copied into another file to run.



for this project to run, the argon and arduino must have their appropiate code flashed onto the device.
	To do this, i connected my arduino to my laptop via USB 
	Downloaded the "arduinoSlave.ino" file, and opened it with the arduino app
	uploaded the code
	
	For the argon, i flashed the code from the build.particle sight onto my device (https://www.youtube.com/watch?v=b6sUP16HWKM)
	To do this, i copied the code from "Argon_code"

Once that's done, then connect up all the devices as shown in the report (note that each device needs a source of power)

Run the raspberryGUI.py file on the raspberry. To do this, download the file "raspberryGUI.py" and save it on your raspberry
	Open a terminal and change the directory to the location of the file.
	type "python3 raspberryGUI.py" , which will launch the program
	to end it, click the escape button on the GUI