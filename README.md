# Gateway demo
Requires a "Raspberry Pi 3 Model B+" with "u-blox LARA-R2" hat and an "Adafruit Feather nRF52840 Express". 

## Arduino
The serial.ino must be run on an "Adafruit Feather nRF52840 Express" which must have a serial connection to the Raspberry 3.
This connection should be established automatically if the Arduino and the Raspberry are connected via USB.

## Python
The `RXTX` package requires Pyhton 2 with [pyserial](https://pypi.org/project/pyserial/) and [ublox-lara-r2](https://pypi.org/project/ublox-lara-r2/) to be installed.

Start Python in sudo mode, otherwise instructions sent to the LARA-R2 might get blocked:
```bash
sudo python
```

The code can be started like this:
```python
from RXTX import *
r = RXTX(debug=True)
r.connect()
```

If `debug` is set to `True`, additional information will be printed during the program execution.
