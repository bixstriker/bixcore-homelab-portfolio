# DNS, DHCP and Network Services

I wanted clients to get dependable DNS without making the Windows domain controllers responsible for every internet lookup. IPv6, guest access and certificate renewal added a few interesting requirements.

## How DNS is arranged

OPNsense provides DHCPv4 and the local network's routing functions. AdGuard is the client-facing resolver where filtering is required, while Unbound handles its own DNS role and selected internal records. Queries for the Active Directory domain are forwarded to the directory DNS service.

IPv6 clients learn their resolver information through Router Advertisements and RDNSS. I checked that the ordinary client and guest segments get the intended DNS behavior without relying on the same address family everywhere.

## Public records and HTTPS certificates

Dynamic DNS updates external records as WAN addressing changes. ACME DNS-01 is used for certificate renewal where needed, while NAS reverse-proxy certificates have a separate maintenance step. I check certificate renewal and external service connectivity independently; one being successful does not automatically make the other work.

## A careful AdGuard update

I moved AdGuard Home to a new beta image after making a rollback copy of its configuration and working data. I then checked normal DNS replies, conditional Active Directory queries, blocked domains, HTTPS, DNS-over-HTTPS and DNS-over-TLS. DNS-over-QUIC was listening, but I have not completed a full QUIC client request test. Renewed certificates are still deployed manually from the gateway to the NAS services.

## Guest access and network boot

The guest Captive Portal needs an IPv6 AAAA record that follows the guest network's current prefix. I added an update hook and compared the generated DNS record with the actual address. The mechanism worked in the recorded test, but a real provider prefix rotation still needs another check.

For network boot, I use a NAS-hosted PXE/ISO service with ProxyDHCP in the appropriate client segment instead of replacing the gateway's normal DHCP service.

## Making the Captive Portal discoverable over IPv6

I was already providing the portal URL through DHCPv4 Option 114. For IPv6 guests I added **RFC 8910 Router Advertisement Option 37** on the guest VLAN only. I captured the actual RAs and found the URL on Guest but not on Core or the IPv6-only test network. Prefixes, RDNSS and PREF64 remained unchanged.

The installed OPNsense release needed a small generator patch. I kept its original and rollback files, and will check it after upgrades. I haven't separately verified how each phone or operating system reacts to the option; the packet captures prove the advertisement itself.

I also fixed a separate dual-stack portal issue. A guest iPhone had IPv4 and IPv6, yet an IPv6-first login excluded IPv4 from PF. I applied the upstream OPNsense fix for issue #11214. The original live session gained IPv4 without a new login, kept nine IPv6 entries and passed the phone's 10/10 IPv6 readiness check.

[The portal issue →](../docs/pages/notes.html#portal-dualstack)

## Letting an IoT camera find the NAS without opening the whole network

Moving my Xiaomi camera to the isolated IoT network stopped its NAS discovery. The camera was sending NetBIOS discovery broadcasts, which did not cross the VLAN boundary. I used the OPNsense UDP Broadcast Relay for discovery and added a narrowly scoped SMB rule from that camera to the intended NAS interface.

I checked the active PF rules and captured the discovery and SMB traffic. With the discovery rule disabled, the camera could not find the NAS; enabling it restored discovery. I then confirmed that the camera's recordings were actually imported to the NAS. I left the general IoT-to-Core block in place, rather than allowing every IoT device to reach the storage network.

The test verifies this particular camera and its transfer path, not complete isolation against every possible protocol. No changes to the NAS's SMB service or credentials were necessary.

A separate check on 22 November confirmed that ordinary Core clients receive AdGuard as their DNS resolver, while Guest uses the gateway's local resolver in both IPv4 and IPv6. An encrypted DNS listener being enabled does not prove that every client uses it.

## Problems I ran into

After a reboot, dynamic DNS stopped updating even though its service was running. The cause was upstream IPv6 reachability, not a missing DNS configuration. The [DDNS investigation](../docs/pages/notes.html#ddns) and the [WAN source-address tests](../docs/pages/notes.html#ipv6) explain how those two symptoms were connected.

I also documented the [guest portal's IPv6 record updates](../docs/pages/notes.html#portal) and the [NAS DNS address disappearing](../docs/pages/notes.html#nas-ula) after a network event. These are separate problems with separate fixes.

[Gateway and IPv6 →](../docs/pages/opnsense-ipv6.html)   [NAS and Docker →](../docs/pages/nas-services-operations.html)

---
