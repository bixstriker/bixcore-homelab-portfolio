# The Virtual Firewall Lab

My Proxmox lab lets me work with firewall systems without replacing the OPNsense gateway I use every day. I can build a configuration, connect a Windows or Linux client, test the traffic and then move on to another platform.

## How the lab works

Proxmox runs on a reused desktop with Debian 13. I have a dedicated upstream for the test firewalls and separate Linux bridges for their LAN interfaces. The same client VMs can be attached to the firewall being tested, so I don't need a large number of machines running at the same time.

As of 6 November 2026, I have 14 VMs: eleven firewall/router systems, two test clients and a separate PacketFence NAC VM. NethSecurity 8.8, FreeSense 1.1.11, DD-WRT r66445 and a second, virtual OPNsense Community 26.7 joined the earlier MikroTik, pfSense, Sophos, VyOS, FortiGate, OpenWrt and IPFire systems. Each gets a separate virtual LAN and shares the isolated test upstream. I checked basic management, internet/NAT, DHCP and two client RDP forwards on the four newest platforms. I also checked internet, selected RDP forwarding and an external Ethernet laptop with all eleven firewall/router systems. The <a href="../docs/pages/phylan1.html">PhyLan1</a> connection works only when one firewall is running. PacketFence uses a separate isolated virtual LAN and is <a href="../docs/pages/packetfence-nac.html">documented here</a>. More consistent negative-path and performance tests are still needed.

## Problems I encountered

The VLAN path for the lab WAN caused a DHCP investigation that went all the way from the gateway to the physical switch and the virtual NIC. I also corrected an upstream bridge mistake during the IPFire setup. Those are described in the [troubleshooting notes](../docs/pages/notes.html#lab). DD-WRT later needed a UEFI boot repair involving its GRUB file, embedded binary template and reboot handling; two reboot tests succeeded, but normal shutdown remains unresolved. The [DD-WRT boot repair](../docs/pages/notes.html#ddwrt-uefi) and [SSH management lockout](../docs/pages/notes.html#ddwrt-access) have their own incident notes.

## Where I want to go next

### Commercial firewalls

I would like to test Palo Alto VM-Series, Juniper vSRX, Check Point CloudGuard and SonicWall NSv, as well as a more fully licensed FortiGate VM. Cisco Catalyst 8000V is also on the list for routing and WAN experiments. These depend on trial images and licenses being available.

[Commercial platform plans →](../docs/pages/roadmap.html)

### RADIUS, 802.1X and NAC

The real network already uses FreeRADIUS with certificate-based access. In the lab I want to test how firewall and access-control systems interact with RADIUS, and eventually integrate it with the PacketFence VM. Captive-portal guest tests are now working, but RADIUS/802.1X is still planned.

[NAC and Wi-Fi plans →](../docs/pages/roadmap.html)

### Real Wi-Fi clients

A dedicated Cudy Wi-Fi 7 access point would let me try captive portals, VLANs, EAP-TLS and guest isolation with physical devices, without changing the main Wi-Fi setup.

[Physical client tests →](../docs/pages/roadmap.html)

### IPv6-only and routing protocols

I also want a separate IPv6-only lab uplink and more routing experiments with BGP and FRR. The goal is a repeatable test, not just a successful installation.

[The common test checklist →](../docs/pages/lab-operational-method.html)

Before comparing products, I want to check unwanted access paths, management exposure, restarts and configuration recovery. A simple successful RDP port forward is a useful first test, not the end of the assessment.

[What I tested on each firewall →](../docs/pages/virtual-firewall-platforms.html)   [Physical Ethernet tests →](../docs/pages/phylan1.html)   [Full list of planned experiments →](../docs/pages/roadmap.html)

---
