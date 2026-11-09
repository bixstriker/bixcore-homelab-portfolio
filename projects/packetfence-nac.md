# PacketFence: My First NAC Lab

**Tested 6 November 2026:** PacketFence 15.2 on Debian 12, in an isolated Proxmox VM.

I installed PacketFence because I wanted to see what happens when a guest registers through a captive portal and later loses network access. My Windows test VM got DHCP and reached the portal, but initially couldn't browse the web even after registering.

## Two different problems

**IPSet:** PacketFence's rule generator passed an IP/MAC pair to an IP-only set. The resulting rule failed to load, so the guest could not access the outside network. I traced the rule with Codex and used a small local hotfix without adding any bypass rule. This corresponds to [upstream issue #9339](https://github.com/inverse-inc/packetfence/issues/9339). I have not verified an upstream fix in the installed package.

**DNS:** Once IPSet worked, normal web names still resolved to the portal. PacketFence was forwarding queries to its own DNS listener. I changed the upstream to the lab gateway while keeping PacketFence as the DNS server assigned to clients.

## From my temporary fix to upstream PR #9350

On 9 November I returned to the IPSet code and applied a functional backport of [merged upstream PR #9350](https://github.com/inverse-inc/packetfence/pull/9350) to the installed 15.2.0 module. I checked the candidate against the upstream change, verified Perl syntax, kept a rollback copy and restarted only the affected service.

I checked both registered and guest IPSet membership, then revoked registration and watched outside access fail and the portal reappear. Re-registering restored access. After a normal reboot the main PacketFence services were active, membership was present and HTTPS worked again without re-registering.

This is a locally applied backport, **not** an official updated package. A later upgrade could replace it. I have not validated RADIUS/802.1X, Security Events, spoofing resistance or a physical NAC client.

## Results and limits

- Guest registered: external TCP/443 and HTTPS worked with normal TLS validation.
- Registration revoked: new outside connections failed and the portal appeared.
- Registration repeated: access returned without manual IPSet changes.
- After reboot: DHCP, DNS and IPSet services were active, membership was present, and DNS/HTTPS worked again.

The admin listener became active after reboot, but a fresh browser login wasn't recorded. I repeated the full revoke/register cycle after the backport, but not again after that reboot.

This is a **virtual guest-registration test**, not an 802.1X or physical-device NAC deployment. RADIUS/EAP-TLS, dynamic VLANs, physical clients, checking the next official release for this upstream fix and independent backups remain open.

[Read the project](../docs/pages/packetfence-nac.html) · [IPSet problem](../docs/pages/notes.html#packetfence-ipset) · [DNS problem](../docs/pages/notes.html#packetfence-dns)
