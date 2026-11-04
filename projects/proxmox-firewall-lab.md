# The Virtual Firewall Lab

My Proxmox lab lets me work with firewall systems without replacing the OPNsense gateway I use every day. I can build a configuration, connect a Windows or Linux client, test the traffic and then move on to another platform.

## How the lab works

Proxmox runs on a reused desktop with Debian 13. I have a dedicated upstream for the test firewalls and separate Linux bridges for their LAN interfaces. The same client VMs can be attached to the firewall being tested, so I don't need a large number of machines running at the same time.

In the first round I installed and tried MikroTik CHR, pfSense CE, Sophos Firewall Home, VyOS, FortiGate VM, OpenWrt and IPFire. The tests covered boot and management, DHCP, DNS, outbound NAT and selected port forwards to a Windows or Linux client. I haven't yet put every product through an identical security and performance test suite.

## Problems I encountered

The VLAN path for the lab WAN caused a DHCP investigation that went all the way from the gateway to the physical switch and the virtual NIC. I also corrected an upstream bridge mistake during the IPFire setup. Both are described in the [troubleshooting notes](../docs/pages/notes.html#lab).

## Where I want to go next

### Commercial firewalls

I would like to test Palo Alto VM-Series, Juniper vSRX, Check Point CloudGuard and SonicWall NSv, as well as a more fully licensed FortiGate VM. Cisco Catalyst 8000V is also on the list for routing and WAN experiments. These depend on trial images and licenses being available.

[Commercial platform plans →](../docs/pages/roadmap.html)

### RADIUS, 802.1X and NAC

The real network already uses FreeRADIUS with certificate-based access. In the lab I want to test how firewall and access-control systems interact with RADIUS, then try PacketFence as a separate NAC project.

[NAC and Wi-Fi plans →](../docs/pages/roadmap.html)

### Real Wi-Fi clients

A dedicated Cudy Wi-Fi 7 access point would let me try captive portals, VLANs, EAP-TLS and guest isolation with physical devices, without changing the main Wi-Fi setup.

[Physical client tests →](../docs/pages/roadmap.html)

### IPv6-only and routing protocols

I also want a separate IPv6-only lab uplink and more routing experiments with BGP and FRR. The goal is a repeatable test, not just a successful installation.

[The common test checklist →](../docs/pages/lab-operational-method.html)

Before comparing products, I want to check unwanted access paths, management exposure, restarts and configuration recovery. A simple successful RDP port forward is a useful first test, not the end of the assessment.

[What I tested on each firewall →](../docs/pages/virtual-firewall-platforms.html)   [Full list of planned experiments →](../docs/pages/roadmap.html)

---
