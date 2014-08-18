import socket
import pygame
import sys
import pygame.camera
import kodo
import time

def main():


    host = "127.0.0.1"
    port=5000
    screen = pygame.display.set_mode((640,480))
    size = (640,480)
    surface = pygame.surface.Surface(size,0,screen)
    #screen = pygame.display.set_mode((640,480),0)

    # Decoder 
    symbols = 64
    symbol_size = 14400#3600  #14000
    decoder_factory = kodo.full_rlnc_decoder_factory_binary(symbols,
                                                                symbol_size)

    # socket 
    
    clientsocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    clientsocket.bind(('', port))
    
    # loop .recv, it returns empty string when done, then transmitted data is completely received
    while True:
        decoder = decoder_factory.build()

        while not decoder.is_complete():
            recvd_data = clientsocket.recv(921600)
            print ('recv_data',len(recvd_data),' Bytes',sys.getsizeof(recvd_data))
            decoder.decode(recvd_data)
        data_out = decoder.copy_symbols()
        print ('dataout:',len(data_out),' Bytes',sys.getsizeof(data_out))
        
        image = pygame.image.frombuffer(data_out,(640,480),"RGB") # convert received image from string
        print ("convert image")
        screen.blit(image,(0,0)) # "show image" on the screen
        pygame.display.update()
        print ('fin')
        # check for quit events
        #for event in pygame.event.get():
         #    if event.type == pygame.QUIT:
          #          pygame.quit()
           #         sys.exit()


if __name__ == "__main__":
        main()


