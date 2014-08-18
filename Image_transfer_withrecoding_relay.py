#! /usr/bin/env python
# encoding: utf-8

# Copyright Steinwurf ApS 2011-2013.
# Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
# See accompanying file LICENSE.rst or
# http://www.steinwurf.com/licensing

import os
import sys
import argparse
import time
import socket
import kodo


def main():
    
    # Set the number of symbols (i.e. the generation size in RLNC
    # terminology) and the size of a symbol in bytes
    symbols = 64
    symbol_size = 14000

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run with network use.')

    args = parser.parse_args()


    # In the following we will make an encoder/decoder factory.
    # The factories are used to build actual encoders/decoders
    decoder_factory = kodo.full_rlnc_decoder_factory_binary(symbols,
                                                            symbol_size)
    decoder1 = decoder_factory.build()

    #Socket for the receiver 
    Unicast_Rcvr = ''
    Unicast_PORT = 5008
    
    sock = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_DGRAM,
        proto=socket.IPPROTO_UDP)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', Unicast_PORT))
    

    print ("reveive data")
    #Socket for the sender 
    Unicast_Rcvr2 ='127.0.0.1'
    Unicast_PORT2 = 5007
    sock2 = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_DGRAM,
        proto=socket.IPPROTO_UDP)
    
    print ("Socket sender") 

    # Assign the data buffer to the encoder so that we may start
    # to produce encoded symbols from it
   
    address = (Unicast_Rcvr2, Unicast_PORT2)

    print("Processing")
    package_number = 0
    
    while not decoder1.is_complete() and not args.dry_run:
        print ("WHILE")
        time.sleep(0.2) 
        packet = sock.recv(1024000)
        print ("Receiving sock")
	#Decode 
        sys.stdout.write("\tDecoding packet {}...".format(package_number))

        decoder1.decode(packet)

        sys.stdout.write(" done!\n")
        print("rank: {}/{}".format(decoder1.rank(), decoder1.symbols()))

	#Recode
	sys.stdout.write("\tRecoding packet...")
        packet = decoder1.recode()
        sys.stdout.write(" done!\n")

        package_number += 1
	# Send the packet.
	sock2.sendto(packet, address)


 
if __name__ == "__main__":
    main()
