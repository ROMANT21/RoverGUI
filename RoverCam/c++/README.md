# RoverCam C++

This code uses OpenCV to send images between a server and client via sockets.

## Building and running

### Requirements

Requires OpenCV and can be installed with
```
sudo apt install libopencv-dev
```
Note: make sure you are on Ubuntu 20.04 so that OpenCV 4 installs instead of OpenCV 3 which will install on earlier versions.
### Building

Navigate to /RoverCam/c++/ and run the following code:
```
mkdir build && cd build
cmake ..
make
```


### Running
#### Server
Usage:
```
./server [port]
```
Running "server" without arguments will use port 4096 by default, but a port can be specified.

#### Client
Usage:
```
./client [ip of server] [port]
```
Client needs an ip and port to be specified to work. If testing on the same device, use 127.0.0.1 for address and 4096 for port.