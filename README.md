# BiXCore Homelab

I built BiXCore as a personal network and security lab. It lets me explore OPNsense, Windows Server and PKI, enterprise Wi-Fi, Linux clients and virtual firewall platforms — and work through the problems that appear along the way.

**[Open the website](docs/index.html)** · [Hardware](docs/pages/hardware.html) · [Projects](docs/pages/work-index.html) · [Troubleshooting](docs/pages/notes.html) · [Plans](docs/pages/roadmap.html) · [About me](docs/pages/about.html)

## What I've worked on

- **Routing and firewalls:** OPNsense, IPv6, WireGuard, VLANs, Suricata and Zenarmor, including a [working IPv6-only VLAN](projects/ipv6-only-lab.md) with DNS64/NAT64.
- **Identity and certificates:** Active Directory, AD CS, NDES/SCEP, FreeRADIUS and EAP-TLS on Windows, Kubuntu and Android.
- **Infrastructure:** Managed switches and enterprise Wi-Fi, NAS services, Docker networking, monitoring and backups.
- **Virtualization:** Proxmox, single-disk ZFS recovery, GPU passthrough, and 14 VMs: 11 firewall/router platforms, two Windows/Linux clients and a separate PacketFence NAC guest.
- **NAC and physical lab clients:** [PacketFence](projects/packetfence-nac.md) guest access and [PhyLan1](projects/phylan1.md), a physical laptop linked to the selected firewall VM.
- **Software and switch tooling:** [BiX Barox Config Tool](projects/barox-config-tool.md), an offline CLI conversion and switch-comparison project with a Windows GUI and ongoing serial-console research.

The [Proxmox v1.9 index](inventory/proxmox-v1.7.md) covers all 36 chapters of my working documentation, including physical client testing and PacketFence. Its older URL is retained for existing links. The site contains 31 troubleshooting cases, including a recent DD-WRT UEFI boot repair and an SSH management lockout. I have also kept [project articles](projects/), [diagrams](diagrams/) and [working-note indexes](inventory/) for people who prefer reading in GitHub.

## Where my networking experience started

My professional background is in electronic security systems, including video surveillance, access control and fire detection. Networking is part of that work: I integrate surveillance systems with Active Directory, configure switches, routers, firewalls and GSM modems, and troubleshoot IP connectivity between Axis cameras and video servers. BiXCore is where I take those interests further and test them independently.

## Another personal project

I also wrote a science-fiction story, **Seele der KI**, and built an [interactive book website](https://bixcore.de/) for it, with German, Russian and Ukrainian editions. If you read it, I'd be happy to hear your thoughts.

## What I want to explore next

I have plans for more commercial firewall platforms, PacketFence and RADIUS integration, an IPv6-only test network, physical Wi-Fi clients, more Zenarmor filtering and TLS inspection experiments, and recovery testing. See the [roadmap](docs/pages/roadmap.html) for the full list.

## About this repository

This is a snapshot of my portfolio website and its public project notes. The website is plain HTML and CSS and has no analytics or external JavaScript. I keep device configurations, operational backups and detailed working logs outside the portfolio.

The public website is hosted through GitHub Pages from `docs/` at **https://lab.bixcore.de/**. Project notes are updated as experiments are verified.
