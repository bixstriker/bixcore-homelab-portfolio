# Projects I'm planning

Some ideas come from things I still want to improve in the running network. Others are technologies I've been curious about for a while. This is the list I come back to when I have time to work on the lab.

## Getting more out of the current setup

### IPv6 after a real prefix change

WireGuard and NPTv6 work with the current delegated prefix. I want to see what happens when my provider changes it, including the DNS updates and what the mobile clients experience after reconnecting.

[Current IPv6 setup →](../docs/pages/opnsense-ipv6.html)

### Restoring services from backup

I have backups and working recovery procedures for several systems. Next I want to restore individual NAS applications, the Proxmox guest data and the Windows certificate services in a controlled test, not just check that backup jobs have run.

[NAS work →](../docs/pages/nas-services-operations.html)

### Testing the paths that should be blocked

The lab networks are separated through bridges and firewall rules. I want to go through the possible IPv4 and IPv6 paths systematically, including management access, VPNs and connections between virtual firewalls.

[Firewall tests so far →](../docs/pages/lab-operational-method.html)

### Certificate renewals and old device identities

Windows, Kubuntu and managed Android devices can authenticate with certificates. I want to improve automatic replacement and revocation, especially when Android requests another SCEP identity while receiving a Wi-Fi profile.

[Client certificate work →](../docs/pages/linux-mobile-identity.html)

## Other firewall and router systems

I've already tried several free or restricted virtual editions in Proxmox. I'd like to learn the full policy and management workflows of some commercial products, using the same Windows and Linux test clients. The available trials and features will determine what I can actually run.

### FortiGate-VM

I've used the restricted free edition. A broader evaluation would let me spend more time with FortiGuard inspection, SD-WAN, VPN and VDOMs.

### Palo Alto VM-Series

I want to learn PAN-OS zones, App-ID, security profiles and how policy decisions appear in the logs.

### Juniper vSRX

Junos, security zones, routing, NAT and VPN behavior are the main reasons I want to try it.

### Check Point CloudGuard

I'm interested in the separation between management, policy installation and inspection on the virtual gateway.

### SonicWall NSv

Another opportunity to compare firewall administration, VPNs and threat-prevention policies.

### Cisco Catalyst 8000V

This is a virtual router rather than a traditional NGFW. I'd use it to learn more about IOS XE, dynamic routing and WAN scenarios.

Of these, FortiGate-VM is already installed in its free edition. The wider evaluations are still on my list.

## More ways to test the network

### IPv6-only lab WAN

I want a separate IPv6-only upstream for the virtual firewalls so I can test DNS, routing, application behavior and the workarounds different systems need without IPv4.

### A physical Wi-Fi test network

A dedicated Cudy Wi-Fi 7 access point and real laptops and phones would be useful for captive portals, VLAN behavior, DHCP and enterprise Wi-Fi, without changing the regular home WLAN.

### RADIUS and PacketFence

FreeRADIUS already handles EAP-TLS in the main network. I want to experiment with RADIUS integration in the lab, then explore what PacketFence adds for network access control.

### BGP and FRR

I'd like to set up a small routing lab and watch how prefixes and routes change when a link or neighbor disappears.

## More Zenarmor experiments

I already use Zenarmor on the OPNsense gateway and have tested policy-based blocking. There's more I want to investigate, especially how inspection behaves with encrypted traffic and what information its reports provide.

### TLS inspection

Compare what the lightweight TLS inspection can see with a controlled full TLS decryption test, if that feature becomes available. I'm interested in client trust, pinned applications, QUIC and websites that should bypass decryption.

### Filtering policies and reporting

Try different application and web-category policies on test clients, check exceptions and false positives, and compare live sessions and reports with what I see from the client.

### Interaction with Suricata

Look at how Zenarmor's policy decisions and Suricata IPS events relate to the same controlled traffic, without treating the two engines as if they do identical jobs.

### Inspection performance

Measure throughput, latency, loss and CPU use on the Intel N305 with and without inspection. If multi-core processing is available, repeat the measurements with the same traffic and policy settings.

[Zenarmor work and test ideas →](../docs/pages/zenarmor.html)   [The performance test plan →](../docs/pages/zenarmor-multicore.html)

---
