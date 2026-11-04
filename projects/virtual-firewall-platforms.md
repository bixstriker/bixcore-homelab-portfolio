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

## What the tests taught me

Most of the early problems were about getting packets through the right interface. A virtual NIC connected to the wrong bridge can look like a DHCP or firewall problem, so I now check the host, switch and gateway before changing guest rules.

Port forwarding is a useful way to verify a path, but it doesn't say much about what a firewall blocks. I want to make the next round more consistent: positive and negative access tests, IPv4 and IPv6, management security, restart behavior and eventually performance.

## More platforms on the list

I'd like to try licensed versions of Palo Alto VM-Series, Juniper vSRX, Check Point CloudGuard, SonicWall NSv and FortiGate VM, plus Cisco Catalyst 8000V for routing. I also want to bring RADIUS, PacketFence and real Wi-Fi clients into the lab. These are plans, and access to commercial features will depend on the available trials.

[Complete list of planned tests →](../docs/pages/roadmap.html)   [How I test the platforms →](../docs/pages/lab-operational-method.html)   [The IPFire bridge mistake →](../docs/pages/notes.html#ipfire)

---
