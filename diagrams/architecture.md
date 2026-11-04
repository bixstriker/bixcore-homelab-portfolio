# BiXCore network architecture

This simplified diagram shows how the main services relate. It is not a physical port map.

```mermaid
flowchart TD
    Internet[Internet / ISP] --> FW[OPNsense gateway]
    FW --> Trusted[Trusted network]
    FW --> Guest[Guest network]
    FW --> LabWAN[Dedicated firewall lab upstream]
    Trusted --> NAS[NAS, DNS and containers]
    Trusted --> AD[Two Active Directory controllers]
    AD --> CA[Enterprise CA and SCEP]
    Trusted --> Access[Managed switching and Wi-Fi]
    Device[Wired / Wi-Fi client] -->|EAP-TLS| Access
    Access -->|RADIUS| AAA[FreeRADIUS on OPNsense]
    AAA -->|LDAPS authorization| AD
    CA -->|Client certificates| Device
    LabWAN --> Hypervisor[Firewall VMs in Proxmox]
    Hypervisor --> LabClients[Windows and Linux test clients]
    Remote[Remote client] -->|WireGuard| FW
```

The virtual firewall lab has its own upstream and client bridges. Some negative-path access tests are still open.
