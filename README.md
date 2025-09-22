# EVISION_8TH

[네트워크 패킷 캡처 프로그램]
- 파이썬의 Scapy 라이브러리 사용
- CLI 기반으로 동작
- IP, TCP, UDP, ICMP 지원

- 기능 구현:
1. 네트워크 인터페이스 선택

2. 필터 입력
-> BPF(Berkeley Packet Filter)
ex) tcp : TCP 패킷만
tcp port 80 : HTTP 트래픽만
host 192.168.0.10 : 특정 IP

3. 실시간 패킷 캡처
-> iface, filter, timeout 지정

4. 프로토콜 통계 + 그래프 출력
-> 프로토콜별 패킷 수 바 그래프
-> 초 단위 패킷 수 변화
   
5. pcap 파일 저장/불러오기

*libpcap/WinPcap 설치 필요
*pip install scapy pandas matplotlib
