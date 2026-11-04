# OPNsense, WireGuard and IPv6

OPNsense is the centre of my network. Most days it quietly handles routing, firewall rules, VPN access and DNS. The interesting work starts when something behaves differently after a reboot or when IPv6 takes a different path from IPv4.

## The network behind it

The gateway is an Intel N305 appliance with 10GbE interfaces. I use separate network segments for everyday clients, guests, managed devices and the Proxmox test environment. Suricata and Zenarmor inspect selected traffic, while FreeRADIUS works with the certificate infrastructure for supported wired and Wi-Fi devices.

I have also set up policy routing, a commercial VPN connection for particular traffic, WireGuard for remote access, and dynamic DNS and certificate renewal for services that need them.

## What I tested

- **Firewall policy:** selected access paths between network segments were checked from clients, not just in the rule editor.
- **Suricata and Zenarmor:** a controlled IPS test produced a blocked event; a separate restricted-category request was denied by the configured Zenarmor policy.
- **WireGuard:** I tested a mobile client with IPv4 and IPv6 routed through home, including DNS and access to permitted internal services. Other clients can keep split-tunnel profiles.
- **IPv6 NPTv6:** I moved away from a static translation that could not follow changes to the upstream prefix. The new rule tracks the delegated prefix, and I checked the effective rule and the IPv6 address reported by the test client.
- **WAN source selection:** when the ISP's SLAAC address stopped working as an outbound source, I compared it with the DHCPv6 address and added a recovery path for the observed failure.

## Problems worth keeping notes about

The [invalid PF route-to states](../docs/pages/notes.html#pf-state) after a reboot were different from the [WAN IPv6 source-address problem](../docs/pages/notes.html#ipv6). A [dynamic DNS failure](../docs/pages/notes.html#ddns) turned out to depend on the same IPv6 connectivity issue, and the [WireGuard full-tunnel setup](../docs/pages/notes.html#wireguard) needed its own prefix-translation solution. I keep them as separate investigations rather than one generic “IPv6 problem”.

## Next checks

I still want to observe the NPTv6 setup during a real ISP prefix change, repeat the new behavior after a complete reboot and work through the remaining negative-path tests between network segments. The [Zenarmor multi-core comparison](../docs/pages/zenarmor.html) is planned separately; the 10GbE links are not an inspection-throughput measurement.

[Read the troubleshooting notes →](../docs/pages/notes.html)   [Updates and gateway operations →](../docs/pages/security-operations.html)   [DNS and guest services →](../docs/pages/network-services.html)

---
