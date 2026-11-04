# DNS, DHCP and Network Services

I wanted clients to get dependable DNS without making the Windows domain controllers responsible for every internet lookup. IPv6, guest access and certificate renewal added a few interesting requirements.

## How DNS is arranged

OPNsense provides DHCPv4 and the local network's routing functions. AdGuard is the client-facing resolver where filtering is required, while Unbound handles its own DNS role and selected internal records. Queries for the Active Directory domain are forwarded to the directory DNS service.

IPv6 clients learn their resolver information through Router Advertisements and RDNSS. I checked that the ordinary client and guest segments get the intended DNS behavior without relying on the same address family everywhere.

## Public records and HTTPS certificates

Dynamic DNS updates external records as WAN addressing changes. ACME DNS-01 is used for certificate renewal where needed, while NAS reverse-proxy certificates have a separate maintenance step. I check certificate renewal and external service connectivity independently; one being successful does not automatically make the other work.

## Guest access and network boot

The guest Captive Portal needs an IPv6 AAAA record that follows the guest network's current prefix. I added an update hook and compared the generated DNS record with the actual address. The mechanism worked in the recorded test, but a real provider prefix rotation still needs another check.

For network boot, I use a NAS-hosted PXE/ISO service with ProxyDHCP in the appropriate client segment instead of replacing the gateway's normal DHCP service.

## Problems I ran into

After a reboot, dynamic DNS stopped updating even though its service was running. The cause was upstream IPv6 reachability, not a missing DNS configuration. The [DDNS investigation](../docs/pages/notes.html#ddns) and the [WAN source-address tests](../docs/pages/notes.html#ipv6) explain how those two symptoms were connected.

I also documented the [guest portal's IPv6 record updates](../docs/pages/notes.html#portal) and the [NAS DNS address disappearing](../docs/pages/notes.html#nas-ula) after a network event. These are separate problems with separate fixes.

[Gateway and IPv6 →](../docs/pages/opnsense-ipv6.html)   [NAS and Docker →](../docs/pages/nas-services-operations.html)

---
