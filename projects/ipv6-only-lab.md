# Building an IPv6-only Network That Can Still Reach IPv4

**Tested:** 9 November 2026 · **Gateway:** OPNsense · **Clients:** Windows and Android over Wi-Fi 7  
[Read the public project page](../docs/pages/ipv6-only-lab.html)

I wanted a real IPv6-only test network rather than a demonstration on a single computer. I put a separate VLAN through three managed switches, both UniFi test access points and the Proxmox uplink. The production enterprise Wi-Fi and everyday Core/Guest networks were left in place.

## What I implemented

- A dedicated OPNsense VLAN interface with no routable IPv4 configuration, dynamic global IPv6 addressing and a local ULA prefix.
- Router Advertisements in Assisted mode with global and local on-link IPv6 prefixes.
- Kea DHCPv6 with a working stateful address for Windows and a reserved pool for future delegated /64 prefixes.
- DNS64 and Tayga NAT64 so IPv6-only clients can reach IPv4-only websites.
- Tagged VLAN delivery across three switches, two Wi-Fi 7 access points and the Proxmox lab uplink.

## Actual client results

The Windows test laptop received the expected IPv6 configuration, passed native IPv6 and NAT64 checks, and opened IPv4-only websites. Android used SLAAC for its global IPv6 address and reached both types of site without receiving a stateful DHCPv6 address. I also tested a permitted Core-to-laptop connection and RDP, after adding a narrowly scoped local Windows Firewall allowance.

## Tests that remain open

The configured Kea prefix-delegation pool has **not** yet been used successfully by a virtual router. The OPNsense clone intended for that experiment has not been proved connected to the IPv6-only WAN. Full LAB-to-Core and Guest-to-LAB negative-path tests are open.

A temporary inbound-IPv6 test option exists but is **disabled by default**, with no successful external inbound test. The final runtime order of its WAN rules was not provided. ISP prefix renumbering has not been exercised; aliases and clients may need intervention when it happens.

This is a personal lab write-up, not a configuration export. It contains no current external IPv6 prefix, local IP addresses, exact switch ports, credentials or deployable firewall rule set.

[Main gateway notes](../docs/pages/opnsense-ipv6.html) · [Proxmox lab](../docs/pages/proxmox-firewall-lab.html) · [Future tests](../docs/pages/roadmap.html)
