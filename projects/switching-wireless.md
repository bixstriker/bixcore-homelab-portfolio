# Switching, Wi-Fi and 802.1X

The switching and Wi-Fi side of BiXCore has been a good place to learn how the same network looks from three different directions: the client, the access point or switch, and the RADIUS server.

## Switches and VLANs

I use managed Omada and Grandstream switches to separate client, guest, infrastructure and lab traffic. I checked tagged and untagged VLAN membership, port PVIDs and trunk behavior in the actual switch interfaces. Exported configuration data helped with cross-checking, but it did not replace looking at the live settings.

The switches also gave me a chance to examine vendor-specific configuration formats and compare two devices without assuming their ports had identical roles.

## Enterprise Wi-Fi and network access

The Wi-Fi setup uses managed UniFi access points and a locally hosted controller. For supported clients, access is authenticated using EAP-TLS certificates through FreeRADIUS rather than a shared password. Wired 802.1X adds another layer: devices such as domain controllers need careful handling so that network authentication doesn't depend on services they can't reach yet.

I also investigated what could be learned from the controller backup format. Those investigations helped me understand the stored WLAN settings, but the running controller and actual client connections remain the more useful checks.

## UniFi session Accounting and Disconnect

I used the existing FreeRADIUS database to track sessions from both UniFi access points. A Disconnect test initially failed with a stale session ID after roaming. Using the active session produced an ACK, and the phone left Wi-Fi and authenticated again using EAP-TLS. I still haven't verified a live VLAN reassignment through CoA.

[The session-ID investigation →](../docs/pages/notes.html#radius-coa) · [IPv6-only test Wi-Fi →](../docs/pages/ipv6-only-lab.html)

## Three investigations I keep separate

### IPv6 Neighbor Discovery

One Windows domain controller had IPv6 addresses that resolved in DNS but could not be reached. The switch-side ND inspection behavior was part of the problem. Specific neighbor bindings restored the tested connections.

[How I diagnosed it →](../docs/pages/notes.html#omada-nd)

### LLDP after configuration changes

Neighbor discovery worked, but I also wanted the correct management address to be advertised after startup and configuration regeneration. That required a persistent startup setting.

[The LLDP fix →](../docs/pages/notes.html#lldp)

### Wired certificate authentication

Bringing infrastructure devices and domain controllers onto 802.1X required a different authorization path from ordinary workstations. I tested the final behavior against the switch and FreeRADIUS.

[The EAP-TLS bootstrap issue →](../docs/pages/notes.html#dc-eap)

## What I still want to check

The physical cabling inventory is not finished, and some IPv6 neighbor bindings still need a complete restart and prefix-change test. I'd also like to use a dedicated Wi-Fi access point with the Proxmox lab for separate captive-portal and NAC experiments.

[Certificate-based network access →](../docs/pages/identity-pki.html)   [Upcoming Wi-Fi tests →](../docs/pages/roadmap.html)

---
