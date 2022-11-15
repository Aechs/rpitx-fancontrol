# rpitx-fancontrol
Simple program using rpitx to control ceiling fans

This is a Python script using [rpitx](https://github.com/F5OEO/rpitx) to control Harbor Breeze fans (or other simple rf fans) with a Raspberry Pi.

In order to use this with your own fan, you need to know the fan ID and frequency which can be obtained using a sdr/tv-tuner. Your Raspberry Pi needs*  a bandpass filter on pin 7 or GPIO4. Read [here](https://github.com/F5OEO/rpitx#hardware) for more info

## The Fan
![16863098 512](https://user-images.githubusercontent.com/89534947/200408889-34aa8f5b-2945-4a70-b2e1-cf566fdb3ac7.jpeg)

This fan can be found for cheap at local home improvement stores and are common in some rental units [(link)](https://www.lowes.com/pd/Harbor-Breeze-Beach-Creek-44-in-Brushed-Nickel-LED-Indoor-Ceiling-Fan-with-Light-Kit-and-Remote-3-Blade/1000181467).
The fan comes with hardware to attach to a ceiling junction box, a reciever, and a small remote to control the fan.

The Remote has 5 buttons for controling the light and fan speed. This remote uses 304.2MHz on/off keying (or ook) to control the fan.

## Signal Decoding
In order to control the fan, you need to know the ID of the fan and the control code used for each button the remote has. Using [this](https://github.com/jopohl/urh) software, the fan remote, and a SDR radio, The signal can be decoded to simple binary data once you know the right frequency. For this fan it is 304.2MHz

![Screenshot from 2022-11-07 14-44-56](https://user-images.githubusercontent.com/89534947/200411774-46cc5c5a-611b-492f-8748-c4ae474d9764.png)

 This remote uses a carrier signal of '10_' where '\_' is 1 bit of data. Removing the carrier signal produces this below
 
![Screenshot from 2022-11-07 13-40-25](https://user-images.githubusercontent.com/89534947/200414212-5426b22d-fec6-4cf5-9127-96c84cc4e7e8.png)


After Analyzing the decoded signal, The first 16 bits correspond to the fan ID or which fan the remote is talking to (marked in green above). The last 8 Bits are the Control Code or which button on the remote got pressed (marked in yellow)

So, we need to get the Pi to send this signal in order to control the fan.

## Programming

rpitx has a module called sendook that allows us to send on/off keyed messages which we will use to control the fan. sendook also requires us to specfiy a few extra details such as timing between on/off keys, pause duration, and # of repeats. 


Install rpitx
```sh
sudo apt-get install git
git clone https://github.com/F5OEO/rpitx
cd rpitx
./install.sh
sudo reboot
```
Download the program
```sh
wget 'https://raw.githubusercontent.com/Aechs/rpitx-fancontrol/main/parse_tx.py'
```

Run the program
This example would set a low fan speed on the "K" fan
```sh
python parse_tx.py K 1
```
