from scapy.all import *

pkt = sniff(filter="ether dst 01:80:c2:00:00:00", count=1)

pkt[0]

pkt[0].show()

pkt[0][0].show()

pkt[0][1].show()

pkt[0][2].show()