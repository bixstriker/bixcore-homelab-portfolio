# Switching, Wi-Fi and 802.1X

The switching and Wi-Fi side of BiXCore has been a good place to learn how the same network looks from three different directions: the client, the access point or switch, and the RADIUS server.

## Switches and VLANs

I use managed Omada and Grandstream switches to separate client, guest, infrastructure and lab traffic. I checked tagged and untagged VLAN membership, port PVIDs and trunk behavior in the actual switch interfaces. Exported configuration data helped with cross-checking, but it did not replace looking at the live settings.

The switches also gave me a chance to examine vendor-specific configuration formats and compare two devices without assuming their ports had identical roles.

## Centralized switch administration with TACACS+

I added TACACS+ authentication through AD/LDAPS for the managed Omada and Barox switches, with separate administrative and restricted roles. The most valuable result came from testing failure behavior: Barox accepted a local recovery account when the server was offline; Omada did not fall back as expected despite accepting the same local account in explicit local mode. I documented the packet captures and reported the reproducible problem to the vendor without assuming a firmware root cause.

[The TACACS+ switch project →](../docs/pages/tacacs-switch-aaa.html)

## Enterprise Wi-Fi and network access

The Wi-Fi setup uses managed UniFi access points and a locally hosted controller. For supported clients, access is authenticated using EAP-TLS certificates through FreeRADIUS rather than a shared password. Wired 802.1X adds another layer: devices such as domain controllers need careful handling so that network authentication doesn't depend on services they can't reach yet.

I also investigated what could be learned from the controller backup format. Those investigations helped me understand the stored WLAN settings, but the running controller and actual client connections remain the more useful checks.

## Securing RADIUS between the APs, switch and gateway

I migrated both UniFi APs and my wired Omada switch to **RadSec over TLS 1.3**. The client login is still EAP-TLS inside FreeRADIUS; RadSec protects and authenticates the network device's transport to the server.

Omada rejected experimental internal server certificates with verification enabled, even when OpenSSL checks passed elsewhere. I used a trusted Let's Encrypt server chain while keeping the original separate RadSec client CA on the gateway. With verification still enabled, Omada authenticated successfully and sent Accounting. I also verified both UniFi APs over TLS 1.3.

After the migration I updated the restricted UniFi session-control helpers, not the APs' whole configuration or the NAS web image. [The RadSec implementation →](../docs/pages/radsec-mtls.html)

## UniFi session Accounting and Disconnect

I used the existing FreeRADIUS database to track sessions from both UniFi access points. A Disconnect test initially failed with a stale session ID after roaming. Using the active session produced an ACK, and the phone left Wi-Fi and authenticated again using EAP-TLS. I later tried a live VLAN change through CoA, but the tested UniFi firmware returned an Unsupported-Attribute NAK.

[The session-ID investigation →](../docs/pages/notes.html#radius-coa) · [IPv6-only test Wi-Fi →](../docs/pages/ipv6-only-lab.html)

## Adding wired Disconnect to Omada

My RADIUS Control tool now handles eligible individual wired 802.1X sessions on the configured Omada switch. The first request returned a NAK; after narrowing the packet to the supported attributes, Omada sent a verified Disconnect-ACK.

The switch didn't always send an Accounting-Stop, though, and a replacement Accounting-Start arrived after my original timeout. I now wait for a unique successor session on the same port and client before closing an unchanged old record. I tested the resulting behavior on **two physical ports**, with a workstation and a domain controller. Unknown outcomes are not automatically retried.

[The Accounting investigation →](../docs/pages/notes.html#omada-accounting) · [RADIUS Control →](../docs/pages/radius-control.html)

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

## Getting notified when a switch link changes

I wanted a link failure to produce an actual event, rather than waiting for my dashboard to be opened. I configured traps from the two Grandstream switches and the Omada switch, using SNMPv3 authentication and encryption on Omada. My NAS-side receiver records events and sends Telegram notifications for selected ports. I verified real link-down and link-up notifications from an Omada test port; I did not unplug every critical server or uplink.

[How the receiver and delivery queue work →](../docs/pages/nas-services-operations.html)

## What I still want to check

The physical cabling inventory is not finished, and some IPv6 neighbor bindings still need a complete restart and prefix-change test. I'd also like to use a dedicated Wi-Fi access point with the Proxmox lab for separate captive-portal and NAC experiments.

[Certificate-based network access →](../docs/pages/identity-pki.html)   [Upcoming Wi-Fi tests →](../docs/pages/roadmap.html)

---
