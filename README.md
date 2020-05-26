# MiBand2
Library to work with Xiaomi MiBand 2 and Amazfit Bip
[Read the Article here](https://medium.com/@a.nikishaev/how-i-hacked-xiaomi-miband-2-to-control-it-from-linux-a5bd2f36d3ad)

# Contributors & Info Sources
1) Base lib provided by [Leo Soares](https://github.com/leojrfs/miband2)
2) Additional debug & fixes was made by my friend [Volodymyr Shymanskyy](https://github.com/vshymanskyy/miband2-python-test)
3) Some info that really helped i got from [Freeyourgadget team](https://github.com/Freeyourgadget/Gadgetbridge/tree/master/app/src/main/java/nodomain/freeyourgadget/gadgetbridge/service/devices/huami/miband2)

## Online Course "Object Detection with PyTorch"
Subscribe to my new online course: [LearnML.Today](http://learnml.today/)

# Run 

1) Install dependencies
```sh
python3 -m pip install -r requirements.txt
```
2) Turn on your Bluetooth
3) Unpair you MiBand2 from current mobile apps
4) Find out you MiBand2 MAC address
```sh
sudo hcitool lescan
```
5) Run this to auth device
```sh
python example.py --mac MAC_ADDRESS --init
```
6) Run this to call demo functions
```sh
python example.py --standard --mac MAC_ADDRESS
python example.py --help
```
7) If you having problems(BLE can glitch sometimes) try this and repeat from 4)
```sh
sudo hciconfig hci0 reset
```
This program requires creation of SQLITE3 database with the following schema:
CREATE TABLE `fitness` (
	`d_t`	NUMERIC NOT NULL UNIQUE,
	`r_k`	INTEGER NOT NULL,
	`r_i`	INTEGER NOT NULL,
	`s_t`	INTEGER NOT NULL,
	`h_r`	INTEGER,
	PRIMARY KEY(`d_t`)
);
CREATE TABLE `parameters` (
	`id`	INTEGER NOT NULL,
	`mac_add`	NUMERIC,
	`battery`	INTEGER,
	`soft_ver`	NUMERIC,
	`hard_rev`	NUMERIC,
	`ser_num`	INTEGER,
	`u_time`	NUMERIC NOT NULL,
	`hours`	INTEGER NOT NULL,
	`s_image`	BLOB NOT NULL,
	PRIMARY KEY(`id`)
);

You need to add the mac_add and 360px x 360px image in s_image 
