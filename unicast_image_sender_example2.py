import argparse
import kodo
import os
import socket
import sys
import time

#IP Adress of the reciever
#Unicast_Rcvr ='172.17.67.45'
Unicast_Rcvr = socket.gethostname()
Unicast_PORT = 5009


def main():
    """
    Example of a sender which encodes and sends an image file.


    """

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        '--file-path',
        type=str,
        help='Path to the file which should be send.',
        default=os.path.realpath(__file__))

    parser.add_argument(
        '--ip',
        type=str,
        help='The ip to send to.',
        default=Unicast_Rcvr)

    parser.add_argument(
        '--port',
        type=int,
        help='The port to send to.',
        default=Unicast_PORT)

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run with network use.')

    args = parser.parse_args()

    # Check file.
    if not os.path.isfile(args.file_path):
        print("{} is not a valid file.".format(args.file_path))
        sys.exit(1)

    # Set the number of symbols (i.e. the generation size in RLNC you may need to change the symbol size depending on the size of the image you have
    # terminology) and the size of a symbol in bytes
    symbols = 64
    symbol_size = 14000

    # In the following we will make an encoder factory.
    # The factories are used to build actual encoder
    encoder_factory = kodo.full_rlnc_encoder_factory_binary(symbols,
                                                            symbol_size)
    encoder = encoder_factory.build()

   # Define UDP socket for the sender
    sock = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_DGRAM,
        proto=socket.IPPROTO_UDP)

   

    # Get the data to encode.
    # import the image 
    print "Enter file name of the image with extentsion (example: filename.jpg,filename.png or if a video file then filename.mpg etc) - "
    fname = raw_input() 

    f = open(fname,'rb')
    data_in = f.read()
    f.close()

    # Assign the data buffer to the encoder so that we can
    # produce encoded symbols
    encoder.set_symbols(data_in)

    address = (args.ip, args.port)

    print("Processing")
    counter = 0
    while True and not args.dry_run:
        time.sleep(0.2)
        counter += 1
        # Generate an encoded packet
        sys.stdout.write("\tEncoding packet...")
        packet = encoder.encode()
        sys.stdout.write(" done!\n")

        # Send the packet.
        sock.sendto(packet, address)

    print("Processing finished")

if __name__ == "__main__":
    main()
