# BiXCore network architecture

This simplified diagram shows how the main services relate. It is not a physical port map.

```mermaid
flowchart TD
    Primary[Primary internet / Vodafone] --> FW[OPNsense gateway]
    Backup[O2 LTE / Ethernet passthrough] --> FW
    FW --> IoT[Restricted IoT network]
    FW --> Trusted[Trusted network]
    FW --> Guest[Guest network]
    FW --> LabWAN[Dedicated firewall lab upstream]
    Trusted --> NAS[NAS, DNS and containers]
    Trusted --> AD[Two Active Directory controllers]
    AD --> CA[Enterprise CA and SCEP]
    Trusted --> Access[Managed switching and Wi-Fi]
    Device[Wired / Wi-Fi client] -->|EAP-TLS| Access
    Access -->|RadSec / mTLS on tested devices| Proxy[RadSecProxy on OPNsense]
    Proxy -->|Local RADIUS| AAA[FreeRADIUS on OPNsense]
    AAA -->|LDAPS authorization| AD
    CA -->|Client certificates| Device
    LabWAN --> Hypervisor[Firewall VMs in Proxmox]
    Hypervisor --> LabClients[Windows and Linux test clients]
    Remote[Remote client] -->|WireGuard| FW
```

The LTE backup is selective: Core and IoT can use the backup IPv4 path, while Guest and the IPv6-only lab are not given unrestricted LTE access. RadSec secures transport for the two UniFi APs and the tested Omada switch; it does not replace end-device EAP-TLS. The virtual firewall lab has its own upstream and client bridges. Some negative-path access tests are still open.
