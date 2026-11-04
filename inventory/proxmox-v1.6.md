# Proxmox: Project Index

These are the main tasks and experiments from building the Proxmox lab. Earlier installation notes are included alongside the later storage migration, firewall tests and GPU work.

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
| 27 | Actual November status and follow-up plan | Current as of source date | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| A | Read-only diagnostics for host, router and gateway | Methods retained | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| B | Network and VM configuration examples | Private source; sanitized design | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| C | Windows-to-Proxmox one-time reboot automation | Observed method | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |

### How the setup changed

- The source's **November 1 latest state** overrides earlier ideas about which VM number would be allocated to which firewall distribution.
- The VMware-class test inventory is not a list of concurrently running guests.
- A previous storage arrangement was replaced by a **single-disk** ZFS pool after documented health observations. Storage migration and snapshots are not high availability or a proved external recovery plan.
- Earlier virtual graphics paths are superseded by a later passthrough/EDID/KRDP solution. The final result does not prove all remote frames are hardware-encoded.
- Additional IPv6-only upstreams, physical test AP clients and broad performance comparisons are **planned**, not installed/finished merely because the source describes their intended architecture.

---
