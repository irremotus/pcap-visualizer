#!/bin/python3

from scapy import all as sp
from graphviz import dot


pcap = sp.rdpcap("cap1.pcap")
sessions = pcap.sessions()
hosts = set()
talks = list()
for session_name, session in sessions.items():
    for packet in session:
        ip = packet[sp.IP]
        src = ip.src
        dst = ip.dst
        hosts.add(src)
        hosts.add(dst)
        talks.append((src, dst))
print(hosts)

graph = dot.Digraph()
graph.attr(layout="circo")
for host in hosts:
    graph.node(host)
talk_counts = {}
for talk in set(talks):
    talk_counts[talk] = talks.count(talk)
print(talk_counts)
max_count = max(talk_counts.values())
max_width = 5.0
for k, v in talk_counts.items():
    talk_counts[k] = talk_counts[k] / max_count * max_width
for talk, count in talk_counts.items():
    graph.edge(talk[0], talk[1], penwidth=str(count))

graph.render('output.gv')
