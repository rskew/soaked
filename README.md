# Soaked

Control garden critters to water the veggies and eventually also other things.

This project uses [MicroPython](https://micropython.org/). I'm running an [ESP32](http://esp32.net/) microcontroller, with digital I/O controlling relays that switch a couple of solenoid valves which are part of the drip watering system in my front yard.

### Roadmap:
- [x] run a webserver on a microcontroller
- [x] control i/o pins via a web interface
- [x] i/o pins control garden watering system
- [ ] control watering schedule via web interface
- [ ] control multiple nodes from a single webserver
- [ ] add soil moisture sensor nodes
- [ ] watering responds to soil moisture
- [ ] adapt watering schedule to weather forecast


## Running it

Board preparation:

- Load the MicroPython firmware onto the board.

- Create file '/wifi_creds' with the wifi ssid on the first line and the
  password on the second line.

- Load boot.py and main.py onto the board.


## License

The project is licensed under the terms of the Apache License (Version 2.0).

See [LICENSE](./LICENSE) or http://www.apache.org/licenses/LICENSE-2.0 for details.
