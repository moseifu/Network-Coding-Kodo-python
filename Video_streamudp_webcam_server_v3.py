import socket
import pygame
import pygame.camera
import sys
import time
import kodo
import random


def main():

    port = 5000

    pygame.init()

    # Encode 
    symbols = 64 
    symbol_size = 14400#3600 #14000
    encoder_factory = kodo.full_rlnc_encoder_factory_binary(symbols,
                                                                symbol_size)
    #   encoder = encoder_factory.build()
    

    # creation of the socket 
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Initiation of the camera 
    pygame.camera.init()
    
    screen = pygame.display.set_mode((640,480))
    size = (640,480)
    surface = pygame.surface.Surface(size,0,screen)
    # Set the parmaeter of the source 
    webcam = pygame.camera.Camera(0,(640,480))
    webcam.start()
    while True:
        encoder = encoder_factory.build()
        image = webcam.get_image(surface) # capture image
        # print ('image:',len(image))
        data = pygame.image.tostring(image,"RGB") # convert captured image to string, use RGB color scheme
        print ('data:',len(data),' Bytes',sys.getsizeof(data))
        print ('block size', encoder.block_size())
        encoder.set_symbols(data)
        for i in range(symbols):
             # With 50% probability toggle systematic
            #if random.choice([True, False]):
                #if encoder.is_systematic_on():
                #    print("Turning systematic OFF")
                #    encoder.set_systematic_off()
                #else:
                #    print("Turning systematic ON")
                #    encoder.set_systematic_on()
            packet = encoder.encode()
            serversocket.sendto(packet, ("127.0.0.1", port))     
            #print ('packet:',len(packet),' Bytes',sys.getsizeof(packet))

if __name__ == "__main__":
    main()
