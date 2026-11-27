# Problems I ran into

Quite a few parts of BiXCore took more than one attempt. Some failures were caused by a small configuration detail; others needed packet captures, service logs and tests from both sides of the connection. These are the cases worth keeping notes about.

## OPNsense, WAN and IPv6

### Automating cleanup of invalid PF states after boot

My earlier manual PF cleanup stopped the warnings but did not prevent the problem from returning. On 26 November I found the same invalid gateway states after reboot, even though the active rules and the local broadcast rule were correct.

I extended my periodic check to verify the working gateway and recheck each matching state before removal. A second real reboot reproduced the warnings, then the check removed all 25 invalid states automatically. This mitigates the startup race without flushing unrelated states; it does not fix the upstream cause.

[The physical reboot and recovery tests →](../docs/pages/wan-failover-recovery.html)

### Why my TLS inspection kept being bypassed

The browser sometimes presented the public certificate despite a site-specific inspection rule. With the exclusion for flows without DNS enrichment enabled, the chosen HTTPS connections bypassed inspection. Turning that option off restored the local issuer and TLS-Inspected status.

A direct DNS test against Unbound, including a query and TLS connection using the same source address, did not fix the bypass. The missing enrichment remains unexplained; the result does not establish that AdGuard Home caused it.

[The TLS pilot →](../docs/pages/zenarmor.html)

### My Zenarmor multi-core tests exposed kernel panics

I tried native and emulated Netmap with several worker configurations to compare inspection performance. Instead, I recorded seven crash dumps and two further failures without a new dump. The repeated FreeBSD mbuf/iflib stack and Netmap messages were evidence of a stability problem, not proof of which component was responsible.

I returned to routed Emulated Netmap without multi-core. The gateway resumed service, but a full stress test and a reliable performance comparison are still outstanding.

[The stability investigation →](../docs/pages/zenarmor-multicore.html)

### A dual-stack portal login allowed IPv6 but lost IPv4

My guest iPhone had a valid IPv4 address and several IPv6 addresses, but after signing in over IPv6 the portal only allowed the IPv6 side. The IPv4 address appeared in ARP yet was absent from the captive-portal session and its PF allow table. This wasn't a DHCP problem.

I traced the difference to OPNsense's address filtering with Client Roaming enabled, matching upstream issue #11214. After checking the upstream patch against the installed version and preserving rollback files, I applied the targeted fix and restarted only the portal background process.

The **same live session** gained its missing IPv4 permission without another login. The nine existing IPv6 entries remained in PF, and the phone passed a dual-stack test with an IPv6 readiness score of 10/10. The custom patch must be checked after later OPNsense updates; I can't assume a package upgrade will preserve it.

[How the guest network is set up →](../docs/pages/network-services.html)


### The new IPv6 alias started out empty

I wanted the local IPv6 policy to follow the networks actually assigned to my interfaces, rather than a hard-coded prefix from my ISP. The interface group appeared in OPNsense, but the corresponding PF table initially had no members.

I traced the difference between the interface-group Apply action and the alias refresh. Regenerating the filter templates and refreshing aliases fixed the table without changing firewall source code or flushing PF state. A Guest device could use IPv6 internet but not selected internal ULA or global addresses; a Core device could reach the same services.

This is a test of the **current** prefix, not proof of automatic handling of a future provider renumbering.

[IPv6 isolation →](../docs/pages/opnsense-ipv6.html)


### LTE stayed down after an OPNsense reboot

During the IPv6 lab work, the backup LTE modem did not bring its PPP link back after a gateway restart. A first device reset and interface reconfiguration did not restore usable connectivity. A later device reset brought LTE back in the observed session.

I haven't established the cause of that particular modem startup failure or automated its recovery. The full primary-WAN-to-LTE failover and VPN restoration had passed separate real-world tests; the boot incident was a different problem.

[Gateway operations →](../docs/pages/security-operations.html)

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

