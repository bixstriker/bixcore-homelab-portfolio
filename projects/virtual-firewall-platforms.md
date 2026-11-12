# Firewall and Router Systems I've Tried

I use the same virtual Windows and Linux clients to get a feel for different firewall systems. My first goal with each product is simple: set up the WAN and LAN correctly, make client traffic work, then find out how its firewall rules and administration behave.

## The common lab setup

Each firewall VM has a dedicated test upstream and its own virtual client network. I normally run one firewall with one or two clients, rather than all the products together. None of these experiments replaces my everyday OPNsense gateway.

## What I have installed and tested

| Platform | Work completed | Next things to try |
| --- | --- | --- |
| **MikroTik CHR / RouterOS** | Set up the virtual interfaces, initial RouterOS configuration, LAN addressing and selected NAT/client access. | More firewall rules, routing protocols and VPN testing. |
| **pfSense CE** | Configured WAN/LAN, DHCP, management access and NAT, then checked selected RDP forwards to the client VMs. | IPv6, IPS and a fuller inter-zone policy test. |
| **Sophos Firewall Home** | Completed the initial setup and checked management and basic guest connectivity, including a working checkpoint. | Its security controls, authentication and policies. |
| **VyOS Stream** | Worked through its CLI, client DHCP with fixed leases, outbound NAT and selected destination NAT rules. | More advanced routing, IPv6 and firewall policies. |
| **FortiGate VM** | Used the restricted free edition for basic interfaces, management, time sync, virtual IPs and controlled client access. | A fuller evaluation, if I can get the appropriate license, including inspection, VPN and VDOMs. |
| **OpenWrt x86-64** | Installed the VM, expanded the root filesystem and tested DHCP, NAT and selected management/forwarding access. | Additional routing and guest-network features. |
| **IPFire** | Configured RED/GREEN interfaces, fixed an initial WAN bridge mistake and checked DHCP, the web interface and a selected RDP forward. | More policy, VPN and recovery tests. |
| **NethSecurity 8.8.1** | Configured an isolated virtual LAN, DHCP, internet/NAT, management and two RDP forwards to Windows/Linux clients. | Policies, authentication and recovery. |
| **FreeSense 1.1.12** | Installed on ZFS, recovered from an installation-media mountroot panic, configured Kea DHCP and verified internet plus two RDP forwards. | IPv6 and management hardening. |
| **OpenFW UTM Community 4.2.1** | Configured RED/GREEN networks and DHCP, opened the WebGUI and confirmed an RDP connection through an inbound forwarding rule. | SSH acceptance, tighter management settings and policy/recovery tests. |
| **DD-WRT r66445 (x86-64)** | Tested WAN/LAN, DHCP, NAT, RDP, recovered a UEFI kernel panic, repaired the persistent boot template and validated two reboots. | ACPI shutdown and firmware-update persistence. |
| **OPNsense Community 26.7 (lab VM)** | Deployed a separate virtual OPNsense and verified internet/NAT and two client RDP forwards. | IPv6, rules and isolation. |

[FreeSense startup incident →](../docs/pages/notes.html#freesense-boot)

There are now **thirteen router/firewall VMs representing twelve distinct platforms**. A second virtual OPNsense guest is an independent full clone whose IPv6-only network connection and delegated prefix remain untested. OpenFW was tested with RDP forwarding; the original eleven VMs are the ones covered by PhyLan1.

## November 6: update and real-client checks

I updated MikroTik CHR to RouterOS 7.25.1, Sophos Firewall Home to SFOS 23.0 GA and IPFire to Core Update 205. DD-WRT stays on its tested build because of its local boot patch.

I confirmed internet connectivity, RDP forwarding to my Windows/Linux test guests and an external laptop connection across all eleven firewall/router VMs. The laptop uses my [PhyLan1 bridge selector](../docs/pages/phylan1.html). These are practical basic connectivity checks, not full IPS, VPN or policy comparisons.

## Later maintenance

On 12 November I confirmed NethSecurity 8.8.1 and updates to both virtual OPNsense installations, although their exact build numbers were not recorded. The two client VMs were updated, and VyOS deliberately stayed on Stream 2026.03. I have kept those version updates separate from the earlier tested forwarding and client-access results.

## DD-WRT: boot repair and remaining limitation

A reset exposed a mismatch between the bootloader's disk/filesystem arguments and the guest's installed ext4 root partition. Updating GRUB alone was not durable: its configuration could be regenerated from a compiled template in the DD-WRT service binary. I updated both the configuration and its source template using equal-length substitutions, then used UEFI reboot handling to address the restart hang. Two consecutive guest reboots worked, and I kept a recovery snapshot. Normal ACPI shutdown still fails.

A separate management-access incident was caused by SSH brute-force blocking after failed login attempts, not faulty routing. I inspected the guest blocklist and firewall rules before restoring access.

[DD-WRT boot troubleshooting →](../docs/pages/notes.html#ddwrt-uefi) · [Reboot hang →](../docs/pages/notes.html#ddwrt-reboot) · [SSH access incident →](../docs/pages/notes.html#ddwrt-access)

## What the tests taught me

Most of the early problems were about getting packets through the right interface. A virtual NIC connected to the wrong bridge can look like a DHCP or firewall problem, so I now check the host, switch and gateway before changing guest rules.

Port forwarding is a useful way to verify a path, but it doesn't say much about what a firewall blocks. I want to make the next round more consistent: positive and negative access tests, IPv4 and IPv6, management security, restart behavior and eventually performance.

## More platforms on the list

I'd like to try licensed versions of Palo Alto VM-Series, Juniper vSRX, Check Point CloudGuard, SonicWall NSv and FortiGate VM, plus Cisco Catalyst 8000V for routing. I also want to add RADIUS/802.1X integration to the already installed PacketFence VM, and bring real Wi-Fi clients into the lab. These are plans, and access to commercial features will depend on the available trials.

[Complete list of planned tests →](../docs/pages/roadmap.html)   [How I test the platforms →](../docs/pages/lab-operational-method.html)   [The IPFire bridge mistake →](../docs/pages/notes.html#ipfire)

---
