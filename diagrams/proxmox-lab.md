# Proxmox lab — firewall VMs and NAC

```mermaid
flowchart TD
    Main[Main OPNsense gateway] -->|Restricted lab upstream VLAN| WAN[Test WAN bridge]
    PVE[Proxmox host] --- Mgmt[Separate management bridge]
    WAN --> FW[One selected firewall / router VM]
    FW --> LAN[Its existing virtual LAN]
    LAN --> Guests[Windows or KDE test clients]
    Laptop[External Ethernet laptop] --- Phy[Dedicated physical bridge]
    Phy -.->|Only when exactly one firewall VM runs| LAN
    WAN --> NAC[PacketFence NAC VM]
    NAC --> Inline[Separate isolated inline LAN]
    Inline --> Win[Windows VM for NAC guest tests]
```

I have **14 VMs**: 11 firewall/router platforms, two reusable clients and one PacketFence NAC VM. The external laptop was tested across all eleven firewall platforms, using a Proxmox host hookscript to connect it to the active guest LAN. The physical port disconnects if two or more firewall VMs are running.

PacketFence is a separate virtual NAC test; it does **not** use that physical port. Captive-portal registration and guest access revocation work in the VM test, while RADIUS/802.1X and physical PacketFence clients remain untested. The full lab-to-core isolation matrix and independent VM backups are also open.