I removed the affected states individually and confirmed the errors stopped. The underlying startup-order issue is not fixed upstream. I later added a tested [automatic mitigation](../docs/pages/notes.html#pf-bootzero).

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

### Omada refused my own CA certificates during RadSec setup

I wanted my wired Omada switch to use RADIUS over TLS with **server-certificate verification left on**. My first internally issued certificates failed the handshake. I tried a fresh root CA, then a root and intermediate chain, reissued the server certificate and checked the chain with OpenSSL. Everything could look fine on the machines running OpenSSL while the switch still refused it.

I couldn't retrieve the precise X.509 error from Omada. Instead of inventing a firmware explanation, I tried the existing public Let's Encrypt server certificate and an appropriate trust bundle. The switch passed the server side of TLS, but RadSecProxy then rejected Omada's **client certificate** with an issuer-trust error. The two trust directions had become mixed up during the experiment.

I restored the original client-authentication CA on the proxy while keeping Let's Encrypt for the server. Omada then completed TLS 1.3 and FreeRADIUS returned Access-Accept, with verification enabled. I removed the test certificates and profiles afterward.

I still don't know which exact X.509 rule made Omada reject my experimental internal server certificates. A working public chain is a measured workaround, not proof that the switch rejects all private PKI.

[How I built the RadSec connection →](../docs/pages/radsec-mtls.html)

### RadSec worked, but my UniFi Disconnect stopped working

After moving both UniFi APs to RadSec, clients could still complete EAP-TLS authentication and Accounting, but my own RADIUS Control Disconnect request stopped getting ACKs. It was tempting to blame the TLS migration as a whole. The evidence was more specific.

The proxy had changed the **source directory for Accounting Detail**, even though the original AP identity was still inside the RADIUS record. Separately, the UniFi DAS service rejected requests using an outdated pre-RadSec setting. I traced the latter through an AP-side diagnostic message and the currently active TLS-client configuration.

I changed my two restricted helpers to check the precise proxy/AP Accounting relationship and verify the matching TLS client before selecting the DAS configuration. Unknown or ambiguous state still causes a refusal, not a speculative Disconnect.

In real tests, one phone returned Disconnect-ACK and completed scoped PMKSA cleanup before a new session, while a second accepted an EAPOL reauthentication request and recorded an Accounting Stop/Start. The source/helper release was **v1.0.2**; the NAS web containers were not rebuilt. Those tests happened before the final late-evening certificate cleanup, so I won't extend the claim beyond that checkpoint.

[The RADIUS Control changes →](../docs/pages/radius-control.html) · [RadSec project →](../docs/pages/radsec-mtls.html)

## Switching, certificates and clients

### Omada acknowledged Disconnect but left the old session open

I added individual wired 802.1X Disconnect to my RADIUS Control tool. At first the Omada switch returned a RADIUS NAK. After reducing the packet to the fields it actually expected, the switch sent a verified Disconnect-ACK and the client authenticated again.

The hard part came afterward. Omada did not reliably send Accounting-Stop for the old record, and one replacement Accounting-Start arrived just after my original waiting window. Treating ACK alone as proof that the database was clean would have been misleading.

I kept the exact client/port/session checks, extended the bounded wait and allowed the old Accounting record to close **only when a matching new session appeared and the old row had not changed**. No automatic retry is sent after an uncertain result. Final live tests on two different wired ports confirmed a new session and correctly closed previous record for each.

[What I built around this behavior →](../docs/pages/radius-control.html)


### A stale Wi-Fi session ID caused a UniFi Disconnect-NAK

After adding RADIUS Accounting for UniFi, I tried terminating one phone's Wi-Fi session. The first request failed because I used a session identifier from before roaming. I located the current accounting record and sent another targeted Disconnect. The access point returned an ACK; the phone disconnected and completed EAP-TLS again.

This was a tested disconnect and reauthentication, not a live VLAN reassignment.

[Certificate access →](../docs/pages/identity-pki.html)

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

### TACACS+ did not fall back to local login on Omada

I configured directory-backed TACACS+ login on Omada and Barox switches, then deliberately made the authentication service unreachable. Barox accepted its local recovery account. On Omada, the local account worked in explicit local mode but was rejected with TACACS+-then-local selected. I reproduced the timeout with a targeted network drop and saw unanswered TCP connection attempts.

The behavior is reproducible in this setup; I have not proved why the firmware fails internally. I sent the case to vendor support and kept it open.

[TACACS+ and the controlled fallback tests →](../docs/pages/tacacs-switch-aaa.html)

### Two PKI publication jobs used the same temporary file

An Android certificate revocation triggered two publication paths within seconds. One task reported that its remote temporary file had disappeared: the other had already moved it. An independent task successfully published the updated CRL, so the observed failure wasn't a missing revocation list.

I introduced a named mutex and unique temporary filenames. A normal run worked, and a controlled second run waited for the lock and completed. I have not simulated two simultaneous changing-file publications after the fix.

[Certificate publication and revocation →](../docs/pages/windows-ad-pki.html)

### RustDesk installed, but the deployment task hung

An MSI upgrade returned error 1603 on one workstation. The EXE package installed the newer version, but my PowerShell script kept waiting for child processes instead of the installer. I changed the wait strategy and checked the actual installed version. The revised manual run completed; another workstation was offline during this review.

[The Group Policy deployment →](../docs/pages/windows-policy-deployment.html)

### KRDP connected but rejected the Linux account context

A Windows Remote Desktop connection reached the Kubuntu service over TLS, then showed a brief black screen before disconnecting. Re-entering the same credentials did not help. A saved RDP connection that sent the full Linux UPN in the correct Windows account context worked.

That isolates a tested client-side credential format, not a proved defect in KRDP's internal parser. The separate TLS certificate was also renewed, and SSH key access was tested independently.

[Kubuntu and Android identity →](../docs/pages/linux-mobile-identity.html)

## NAS and infrastructure services

### My NAS chose the wrong network interface

After a brief link loss and recovery, the NAS had two connected routes to the same subnet. New connections could leave through the secondary interface, even though the primary default route was back. That broke the intended source-address restriction on my gateway management connection.

I added a guarded policy-routing rule after the existing source-based rules and a systemd timer to maintain it. Route checks and SMB Multichannel passed, with both SMB paths still selected. A fresh reboot, DHCP renewal and physical link-flap test of this change were still outstanding.

[NAS routing and SMB tests →](../docs/pages/nas-services-operations.html)

### A network adapter reset interrupted a domain controller backup

One scheduled System State backup failed when the domain controller's Realtek adapter reset and SMB access to NAS storage dropped. The driver was updated on both controllers. The following week's backups were reported successful, but restoration and the validity of every backup catalog have not been tested.

The backup rotation is still based on dated folders instead of verified successful backup results.

[Windows backups →](../docs/pages/windows-monitoring-backup.html)

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

### PacketFence registered a guest, but IPSet still failed

The Windows VM reached the captive portal and registered as a guest, yet outside HTTPS did not work. PacketFence generated an IP/MAC pair for a set that accepted IP addresses only, so rule loading failed. Codex and I traced the mismatch and applied a small local fix without bypassing the default filtering policy. The relevant upstream report is issue #9339.

[PacketFence tests →](../docs/pages/packetfence-nac.html)

### PacketFence's DNS proxy forwarded to itself

After IPSet worked, external TCP/443 succeeded, but names resolved back to the portal. PacketFence was using its own DNS listener as an upstream forwarder. I changed the upstream while keeping PacketFence as the client DNS server. Afterward, HTTPS worked, and revoking/restoring guest registration correctly blocked/restored outside access.

[PacketFence tests →](../docs/pages/packetfence-nac.html)


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

### FreeSense started from the wrong boot medium

After installing FreeSense with ZFS, the VM initially stopped with a mountroot panic. The installation ISO was still attached, so it wasn't starting from the installed system disk. Removing the installer from the boot path solved the problem. Kea DHCP, internet access and both RDP port forwards were checked afterward.

[FreeSense tests →](../docs/pages/virtual-firewall-platforms.html)

### DD-WRT could boot, but not reboot

After fixing the root-device mismatch, DD-WRT still hung at “machine restart.” The image used a BIOS reboot setting, but the VM was running under OVMF/UEFI. I changed that setting in the GRUB configuration and in the template that can regenerate it. Two successive reboots worked.

**Normal poweroff remains unresolved.** Neither the guest poweroff command nor Proxmox Shutdown completed a clean power-off in the documented tests.

[DD-WRT tests →](../docs/pages/virtual-firewall-platforms.html)

### DD-WRT: a UEFI kernel panic kept returning

A reset exposed a persistent kernel panic: the bootloader referred to an outdated root device and filesystem format, even though the installed DD-WRT image used an ext4 root partition. The same bad arguments were embedded in a binary configuration template, so simply editing the generated GRUB file was not a durable fix.

With backups and a snapshot available, I updated the boot configuration and made size-preserving replacements in the offline template. A separate UEFI reboot problem also needed a fix. Two further reboots succeeded, and the running kernel parameters matched the root filesystem. **Normal ACPI shutdown is still broken**, and a future firmware update could replace the patched executable.

[DD-WRT on the firewall test page →](../docs/pages/virtual-firewall-platforms.html)

### DD-WRT management vanished after failed SSH attempts

SSH and WebGUI access from the administrator's workstation unexpectedly stopped working. Inspection of the blocklist and packet-filter rules showed that two failed SSH attempts had triggered DD-WRT's brute-force protection; this was not a VLAN, bridge or interface failure.

I removed the affected runtime block in the lab and restored access, without globally disabling the protection. Existing blocklist entries may reapply after reboot until they expire.

[DD-WRT platform notes →](../docs/pages/virtual-firewall-platforms.html)

---
