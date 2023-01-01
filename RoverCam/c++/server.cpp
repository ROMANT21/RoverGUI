#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <stdio.h>
#include <sys/socket.h> 
#include <arpa/inet.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <unistd.h> 
#include <string.h>

using namespace cv;
using namespace std;

int device = 1;

VideoCapture cap(device);

void *display(void *);

int main(int argc, char** argv) {

    // ---------- NETWORKING CODE -------------
    int localSocket, remoteSocket, port = 4097;

    struct sockaddr_in localAddr, remoteAddr;
    pthread_t thread_id;

    int addrLen = sizeof(struct sockaddr_in);

    if ((argc > 1) && (strcmp(argv[1],"-h") == 0)) {
        std::cerr << "usage: ./RoverCam [port] [capture device]\n" <<
                     "port:             : socket port (default is 4097)\n" <<
                     "capture device    : id of device (default is 0)" << endl;
        exit(1);
    }

    if (argc == 2) 
        port = atoi(argv[1]);
    
    localSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (localSocket == -1) {
        perror("socket call failed");
    }

    localAddr.sin_family = AF_INET;
    localAddr.sin_addr.s_addr = INADDR_ANY;
    localAddr.sin_port = htons(port);

    if (bind(localSocket, (struct sockaddr *)&localAddr, sizeof(localAddr)) < 0) {
        perror("can't bind socket");
        exit(1);
    }

    listen(localSocket, 3);

    std::cout << "Waiting for connections \n" << 
                 "Server Port: " << port << endl;

    while(1) {
        remoteSocket = accept(localSocket, (struct sockaddr *)&remoteAddr, (socklen_t*)&addrLen);
        if (remoteSocket < 0) {
            perror("connection failed!");
            exit(1);
        }
        std::cout << "Connection accepted" << endl;
        pthread_create(&thread_id,NULL,display,&remoteSocket);
    }

    return 0;
}
void *display(void *ptr){
    int socket = *(int *)ptr;

    Mat img;
    img = Mat::zeros(480,640,CV_8UC1);

    if (!img.isContinuous()) { 
        img = img.clone();
    }

    int imgSize = img.total() * img.elemSize();
    // Current bytes: 1843200
    // int imgSize = img.rows*img.cols*CV_ELEM_SIZE(img.type());
    int bytes = 0;
    int key;

    if (!img.isContinuous()) {
        img = img.clone();
    }

    std::cout << "Image Size: " << imgSize << std::endl;
    std::cout << "Img.data size: " << sizeof(img.data) << std::endl;
    //namedWindow("CV Server", 1);

    while (1)
    {
        cap.read(img);
        //imshow("CV Server", img);
        if ((bytes = send(socket, img.data, imgSize, 0)) < 0) {
            std::cerr << "bytes = " << bytes << std::endl;
            break;
        }
    }
    return 0;
}
