# The Virtual Firewall Lab

My Proxmox lab lets me work with firewall systems without replacing the OPNsense gateway I use every day. I can build a configuration, connect a Windows or Linux client, test the traffic and then move on to another platform.

## How the lab works

Proxmox runs on a reused desktop with Debian 13. I have a dedicated upstream for the test firewalls and separate Linux bridges for their LAN interfaces. The same client VMs can be attached to the firewall being tested, so I don't need a large number of machines running at the same time.

As of 12 November 2026, I have 18 VMs: thirteen firewall/router instances (twelve distinct platforms), two reusable clients, PacketFence NAC, OpenWISP and Taranac. NethSecurity 8.8.1, FreeSense 1.1.12, DD-WRT r66445 and a second, virtual OPNsense Community 26.7 joined the earlier MikroTik, pfSense, Sophos, VyOS, FortiGate, OpenWrt and IPFire systems. Each gets a separate virtual LAN and shares the isolated test upstream. I checked basic management, internet/NAT, DHCP and two client RDP forwards on the four newest platforms. I also checked internet, selected RDP forwarding and an external Ethernet laptop with all eleven firewall/router systems. The [PhyLan1 test port](../docs/pages/phylan1.html) was verified with the original eleven firewall/router VMs; OpenFW and the new OPNsense clone have not been added to that tested hookscript set. PacketFence uses a separate isolated virtual LAN and is <a href="../docs/pages/packetfence-nac.html">documented here</a>. More consistent negative-path and performance tests are still needed.

## More guests, not more claims

I added OpenWISP 26.09.2 and Taranac Community Edition for future management and AAA/NAC experiments. Taranac was subsequently updated to 1.3.4. OpenWISP's services and dashboard, and Taranac's initial web login, work. I haven't tested their deeper features.

The other two guests are OpenFW UTM Community 4.2.1 and an independent full clone of lab OPNsense. I confirmed a real RDP session through OpenFW's inbound forwarding rule. The OPNsense clone has independent disks but inherited configuration; its separate IPv6-only WAN and DHCPv6-PD still need testing.

The [IPv6-only VLAN](../docs/pages/ipv6-only-lab.html) now works with real Windows and Android Wi-Fi clients. That doesn't yet prove a virtual router can receive and route a delegated /64.

## What the 12 November update confirms

I updated the NethSecurity guest to **8.8.1** and Taranac to **1.3.4**. The Windows and KDE test clients and both virtual OPNsense guests were updated too, but I didn't record exact new build numbers for those systems. I intentionally left VyOS on Stream 2026.03. The new versions do not, by themselves, extend my earlier connectivity tests or prove delegated IPv6 prefixes are working.

## The 26 November lab checkpoint

On 17 November both virtual OPNsense guests were updated to 26.7.9_3. On 22 November I confirmed OpenFW UTM Community 4.5.1 in its WebGUI. My earlier OpenFW forwarding tests were on 4.2.1; I have not repeated its complete firewall, NAT or port-forward tests on 4.5.1.

The inventory is still 18 VMs. I updated the host to Proxmox VE 9.3.1, checked boot and storage, and verified the updated KDE guest and MikroTik RDP/internet path. IPFire was also updated, but I did not repeat its complete forwarding tests.

Taranac Community Edition 1.3.5 received two independent hotfixes. Four nginx-based images now report nginx 1.30.8, and I verified that the running TACACS+ container uses the hotfix image. All 12 containers were up. Full AAA and NAC regression testing remains open.

The earlier November version figures above are historical checkpoints rather than a list of the current installed builds. I have not changed the IPv6-only virtual-router and DHCPv6-PD test status.

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

The IPv6-only lab uplink is now in place. I still need a virtual firewall to receive its own delegated prefix; BGP and FRR remain planned. The goal is a repeatable test, not just a successful installation.

[The common test checklist →](../docs/pages/lab-operational-method.html)

Before comparing products, I want to check unwanted access paths, management exposure, restarts and configuration recovery. A simple successful RDP port forward is a useful first test, not the end of the assessment.

[What I tested on each firewall →](../docs/pages/virtual-firewall-platforms.html)   [Physical Ethernet tests →](../docs/pages/phylan1.html)   [Full list of planned experiments →](../docs/pages/roadmap.html)

---
