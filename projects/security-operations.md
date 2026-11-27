# Keeping OPNsense Running

A firewall can look fine after an update and still have a broken background service or a stale routing state. I have spent almost as much time checking what survives a reboot as I have configuring the features themselves.

## Updates and persistent configuration

My post-update checks cover internet routing, DHCP and DNS, IPv6 delegation, FreeRADIUS and certificate revocation, the guest portal, LLDP, WireGuard, Suricata and Zenarmor. I compare service status with actual client behavior or gateway state where practical.

A standard OPNsense configuration backup doesn't contain every custom hook, cron job or NAS-side dependency I use. I keep a separate recovery list for RADIUS and CRL updates, LLDP settings, dynamic portal records and other local automation.

## A secondary LTE link that didn't return after reboot

While configuring the IPv6-only test network, the gateway's LTE modem didn't restore its PPP connection after a restart. I tried a manual device reset and interface reconfiguration; the link still lacked a usable address until a later reset. It then recovered.

I haven't established the underlying cause of that particular modem startup failure. The separate primary-to-LTE failover and VPN restoration path was successfully tested in live use.

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

## Plex streaming, VPN routing and an IPS test

Remote Plex playback had been going through Windscribe. I compared real download sessions: roughly **2.0–3.4 MB/s** through the VPN versus **4.4–5.1 MB/s** through Vodafone WAN. These figures describe the measured sessions, not a guaranteed speed.

I moved normal Plex streaming onto the faster WAN path. A remote Android phone played a **4K Direct Play** stream around 29 Mbit/s. I retained a dedicated Suricata inspection path and confirmed a controlled test signature was **dropped**, not just logged. I haven't measured coverage of every packet in a complete video session.

Windscribe still has its own forwarded endpoint for the NAS port-check watchdog, and the established HomeWG recovery path remains in place. I had already verified real WAN → LTE → VPN/WireGuard recovery before these Plex adjustments; this change did not redesign that failover path.

## Monitoring and resilience

I use service health checks and notification routing on the gateway, and collect metrics for the wider infrastructure. I ran a real primary-to-LTE-to-primary failover test on 5 November, including VPN recovery. The later isolated modem startup problem was separate from that tested recovery path.

Power protection has similar limits: I tested UPS communication and a controlled loss of mains power, but not every connected device has been confirmed to receive battery-backed power.

## What changed on 26–27 November

I replaced the earlier USB LTE modem with an Ethernet-connected Zyxel. A physical WAN failure and failback exercise verified targeted PF cleanup and automatic Windscribe recovery in both directions. A separate reboot proved the new automatic mitigation for invalid startup states. The [full recovery project](../docs/pages/wan-failover-recovery.html) covers the evidence and the checked but not yet restored backups.

The NUT permission correction also survived configuration regeneration and reboot. My post-boot audit checked the custom hooks, FreeRADIUS and selected services.

## What remains open

The startup cause of the invalid PF states is still unresolved. I will keep checking individual services after WAN reconnects, prefix changes, UPS events and gateway restarts, without treating the previously successful failover test as a new experiment.

[All troubleshooting cases →](../docs/pages/notes.html)   [Current test plans →](../docs/pages/roadmap.html)

---
