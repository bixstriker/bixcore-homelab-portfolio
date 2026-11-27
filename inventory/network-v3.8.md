# Network Master v3.37: Project Index

I keep detailed working notes for the network. This index links each section to the corresponding project write-up, from gateway configuration and DNS to switching, monitoring and the IPv6 problems I have worked through.

The 27 November revision adds switch-event notifications, IoT discovery across VLANs, the Ethernet LTE backup connection, physical WAN failover and failback with automatic VPN recovery, and a tested workaround for invalid PF states after boot. The Zenarmor tests include both a successful two-domain TLS pilot and failed multi-core/Netmap experiments. Older entries remain dated evidence rather than the current configuration.

| Section | Work | Status | Read more |
| --- | --- | --- | --- |
| 01 | Network inventory, hardware roles and logical topology | Implemented and audited | [Hardware and lab setup](../docs/pages/hardware.html) |
| 02 | WAN uplinks; IPv4, IPv6 prefix delegation; VLAN address-plan design | Implemented | [Gateway and IPv6](../docs/pages/opnsense-ipv6.html) |
| 03 | DHCPv4, RDNSS, AdGuard/Unbound, conditional AD DNS, dynamic DNS and ACME | Implemented; selected checks | [DNS, DHCP and guest services](../docs/pages/network-services.html) |
| 04 | Firewall segmentation, NAT, policy routing and invalid stale state troubleshooting | Observed selected events | [Gateway operations and fixes](../docs/pages/security-operations.html) |
| 05 | Home WireGuard, policy-routed commercial VPN and selected forwarded application | Verified selected paths | [Gateway and IPv6](../docs/pages/opnsense-ipv6.html) |
| 06 | FreeRADIUS EAP-TLS, local-first directory fallback and CRL update persistence | Observed selected auth/failover | [Certificate-based access](../docs/pages/identity-pki.html) |
| 07 | Dual-stack guest Captive Portal with dynamically generated AAAA | Configured and observed response | [DNS, DHCP and guest services](../docs/pages/network-services.html) |
| 07.1 | Guest RFC 8910 RA Option 37 | Captured on Guest, absent elsewhere; OS response not retested | [Guest RA](../docs/pages/network-services.html) |
| 07.2 | IPv6-first Captive Portal lost IPv4 permission | Upstream fix and same-session client test passed | [Guest portal incident](../docs/pages/notes.html#portal-dualstack) |
| 08 | Suricata IPS controlled block, Zenarmor policy block and LLDP | Observed selected tests | [Gateway operations and fixes](../docs/pages/security-operations.html) |
| 09 | Managed-switch IPv6/802.1X behavior and configuration diagnostics | Observed selected paths | [Switching, Wi-Fi and 802.1X](../docs/pages/switching-wireless.html) |
| 10 | Enterprise Wi-Fi; Grandstream membership/PVID; UniFi controller backup inspection | Observed / offline extraction | [Switching, Wi-Fi and 802.1X](../docs/pages/switching-wireless.html) |
| 11 | NAS ULA self-healing, Docker routes, proxy, infrastructure applications and update runbook | Implemented / selected tests | [NAS and Docker](../docs/pages/nas-services-operations.html) |
| 12 | Service/metrics monitoring and operating automation | Implemented / selected tests | [Gateway operations and fixes](../docs/pages/security-operations.html) |
| 13 | OPNsense backup, update, custom hook and recovery discipline | Documented and exercised | [Gateway operations and fixes](../docs/pages/security-operations.html) |
| 14 | Earlier post-update audit and selected performance/security observations | Observed historically | [Gateway operations and fixes](../docs/pages/security-operations.html) |
| 15 | Status matrix: confirmed configuration versus open questions | Methodology retained | [How I describe project status](../docs/pages/working-notes.html#running-tested-planned) |
| 16 | Source-evidence hierarchy: live output, exports, operational notes | Methodology retained | [How I investigate problems](../docs/pages/working-notes.html#checking-the-evidence) |
| 17 | Detailed OPNsense configuration export and service-level settings | Private source only | [Gateway operations and fixes](../docs/pages/security-operations.html) |
| 18 | Backup/export evidence boundaries and preservation plan | Methodology retained | [Keeping the working files](../docs/pages/working-notes.html#keeping-source-files) |
| 19 | OPNsense 26.7.7, RADIUS persistence and post-upgrade audits | Observed | [Gateway operations and fixes](../docs/pages/security-operations.html) |
| A | Read-only diagnostics for routing, DNS, RADIUS, VPN, IPS, NAS | Explained generically | [Troubleshooting notes](../docs/pages/notes.html) |
| B | Persistence and restoration of custom firewall/NAS hooks | Runbook documented | [Gateway operations and fixes](../docs/pages/security-operations.html) |
| C | Working configuration patterns for VPN, proxy and portal update logic | Sanitized design | [DNS, DHCP and guest services](../docs/pages/network-services.html) |
| D | WAN IPv6 monitor source-address incident and temporary recovery | Observed historical | [WAN IPv6 source problem](../docs/pages/notes.html#ipv6) |
| E | Post-reboot WAN/DDNS audit and UPS/NUT troubleshooting | Observed selected checks | [Gateway operations and fixes](../docs/pages/security-operations.html) |
| F | Dedicated Proxmox upstream VLAN and ACL/NAT path | Observed selected checks | [Firewall test methods](../docs/pages/lab-operational-method.html) |
| G | Postboot review, guest restrictions and monitoring notifications | Observed / some open | [Gateway operations and fixes](../docs/pages/security-operations.html) |
| H | Persistent workaround for provider IPv6 source-selection failure | Implemented / checked | [WAN IPv6 source problem](../docs/pages/notes.html#ipv6) |
| I | Selected-client WireGuard full-tunnel IPv4/IPv6 and dynamic NPTv6 | Observed on one client | [WireGuard and NPTv6](../docs/pages/notes.html#wireguard) |
| J | OPNsense 26.7.8_2 post-update audit, surviving hooks, NUT/LLDP/Zenarmor observations | Observed; some follow-ups open | [Gateway operations](../docs/pages/security-operations.html) |
| K | Interface-derived IPv6 local networks, PF refresh and Guest/Core functional tests | Tested now; real prefix change not yet tested | [IPv6 isolation](../docs/pages/opnsense-ipv6.html) |
| L | FreeRADIUS Accounting, UniFi session tracking and targeted Disconnect | Targeted Disconnect tested; live VLAN CoA rejected | [RADIUS session study](../docs/pages/identity-pki.html) |
| M | IPv6-only VLAN through OPNsense, switches and Wi-Fi with DNS64/NAT64 | Real clients tested; virtual-router DHCPv6-PD open | [IPv6-only network lab](../docs/pages/ipv6-only-lab.html) |
| N | OPNsense 26.7.9_1 update and WAN/service observations | Dated post-update checks | [Gateway operations](../docs/pages/security-operations.html) |
| O | Strict EAP-TLS and real client/guest-portal checks | Selected tests passed; boot and AD-computer tests open | [RADIUS Control](../docs/pages/radius-control.html) |
| P | OPNsense 26.7.9_3 hotfix audit | Read-only PASS; reboot and fresh EAP-TLS not retested | [Gateway operations](../docs/pages/security-operations.html) |
| Q | TLS 1.2 resumption and 802.11r FT key caching | Full handshake observed; per-device FT invalidation unavailable in tested setup | [RADIUS Control](../docs/pages/radius-control.html) |
| R | Plex moved to Vodafone WAN with Suricata IPS | Measured speeds, 4K Direct Play and controlled IPS drop | [Gateway and IPS tests](../docs/pages/security-operations.html) |
| R.6 | WAN playback and a separate Windscribe forwarded endpoint | Current paths documented; prior live LTE/VPN failover tested | [NAS watchdog](../docs/pages/nas-services-operations.html) |
| S | RADIUS Control helpers and original Omada wired pilot | Documented earlier v0.10.7.3 checkpoint; stable v1.0.1 and later v1.0.2 helper acceptance | [Finished RADIUS Control](../docs/pages/radius-control.html) |
| T | RADIUS Control v1.0.1 production, Omada wired and gateway helper boundary | Prior stable release and tested wired controls | [RADIUS Control](../docs/pages/radius-control.html) |
| U | Initial RadSec/Omada certificate failure | Historical investigation; later resolved on public server chain | [RadSec certificate case](../docs/pages/notes.html#radsec-omada-certificate) |
| V | RadSec established for both UniFi APs and Omada | TLS 1.3, EAP-TLS, Accounting verified; later certificate rollback documented in W | [RadSec project](../docs/pages/radsec-mtls.html) |
| W | Final RadSec/mTLS state, CA cleanup and ACME service actions | Working TLS and restart tested; full ACME renewal to exported PEM untested | [RadSec and ACME](../docs/pages/radsec-mtls.html) |
| RADIUS Control v1.0.2 | Source/helper maintenance after RadSec migration | Three selected live actions passed; not re-run after final evening rollback | [RADIUS Control](../docs/pages/radius-control.html) |
| X | NUT configuration permissions and regeneration | Regeneration checked; later reboot audit passed | [Gateway operations](../docs/pages/security-operations.html) |
| Y | SNMP traps, SQLite and Telegram; Guest DNS | Real Omada link events delivered; other ports mapped | [NAS notification receiver](../docs/pages/nas-services-operations.html) |
| Z | IoT camera discovery and SMB to NAS across VLANs | Discovery A/B test and actual recording import confirmed | [IoT discovery and DNS](../docs/pages/network-services.html) |
| AA | GPON module preparation for future FTTH | Local preparation only; ISP/OLT interoperability not tested | [Future network work](../docs/pages/roadmap.html) |
| AB | Netmap buffer tuning and Suricata ruleset maintenance | Configuration and selected reload checks; later Netmap experiments in AH | [Inspection investigation](../docs/pages/zenarmor-multicore.html) |
| AC | Ethernet LTE migration and initial failover | Physical transition and NAS routing checked; stale-state issue led to later work | [WAN recovery](../docs/pages/wan-failover-recovery.html) |
| AD | Targeted PF cleanup and LTE IPv6 monitoring | Physical transition and autonomous monitor recovery observed | [WAN recovery](../docs/pages/wan-failover-recovery.html) |
| AE | Default-route observer and periodic VPN/PF recovery | Earlier implementation checkpoint; subsequent physical test in AF | [WAN recovery](../docs/pages/wan-failover-recovery.html) |
| AF | Physical failover/failback, custom backup and disk image; boot-state mitigation | Both WAN transitions and reboot cleanup tested; actual image restore open | [WAN recovery and backup](../docs/pages/wan-failover-recovery.html) |
| AG | Persistent access to Ethernet LTE modem in passthrough | HTTPS and SSH checked after modem reboot and renumbering | [LTE management](../docs/pages/wan-failover-recovery.html) |
| AH | Zenarmor multi-core crashes and narrow TLS inspection | Fallback and selected HTTPS tests; root cause and comparative benchmark unresolved | [Zenarmor pilot](../docs/pages/zenarmor.html) |

### How to use this index

The older entries show how the network changed over time. For an individual incident or test, the linked article explains what I checked, what worked and what I still want to try.

---
