# PacketFence: My First NAC Lab

**Tested 6 November 2026:** PacketFence 15.2 on Debian 12, in an isolated Proxmox VM.

I installed PacketFence because I wanted to see what happens when a guest registers through a captive portal and later loses network access. My Windows test VM got DHCP and reached the portal, but initially couldn't browse the web even after registering.

## Two different problems

**IPSet:** PacketFence's rule generator passed an IP/MAC pair to an IP-only set. The resulting rule failed to load, so the guest could not access the outside network. I traced the rule with Codex and used a small local hotfix without adding any bypass rule. This corresponds to [upstream issue #9339](https://github.com/inverse-inc/packetfence/issues/9339). I have not verified an upstream fix in the installed package.

**DNS:** Once IPSet worked, normal web names still resolved to the portal. PacketFence was forwarding queries to its own DNS listener. I changed the upstream to the lab gateway while keeping PacketFence as the DNS server assigned to clients.

## Results and limits

- Guest registered: external TCP/443 and HTTPS worked with normal TLS validation.
- Registration revoked: new outside connections failed and the portal appeared.
- Registration repeated: access returned without manual IPSet changes.
- After reboot: DHCP, DNS and IPSet services were active, membership was present, and DNS/HTTPS worked again.

The admin listener became active after reboot, but a fresh browser login wasn't recorded. I also didn't repeat the full revoke/register cycle after that reboot.

This is a **virtual guest-registration test**, not an 802.1X or physical-device NAC deployment. RADIUS/EAP-TLS, dynamic VLANs, physical clients, an upstream patch comparison and independent backups remain open.

[Read the project](../docs/pages/packetfence-nac.html) · [IPSet problem](../docs/pages/notes.html#packetfence-ipset) · [DNS problem](../docs/pages/notes.html#packetfence-dns)
