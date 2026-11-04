# Problems I ran into

Quite a few parts of BiXCore took more than one attempt. Some failures were caused by a small configuration detail; others needed packet captures, service logs and tests from both sides of the connection. These are the cases worth keeping notes about.

## OPNsense, WAN and IPv6

### The wrong IPv6 source address

My WAN had more than one global IPv6 address, but outbound connections behaved differently depending on which source I used. Tests with explicitly selected addresses showed that the provider's SLAAC address could not reach the same target that worked from the DHCPv6 IA\_NA address.

I added a recovery mechanism for the observed source-selection problem. Provider reconnects and future prefix changes still need watching.

[OPNsense and IPv6 →](../docs/pages/opnsense-ipv6.html)

### Dynamic DNS stopped updating after a reboot

The DNS update service was running, yet it could not reach the provider's API over IPv6. I traced that to the same WAN source-address problem rather than assuming the DNS records or API credentials were wrong.

The connection was restored in the documented session. I kept a follow-up check for future WAN renewals.

[DNS and dynamic records →](../docs/pages/network-services.html)

### Firewall states pointing to an invalid gateway

After a reboot, repeated ARP errors led me to PF states containing a route-to address of 0.0.0.0. The active firewall rules already pointed to the real gateway, so changing the saved rules was not the answer.

I removed the affected states individually and confirmed the errors stopped. The underlying startup-order issue still needs a permanent fix.

[Gateway operations →](../docs/pages/security-operations.html)

### WireGuard: IPv4 worked, but IPv6 needed a different approach

I wanted one mobile client to send both IPv4 and IPv6 traffic through home. A static IPv6 translation did not fit a provider prefix that can change, so I moved to NPTv6 using the tracked delegated prefix.

I checked the effective firewall translation, external client addresses, DNS and permitted local access. A real upstream prefix rotation remains an open test.

[WireGuard test results →](../docs/pages/opnsense.html)

### Keeping the guest portal reachable over IPv6

The guest portal's IPv6 address depends on the prefix assigned by the provider. I added an update path for its DNS AAAA record and checked the generated record against the active address.

That established the update mechanism, but it was not a substitute for testing a future real prefix change.

[Guest network services →](../docs/pages/network-services.html)

### An LLDP management address that needed to survive updates

LLDP neighbors were visible, but the desired management-address advertisement also needed to survive service restarts and configuration regeneration. I added a startup/persistence hook and checked the advertised value.

The distinction between a running setting and a persistent setting has been useful in other parts of the gateway too.

[Switching and LLDP →](../docs/pages/switching-wireless.html)

## Switching, certificates and clients

### Testing the second LDAPS server for real

FreeRADIUS had two directory endpoints configured. I made the primary controller unavailable and repeated the authentication checks instead of assuming failover would happen simply because a second server appeared in the configuration.

The directory lookup continued through the second controller. The CA and enrollment service are separate dependencies with their own recovery needs.

[AD CS and FreeRADIUS →](../docs/pages/windows-ad-pki.html)

### Wired EAP-TLS on the domain controllers

A domain controller can need network access before it can contact the directory and certificate services involved in its usual authorization path. I had to separate the controller's bootstrap identity from ordinary computer authorization.

After adjusting certificate selection and the relevant policies, I verified the wired authentication behavior against the switch and FreeRADIUS.

[Domain controller EAP-TLS →](../docs/pages/windows-ad-pki.html)

### IPv6 addresses that resolved in DNS but could not be reached

A domain controller answered through one IPv6 address but not through its manually configured address. Packet and switch-side checks pointed to Omada's IPv6 Neighbor Discovery inspection.

Specific neighbor bindings restored the tested connections. Automatically learning new addresses after a prefix change remains a separate problem.

[Switch and IPv6 investigation →](../docs/pages/switching-wireless.html)

### Android requested another certificate

Enrollment through the MDM SCEP profile worked, but applying the enterprise Wi-Fi payload could trigger a second request. I investigated the interaction between the certificate and Wi-Fi profiles while checking actual EAP-TLS access on the devices.

The clients connected successfully. Cleaning up certificates that have been superseded is still on my list.

[Android and Linux clients →](../docs/pages/linux-mobile-identity.html)

### Windows signed in with a temporary profile after domain migration

While moving an existing Windows installation into Active Directory, the profile migration tool left a stale registry profile entry and an access problem with the user's profile data. Windows started a temporary desktop instead of the original one.

