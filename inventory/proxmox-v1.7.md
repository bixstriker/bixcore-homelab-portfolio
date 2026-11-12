# Proxmox Master v1.12: Project Index

These are the 40 chapters and four appendices from my current Proxmox working notes, including earlier setup work, the storage migration and newer firewall experiments.

**Updated 12 November 2026:** The lab has 18 VMs, including thirteen router/firewall instances (twelve distinct platforms), two test clients, PacketFence, OpenWISP and Taranac. OpenFW RDP forwarding was tested. The full OPNsense clone is independent at disk level but has not yet completed its IPv6-only WAN and DHCPv6-PD test. The older URL stays available for existing links.


| Section | Work | Status | Read more |
| --- | --- | --- | --- |
| 01 | Host hardware, software state and installed VM status | Observed | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| 02 | Laboratory architecture, network zones and test clients | Implemented / selected tests | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| 03 | Retain Windows while installing Debian and Proxmox | Observed | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| 04 | UEFI dual boot / one-time Windows to Proxmox BootNext | Observed | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| 05 | NICs, Linux bridges, VLAN upstream and IPv4/IPv6 | Implemented / selected tests | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| 06 | Host service stability, NetworkManager to ifupdown2 migration | Observed | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| 07 | Historical VM ZFS storage and recovery risks | Observed historically | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| 08 | MikroTik CHR installation, RouterOS and LAN/WAN provisioning | Observed selected tests | [Firewall systems tested](../docs/pages/virtual-firewall-platforms.html) |
| 09 | Guest WAN DHCP VLAN troubleshooting and evidence limits | Observed | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| 10 | Production/lab network isolation and access boundaries | Design / incomplete negative tests | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| 11 | Operating checks, reboot, restore procedures | Documented | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| 12 | Open tasks and test programme | Planned | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| 13 | Source hierarchy and deployment change log | Historical evidence | [Tracking host changes](../docs/pages/working-notes.html#changes-over-time) |
| 14 | Join Proxmox to AD, CA-issued HTTPS, IPv6 RA incident | Observed selected checks | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| 15 | KDE neon guest, remote desktop and graphics troubleshooting | Observed | [GPU and KRDP troubleshooting](../docs/pages/gpu-remote-desktop.html) |
| 16 | Windows 11 guest first installation | Historical then completed | [Firewall systems tested](../docs/pages/virtual-firewall-platforms.html) |
| 17 | CPU/BIOS VT-d upgrade preparation and constraints | Historical planning, later executed | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| 18 | Windows client completion, pfSense CE and Sophos Home guest tests | Observed selected tests | [Firewall systems tested](../docs/pages/virtual-firewall-platforms.html) |
| 19 | Follow-up checklist and temporary project debt | Historical status | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| 20 | VyOS, FortiGate VM and OpenWrt evaluation, filesystem expansion | Observed selected tests | [Firewall systems tested](../docs/pages/virtual-firewall-platforms.html) |
| 21 | Future guest OS, IPv6-only upstream, physical test AP | Planned / partially superseded | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| 22 | SMART/ZFS incident, transfer to single-disk pool and retired array | Observed | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| 23 | CPU upgrade, IOMMU verification and GPU passthrough troubleshooting | Observed | [GPU and KRDP troubleshooting](../docs/pages/gpu-remote-desktop.html) |
| 24 | KDE neon Full HD, EDID, KRDP and hardware codec validation | Observed selected behavior | [GPU and KRDP troubleshooting](../docs/pages/gpu-remote-desktop.html) |
| 25 | Actual latest October host/lab status | Observed status correction | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| 26 | IPFire WAN/LAN, bridge correction, DHCP/DNS/NAT and RDP | Observed selected tests | [Firewall systems tested](../docs/pages/virtual-firewall-platforms.html) |
| 27 | 1 November status and follow-up plan | Earlier snapshot | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| 28 | Four new VMs, lab virtual bridges and network boundaries | Verified setup / selected tests | [Firewall lab overview](../docs/pages/proxmox-firewall-lab.html) |
| 29 | NethSecurity 8.8 and FreeSense 1.1.11: DHCP, NAT and two client RDP tests | Verified selected IPv4 tests | [Firewall systems tested](../docs/pages/virtual-firewall-platforms.html) |
| 30 | DD-WRT kernel panic, compiled GRUB template, UEFI reboot and SSH blocklist | Boot and reboot repaired; poweroff open | [DD-WRT incident](../docs/pages/notes.html#ddwrt-uefi) |
| 31 | Separate OPNsense Community VM; WAN, LAN and NAT/DNAT tests | Verified selected IPv4 tests | [Firewall systems tested](../docs/pages/virtual-firewall-platforms.html) |
| 32 | Final inventory, limitations and future testing | Current status / incomplete follow-ups | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| 33 | Firewall/router version updates and checks | Selected updates verified | [Tested platforms](../docs/pages/virtual-firewall-platforms.html) |
| 34 | PhyLan1 physical test bridge, hookscript and multiple-VM disconnect | Confirmed with external laptop | [Physical LAN case study](../docs/pages/phylan1.html) |
| 35 | End-to-end checks for eleven firewall/router VMs | Internet, RDP, laptop tested; complete isolation not proven | [Lab test method](../docs/pages/lab-operational-method.html) |
| 36 | PacketFence 15.2 inline guest portal, IPSet and DNS recovery | Guest access tested; 802.1X open | [PacketFence](../docs/pages/packetfence-nac.html) |
| 37 | PacketFence PR #9350 functional backport and access-regression checks | Tested with one virtual guest | [PacketFence](../docs/pages/packetfence-nac.html) |
| 38 | IPv6-only VLAN prepared for virtual routers | Real Windows/Android client tests, router PD untested | [IPv6-only lab](../docs/pages/ipv6-only-lab.html) |
| 39 | OpenWISP, Taranac, OPNsense full clone and OpenFW | Initial service access and OpenFW RDP verified | [Proxmox guest overview](../docs/pages/proxmox-firewall-lab.html) |
| 40 | Version and maintenance status of VM100–117 (12 November) | NethSecurity 8.8.1, Taranac 1.3.4; OPNsense/client updates with exact builds not recorded | [Firewall lab update](../docs/pages/proxmox-firewall-lab.html) |
| A | Read-only diagnostics for host, router and gateway | Methods retained | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| B | Network and VM configuration examples | Private source; sanitized design | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| C | Windows-to-Proxmox one-time reboot automation | Observed method | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| D | Physical LAN hookscript (private source only; public design) | Implemented | [PhyLan1](../docs/pages/phylan1.html) |

Other cases: [FreeSense boot](../docs/pages/notes.html#freesense-boot), [DD-WRT boot](../docs/pages/notes.html#ddwrt-uefi), [DD-WRT reboot](../docs/pages/notes.html#ddwrt-reboot) and [SSH lockout](../docs/pages/notes.html#ddwrt-access).

### How the setup changed

- The installed VM numbers in the 4 November inventory replace the earlier planning numbers.
- I normally run one firewall with one or two clients, rather than all 18 VMs together.
- A previous storage arrangement was replaced by a **single-disk** ZFS pool after documented health observations. Storage migration and snapshots are not high availability or a proved external recovery plan.
- Earlier virtual graphics paths are superseded by a later passthrough/EDID/KRDP solution. The final result does not prove all remote frames are hardware-encoded.
- PacketFence's guest access works after the PR #9350 backport and the physical laptop port has been tested with eleven older router VMs. VLAN41 now works on real Wi-Fi clients, but router DHCPv6-PD, PacketFence 802.1X and full isolation tests remain open.

---
