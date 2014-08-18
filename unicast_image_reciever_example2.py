import argparse
import kodo
import socket
import struct
import sys
import time

#MCAST_GRP = '224.1.1.1'
Unicast_Rcvr = socket.gethostname()
Unicast_PORT = 5007


def main():
    """
    Example showing a receiver which receives data, decodes it, and finally
    writes it to a file.
    """

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        '--output-file',
        type=str,
        help='Path to the file which should be received.',
        default='output_file')

   
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
        help='Run without network use.')

    args = parser.parse_args()

    # Set the number of symbols (i.e. the generation size in RLNC
    # terminology) and the size of a symbol in bytes
    symbols = 64
    symbol_size = 14000

    # In the following we will make an decoder factory.
    # The factories are used to build actual decoder
    decoder_factory = kodo.full_rlnc_decoder_factory_binary(symbols,
                                                            symbol_size)
    decoder = decoder_factory.build()

    sock = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_DGRAM,
        proto=socket.IPPROTO_UDP)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('', args.port))
    sock.connect((args.ip, args.port))
    
    #mreq = struct.pack("4sl", socket.inet_aton(args.ip), socket.INADDR_ANY)

    #sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Processing")
    package_number = 0
    while not decoder.is_complete() and not args.dry_run:
        time.sleep(0.2)
        packet = sock.recv(1024000)

        sys.stdout.write("\tDecoding packet {}...".format(package_number))
        decoder.decode(packet)
        sys.stdout.write(" done!\n")
        package_number += 1
        print("rank: {}/{}".format(decoder.rank(), decoder.symbols()))

        # Write data to file (it may not be valid until the very end though).
        f = open(args.output_file, 'wb')
        f.write(decoder.copy_symbols())
        f.close()

    print("Processing finished")

if __name__ == "__main__":
    main()

