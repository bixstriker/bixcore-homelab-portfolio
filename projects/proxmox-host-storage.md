# Building the Proxmox Host

I wanted a proper firewall lab but didn't want to dedicate another powerful computer to it full-time. The solution was to reuse an older desktop, keep Windows available and boot into Proxmox whenever I needed to test something.

## Windows and Proxmox on the same PC

I installed Debian 13 and Proxmox VE 9.2 alongside the existing Windows 11 setup. Windows remains the normal boot choice; when I need the lab, a one-time UEFI BootNext request starts Proxmox instead. I tested the switch without attaching a keyboard or monitor.

I later upgraded the CPU to an Intel Core i7-4790K and confirmed that VT-d/IOMMU was active on the running host. I also changed the Linux network configuration from the desktop-oriented NetworkManager setup to ifupdown2, which works better with Proxmox bridges.

## Host networking and directory integration

The host's management network and the virtual firewalls' upstream traffic have different roles. Each firewall also gets its own virtual LAN for Windows and Linux test clients. That makes it possible to move a client between firewall systems without changing the everyday home gateway.

I joined the Proxmox host to Active Directory with realmd and SSSD and installed a trusted management HTTPS certificate from the internal CA. IPv6 on the management bridge took extra work: I had to adjust how Linux handled Router Advertisements when forwarding and bridges were enabled.

An early VLAN/DHCP problem needed checks on the physical switch, the tagged uplink, the Proxmox bridge and the guest NIC, not just changes inside the virtual router. [I kept the troubleshooting sequence](../docs/pages/notes.html#lab) for later firewall builds.

## Replacing the VM storage

The first VM pool used two older HDDs without disk redundancy. After checking SMART and ZFS health, I decided to move the VM data to a replacement disk rather than keep using the unhealthy arrangement.

I migrated the ZFS data, updated the Proxmox storage references, started the existing guests again and retired the old pool. The current setup uses a single 2 TB ZFS disk. It is suitable for an on-demand lab, but a disk failure would still require recovery from a separate backup.

## What I want to improve

The remaining work is practical: an off-host restore test, more reboot and IPv6 checks, and a complete test of the network paths that should be blocked. I normally run only two or three VMs at a time, so I'm prioritizing reliability and low operating cost over building a permanent cluster.

[The storage incident →](../docs/pages/notes.html#zfs)   [Firewall systems I've tried →](../docs/pages/virtual-firewall-platforms.html)   [GPU passthrough →](../docs/pages/gpu-remote-desktop.html)

---