I checked the profile service events, corrected the registry mapping and permissions, and verified that the usual desktop loaded again. The lesson was to preserve the old profile and diagnose the mapping before creating a new one.

[Windows domain migration →](../docs/pages/windows-policy-deployment.html#profile-migration)

### Keyboard layouts missing at the Windows sign-in screen

On the second domain controller, the expected keyboard layouts were configured in parts of Windows but did not all appear at the sign-in screen. I compared the machine's language settings with the first controller and found that the interactive administrator profile differed.

After updating that profile's language list and signing out, the missing layouts appeared. The scheduled configuration task still returned a nonzero status, so I kept a reboot-persistence check open instead of treating the task result as proof of failure or success.

[Windows policies and administration →](../docs/pages/windows-policy-deployment.html)

### Windows Admin Center and HTTPS binding

When its HTTPS endpoint did not behave as expected, I checked the certificate and HTTP.sys listener/binding rather than treating the issue as a generic browser error. The corrected binding was part of the Windows administration setup.

This was also a reminder that installing a trusted certificate and actually serving it are two different steps.

[Windows administration tools →](../docs/pages/windows-policy-deployment.html)

## NAS and infrastructure services

### The NAS lost its IPv6 ULA

After network events, the NAS could lose the stable internal IPv6 address used by client DNS. An old interface-up hook was not enough to recover reliably.

I replaced that approach with an idempotent recovery script, a systemd oneshot service and a periodic timer, then checked that the expected address returned.

[NAS networking →](../docs/pages/nas-services-operations.html)

### A container chose the wrong network route

A reverse-proxy container attached to more than one Docker network picked up an unsuitable route and IPv6 address. I corrected the desired Compose network settings instead of relying on a temporary change inside the running container.

That mattered for both reachability and predictable behavior after recreation.

[Docker and reverse proxy →](../docs/pages/nas-services-operations.html)

### UPS monitoring would not start

Network UPS Tools could not find the attached USB UPS at first. The permissions on the USB device prevented access; after correcting the device handling, the service connected to the UPS.

Another configuration change accidentally bound the service to addresses not present on the gateway. Correcting the listening addresses restored access. Neither test means every device has battery-backed power.

[Monitoring and power →](../docs/pages/security-operations.html)

## Proxmox and virtual firewalls

### The lab WAN and VLAN path

An early DHCP problem needed checks at the virtual NIC, Proxmox bridge, tagged switch port and gateway, rather than repeatedly changing the guest firewall. I also had to correct DNS permissions for the lab segment.

The relevant L2 path and selected gateway services were checked. A separate test matrix covers traffic that should be denied.

[How I test the lab →](../docs/pages/lab-operational-method.html)

### Proxmox lost IPv6 Router Advertisements

After moving the host to Linux bridges, IPv6 addressing needed attention: the normal forwarding/RA defaults did not give the management bridge the behavior I wanted.

I adjusted the host interface settings and checked the live IPv6 path. Persistence across future network changes was left on the follow-up list.

[Proxmox host networking →](../docs/pages/proxmox-host-storage.html)

### Replacing the VM storage

Health checks on the old VM drives showed a storage problem I did not want to ignore. I inspected SMART and ZFS state, migrated the VM data to a replacement disk and brought the guests back up.

The replacement is a single-disk ZFS pool, so recovering the guests was not the same thing as adding redundancy or testing an off-host restore.

[Storage migration →](../docs/pages/proxmox-host-storage.html)

### Intel passthrough, a missing EDID and a broken-looking desktop

Combining the passed-through Intel GPU with an additional virtual display adapter caused KWin hangs and page-flip errors. With the conflicting display removed, the KDE VM still needed a usable EDID to get Full HD.

Providing the missing EDID solved the resolution problem. A separate KRDP image-quality setting and a KWallet interaction also needed attention.

[GPU and KRDP tests →](../docs/pages/gpu-remote-desktop.html)

### IPFire was connected to the wrong upstream bridge

During the IPFire setup, the WAN-side virtual NIC initially used the wrong Proxmox bridge. Once that was corrected, the firewall obtained its upstream address and the lab client tests could proceed.

Management, DHCP and a selected RDP port forward were verified afterward.

[Firewall platform comparisons →](../docs/pages/virtual-firewall-platforms.html)

---
