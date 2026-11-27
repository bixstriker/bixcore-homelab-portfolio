# Building and Testing My OPNsense WAN Failover and Recovery System

## Why I changed the backup connection

I wanted my network to recover when the main internet connection disappeared, without having to reconnect my VPN or reset every firewall state by hand. My earlier USB LTE modem had sometimes needed manual recovery after a reboot. In late November I replaced it with a Zyxel LTE5398-M904 on a separate Ethernet WAN using IP passthrough. Vodafone remains the primary connection; O2 LTE is the backup.

I deliberately kept the backup policy selective. Core and IoT can use the backup IPv4 path, but the guest and IPv6-only lab networks are not given unrestricted access to my limited mobile data allowance. The LTE link also has working outbound IPv6; that does not make it an equivalent replacement for the inbound services on my primary connection.

## A link can fail without the event I expected

During a physical cable-disconnect test on 26 November, the default IPv4 route moved to LTE while the expected gateway-down event had not arrived. The original monitor hooks therefore missed the transition. Old PF policy-routing states still referred to the failed WAN, and Windscribe needed a manual restart.

I changed the recovery logic to observe the actual default route. A small periodic check now detects a change in the active path, removes only states belonging to the failed gateway when the current routing evidence agrees, and restarts the VPN once the new route has remained stable for 30 seconds. I kept the ordinary gateway-state mechanisms in place rather than replacing them with a global state flush.

## The physical failover and failback test

On 26 November I disconnected the primary WAN again. The recovery logic removed 282 obsolete WAN states, then another 15 in the next check: **297 in total**. Windscribe restarted automatically after the LTE route had been stable for 30 seconds and connected over the backup link.

When I reconnected Vodafone, the regular gateway-state cleanup removed 370 LTE states (249 IPv4 and 121 IPv6). My additional cleanup did not remove unrelated states. Windscribe then restarted once the primary route was stable and returned to Vodafone. I checked the gateways, IPv4/IPv6 paths, VPN and DNS afterward. These were real cable events, not simulated monitor notifications.

I also tested recovery of the LTE IPv6 gateway monitor after a modem reboot and a change of its source address. The periodic watchdog restored the monitor without my intervention in the second test. This is separate from the WAN path-switching logic.

## The old boot problem returned

After making an offline backup, I booted the gateway again and found three PF states pointing to an invalid zero gateway. The active firewall rules already contained the correct route. Packet captures and the local-network alias check also showed that Plex discovery broadcasts used the intended local rule once the gateway was up. Moving firewall rules around would not have addressed what I was seeing.

I extended the existing periodic cleanup with a separate guard for the invalid startup states. It only acts when the real WAN link, default route, cached gateway and active PF rules agree, and it rechecks the affected state before removing it by ID.

On the second physical reboot, the startup warnings appeared again. The periodic check automatically removed **25 of 25 invalid states**. Later checks showed zero remaining invalid states and all five gateways online. This is a tested mitigation for the startup problem, not an upstream fix for the ordering issue that creates the states.

## Two different recovery backups

A configuration export alone is not enough for this gateway. I keep an additional archive of custom files, hooks and service configuration, with a consistent FreeRADIUS SQLite backup. I checked the archive and database integrity before taking the firewall offline.

I then created a complete Clonezilla disk image of the system NVMe. Clonezilla checked the saved partition images, and the USB original and NAS copy matched by SHA-256 for all 32 files. I kept both copies. After booting the original gateway, I checked the custom hooks, service status, certificate validation configuration and selected connections.

The archive and disk image were made before the later startup-state mitigation and the 27 November LTE management changes. I keep the separate PF recovery package and the LTE management recovery notes; neither earlier backup includes those changes. A verified image is not the same as a successful restore: I have not yet restored it onto a spare disk or booted an isolated virtual clone. That is a future recovery exercise.

## Keeping the LTE modem manageable

The LTE passthrough address changes, so relying on that address for administration was inconvenient. I configured access to the modem's own management address through the backup WAN and tested HTTPS and SSH after a modem reboot. The route followed the changed gateway automatically. I did not need another restart hook for this.

## What I know now

The physical WAN transition, automatic Windscribe recovery in both directions and targeted boot-state cleanup were tested on the live gateway. I still need to recheck these mechanisms after future OPNsense upgrades and exercise the full image-restore procedure in isolation. I also do not treat a successful VPN reconnect as proof that every remote application remained uninterrupted.

[Gateway operations →](../docs/pages/security-operations.html) · [The startup-state investigation →](../docs/pages/notes.html#pf-bootzero) · [Hardware →](../docs/pages/hardware.html)
