# Network: Project Index

I keep detailed working notes for the network. This index links each section to the corresponding project write-up, from gateway configuration and DNS to switching, monitoring and the IPv6 problems I have worked through.

The status column distinguishes running configurations, individual tests, earlier approaches and ideas that are not finished yet.

| Section | Work | Status | Read more |
| --- | --- | --- | --- |
| 01 | Network inventory, hardware roles and logical topology | Implemented and audited | [Hardware and lab setup](../docs/pages/hardware.html) |
| 02 | WAN uplinks; IPv4, IPv6 prefix delegation; VLAN address-plan design | Implemented | [Gateway and IPv6](../docs/pages/opnsense-ipv6.html) |
| 03 | DHCPv4, RDNSS, AdGuard/Unbound, conditional AD DNS, dynamic DNS and ACME | Implemented; selected checks | [DNS, DHCP and guest services](../docs/pages/network-services.html) |
| 04 | Firewall segmentation, NAT, policy routing and invalid stale state troubleshooting | Observed selected events | [Gateway operations and fixes](../docs/pages/security-operations.html) |
| 05 | Home WireGuard, policy-routed commercial VPN and selected forwarded application | Verified selected paths | [Gateway and IPv6](../docs/pages/opnsense-ipv6.html) |
| 06 | FreeRADIUS EAP-TLS, local-first directory fallback and CRL update persistence | Observed selected auth/failover | [Certificate-based access](../docs/pages/identity-pki.html) |
| 07 | Dual-stack guest Captive Portal with dynamically generated AAAA | Configured and observed response | [DNS, DHCP and guest services](../docs/pages/network-services.html) |
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

### How to use this index

The older entries show how the network changed over time. For an individual incident or test, the linked article explains what I checked, what worked and what I still want to try.

---
