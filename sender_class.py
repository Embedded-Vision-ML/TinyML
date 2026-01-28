
import socket
import time
import random

class CommandTransmission():
    def __init__(self):
        # Storing the IP addresses in a dict so that addressing is in constant time
        self.esp_id = { 1: "10.42.0.50" }
        self.ESP32_PORT = 4210
        self.connections = {}        


    def send_data(self, id, data):
        ip_address = self.esp_id[id]
        
        if isinstance(data, (list, tuple)):
            # Convert the message to a list of uint8 values
            message = bytes(data)
        else:
            message = data if isinstance(data, bytes) else f"{data}".encode('utf-8')

        # Reuse connection if exists, otherwise create new one
        if id not in self.connections:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip_address, self.ESP32_PORT))
            self.connections[id] = sock

        try:
            self.connections[id].sendall(message)
            print(f"Successfully sent {len(message)} bytes")
        except socket.error as e:
            print(f"Send failed: {e}")

            # Remove the failed send from connections
            if id in self.connections:
                self.connections[id].close()
                del self.connections[id]


    def close(self):
        for sock in self.connections.values():
            sock.close()


if __name__=="__main__":
    data_obj = CommandTransmission()
    data_obj.send_data(1, "Test data")
    data_obj.close()
    