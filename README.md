# BiXCore Homelab

I built BiXCore as a personal network and security lab. It lets me explore OPNsense, Windows Server and PKI, enterprise Wi-Fi, Linux clients and virtual firewall platforms — and work through the problems that appear along the way.

**[Open the website](docs/index.html)** · [Hardware](docs/pages/hardware.html) · [Projects](docs/pages/work-index.html) · [Troubleshooting](docs/pages/notes.html) · [Plans](docs/pages/roadmap.html) · [About me](docs/pages/about.html)

## What I've worked on

- **Routing and firewalls:** OPNsense, IPv6, WireGuard, VLANs, Suricata and Zenarmor, including a [working IPv6-only VLAN](projects/ipv6-only-lab.md) with DNS64/NAT64, [physical WAN failover and recovery](projects/wan-failover-recovery.md), and a [controlled TLS inspection pilot](projects/zenarmor.md).
- **Identity and certificates:** Active Directory, AD CS, NDES/SCEP, FreeRADIUS and EAP-TLS on Windows, Kubuntu and Android, including tested UniFi RADIUS Accounting, strict EAP-TLS checks, the [RadSec migration](projects/radsec-mtls.md) and my [RADIUS Control](projects/radius-control.md) tool. The interface remains v1.0.1; source and restricted UniFi helpers reached v1.0.2 with tested post-RadSec controls.
- **Infrastructure:** Managed switches and enterprise Wi-Fi, [TACACS+ administration over AD/LDAPS](projects/tacacs-switch-aaa.md), NAS services, Docker networking, switch-event notifications, monitoring and backups. I tested different local-login fallback behavior on Omada and Barox.
- **Virtualization:** Proxmox, single-disk ZFS recovery, GPU passthrough, and 18 VMs: 13 router/firewall instances (12 distinct platforms), two Windows/Linux clients, and PacketFence, OpenWISP and Taranac service VMs.
- **NAC and physical lab clients:** [PacketFence](projects/packetfence-nac.md) guest access with a locally backported upstream fix, and [PhyLan1](projects/phylan1.md), tested against the original eleven firewall VMs.
- **Software and switch tooling:** [BiX Barox Config Tool](projects/barox-config-tool.md), an offline CLI conversion and switch-comparison project with a Windows GUI and ongoing serial-console research.

The [Proxmox v1.15 index](inventory/proxmox-v1.7.md) covers all 43 chapters of my working documentation, including physical client testing and PacketFence. Its older URL is retained for existing links. The site contains 43 troubleshooting cases, including Omada certificate validation, UniFi DAS after RadSec, stale PF states after boot, NAS source-route selection and the Zenarmor Netmap and TLS inspection investigations. I have also kept [project articles](projects/), [diagrams](diagrams/) and [working-note indexes](inventory/) for people who prefer reading in GitHub.

## Where my networking experience started

My professional background is in electronic security systems, including video surveillance, access control and fire detection. Networking is part of that work: I integrate surveillance systems with Active Directory, configure switches, routers, firewalls and GSM modems, and troubleshoot IP connectivity between Axis cameras and video servers. BiXCore is where I take those interests further and test them independently.

## Another personal project

I also wrote a science-fiction story, **Seele der KI**, and built an [interactive book website](https://bixcore.de/) for it, with German, Russian and Ukrainian editions. If you read it, I'd be happy to hear your thoughts.

## What I want to explore next

I want to extend PacketFence into wired and Wi-Fi NAC tests, try DHCPv6 prefix delegation from the working IPv6-only lab to a virtual router, add a dedicated isolated test access point, explore commercial firewalls, and investigate the remaining TLS DNS-enrichment issue, backup restoration and inspection performance once the engine stability problem is resolved. See the [roadmap](docs/pages/roadmap.html) for the full list.

## About this repository

This is a snapshot of my portfolio website and its public project notes. The website is plain HTML and CSS and has no analytics or external JavaScript. I keep device configurations, operational backups and detailed working logs outside the portfolio.

The public website is hosted through GitHub Pages from `docs/` at **https://lab.bixcore.de/**. Project notes are updated as experiments are verified.
