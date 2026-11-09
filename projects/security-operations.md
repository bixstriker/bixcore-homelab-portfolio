# Keeping OPNsense Running

A firewall can look fine after an update and still have a broken background service or a stale routing state. I have spent almost as much time checking what survives a reboot as I have configuring the features themselves.

## Updates and persistent configuration

My post-update checks cover internet routing, DHCP and DNS, IPv6 delegation, FreeRADIUS and certificate revocation, the guest portal, LLDP, WireGuard, Suricata and Zenarmor. I compare service status with actual client behavior or gateway state where practical.

A standard OPNsense configuration backup doesn't contain every custom hook, cron job or NAS-side dependency I use. I keep a separate recovery list for RADIUS and CRL updates, LLDP settings, dynamic portal records and other local automation.

## A secondary LTE link that didn't return after reboot

While configuring the IPv6-only test network, the gateway's LTE modem didn't restore its PPP connection after a restart. I tried a manual device reset and interface reconfiguration; the link still lacked a usable address until a later reset. It then recovered.

I haven't established the underlying cause or automated this recovery. The full WAN failover sequence wasn't repeated after the incident.

[The LTE incident →](../docs/pages/notes.html#lte-recovery)

## Issues I investigated

### Invalid PF states after reboot

Old policy-routing states pointed at an invalid gateway even though the active rules were correct. Removing those states stopped the repeated errors; I still need a permanent answer to the startup sequence.

[What I checked →](../docs/pages/notes.html#pf-state)

### WAN IPv6 source selection

A provider-specific problem broke outbound traffic from one WAN IPv6 address. I compared explicit source addresses, applied a temporary workaround and later added a persistent recovery path.

[The IPv6 case →](../docs/pages/notes.html#ipv6)

### DNS and guest access after reconnects

I investigated dynamic DNS updates that stopped after reboot and checked the generated guest portal IPv6 record separately.

[The DDNS investigation →](../docs/pages/notes.html#ddns)

### UPS monitoring

Network UPS Tools initially failed to detect the USB UPS, and a later listener configuration also needed correction. I checked the actual UPS connection and power-test behavior.

[The UPS problems →](../docs/pages/notes.html#ups)

## Monitoring and resilience

I use service health checks and notification routing on the gateway, and collect metrics for the wider infrastructure. I ran a real primary-to-LTE-to-primary failover test on 5 November, including VPN recovery. The later modem boot issue is separate; I still need to retest individual services and failover after that incident.

Power protection has similar limits: I tested UPS communication and a controlled loss of mains power, but not every connected device has been confirmed to receive battery-backed power.

## What remains open

The startup cause of the invalid PF states is still unresolved. I also want more complete tests following WAN reconnects, prefix changes, UPS events and gateway restarts, with the resulting observations added to the working notes.

[All troubleshooting cases →](../docs/pages/notes.html)   [Current test plans →](../docs/pages/roadmap.html)

---
