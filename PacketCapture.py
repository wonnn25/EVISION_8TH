import sys
import time
from scapy.all import sniff, wrpcap, rdpcap, get_if_list, IP, TCP, UDP, ICMP
import pandas as pd
import matplotlib.pyplot as plt

protocol_map = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
packet_list = []
stats = {"TCP": 0, "UDP": 0, "ICMP": 0, "Others": 0}

def choose_interface():
    interfaces = get_if_list()
    print("\n[+] Available Interfaces")
    for idx, iface in enumerate(interfaces):
        print(f"  [{idx}] {iface}")
    choice = int(input("Select interface index: "))
    return interfaces[choice]

def show_packet(pkt):
    if IP in pkt:
        proto_num = pkt[IP].proto
        proto_name = protocol_map.get(proto_num, "Others")
        stats[proto_name] = stats.get(proto_name, 0) + 1

        src, dst = pkt[IP].src, pkt[IP].dst
        length = pkt[IP].len
        info = {"time": time.time(), "proto": proto_name,
                "src": src, "dst": dst, "len": length}
        packet_list.append(info)

        print(f"[{len(packet_list)}] {proto_name}: {src} → {dst} (len={length})")

def start_sniff(iface, flt, duration):
    print(f"\n[+] Sniffing on {iface} for {duration}s ...")
    packets = sniff(iface=iface, filter=flt, timeout=duration, prn=show_packet)
    return packets

def save_pcap(packets):
    fname = input("Save as (ex: capture.pcap): ")
    wrpcap(fname, packets)
    print(f"[+] Saved to {fname}")

def load_pcap():
    fname = input("Open pcap file: ")
    packets = rdpcap(fname)
    for pkt in packets:
        show_packet(pkt)
    print(f"[+] Loaded {len(packets)} packets from {fname}")

def visualize():
    df = pd.DataFrame(packet_list)
    if df.empty:
        print("[-] No packets captured.")
        return
    # 프로토콜 비율
    df['proto'].value_counts().plot(kind='bar', color='skyblue', title="Protocol Distribution")
    plt.xlabel("Protocol")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()
    # 시간별 패킷 수
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time').resample('1s').size().plot(title="Traffic over Time")
    plt.ylabel("Packets/sec")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("=== Python Packet Sniffer ===")
    mode = input("[C]apture / [L]oad pcap ? ").strip().lower()

    if mode.startswith('c'):
        iface = choose_interface()
        flt = input("BPF Filter (ex: tcp port 80 or leave empty): ").strip()
        duration = int(input("Capture duration (seconds): "))
        packets = start_sniff(iface, flt, duration)
        save_pcap(packets)
    else:
        load_pcap()

    print("\n[+] Protocol Stats:", stats)
    visualize()