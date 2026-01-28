#include <WiFi.h>
#include <WiFiServer.h>
#include <wifi_credentials.h>

////////////
// GLOBAL //
////////////

// Hotspot credentials
const char* ssid = WIFI_SSID;
const char* password = WIFI_PASSWORD;

// Manually set IP address
IPAddress local_IP(10, 42, 0, 30);   // Choose something outside DHCP range (e.g., .50)
IPAddress gateway(10, 42, 0, 1);     // Usually the hotspot IP
IPAddress subnet(255, 255, 255, 0);      // Standard subnet mask


// ---- TCP settings ----
WiFiServer server(4210);
WiFiClient client;

const int ARRAY_SIZE = 9216;
uint8_t imageBuffer[ARRAY_SIZE];


///////////
// SETUP //
///////////

void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.println("Configuring static IP...");
    if (!WiFi.config(local_IP, gateway, subnet)) {
        Serial.println("Failed to configure static IP");
    }

    // Connect to WiFi
    Serial.print("Connecting to WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi!");
    Serial.print("ESP32 IP address: ");
    Serial.println(WiFi.localIP());

    // Start TCP server
    server.begin();
    Serial.print("TCP server listening on port 4210");
}


////////////////
// MAIN LOOP //
///////////////

void loop() {
    // If a client exists, make sure that its connected
    if (server.hasClient()) {
        if (!client.connected()) {
            client = server.available();
            Serial.print("New client connected from ");
            Serial.println(client.remoteIP());
        }
    }

    if (client.connected() && client.available()) {
        static int bytesReceived = 0;

        // Keep reading until the image is fully sent
        while (client.available() && bytesReceived < ARRAY_SIZE) {
            imageBuffer[bytesReceived] = client.read();
            bytesReceived++;
        }

        // Check if the image has been transmitted successfully
        if (bytesReceived == ARRAY_SIZE) {
            Serial.print("Received complete array of ");
            Serial.print(ARRAY_SIZE);
            Serial.println(" bytes");
            
            // Print first 20 bytes as example
            Serial.print("First 20 bytes: ");
            for (int i = 0; i < 20; i++) {
                Serial.print(imageBuffer[i], HEX);
                Serial.print(" ");
            }
            Serial.println();

            // Echo back confirmation
            client.print("Array received successfully!");
            
            // Reset for next array
            bytesReceived = 0;
        }
    }

    // Check if client disconnected
    if (!client.connected()) {
        if (client) {
            client.stop();
            Serial.println("Client disconnected");
        }
    }

    delay(10); // small delay to prevent spamming Serial
}
