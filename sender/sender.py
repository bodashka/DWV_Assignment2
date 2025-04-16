import csv
import json
import time
import requests

SERVER_URL = 'http://backend:5000/receive'

def send_packet(packet):
    try:
        response = requests.post(SERVER_URL, json=packet)
        print(f"Sent: {packet['ip']} | Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending packet: {e}")

def main():
    with open('ip_addresses.csv', newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
        reader.sort(key=lambda row: int(row['Timestamp']))
    
    start_timestamp = int(reader[0]['Timestamp']) # set the 'zero-time' as the first entry.

    for i, row in enumerate(reader):
        packet_timestamp = int(row['Timestamp'])
        delay = packet_timestamp - start_timestamp

        if i > 0:
            prev_timestamp = int(reader[i - 1]['Timestamp'])
            delay = packet_timestamp - prev_timestamp
            
        if delay > 0:
            time.sleep(delay)

        packet = {
            'ip': row['ip address'],
            'lat': float(row['Latitude']),
            'lon': float(row['Longitude']),
            'timestamp': packet_timestamp,
            'suspicious': float(row['suspicious'])
        }
        send_packet(packet)

if __name__ == '__main__':
    main()
