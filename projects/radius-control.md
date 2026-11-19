# Building My Own RADIUS Session Management Tool

I originally built BiXCore RADIUS Control because I was tired of switching between the UniFi controller, RADIUS Accounting and OPNsense just to figure out which device was connected. My first attempt to disconnect a roaming phone used an old Session ID and failed. That was a useful reminder: a management tool should know what it is acting on, not just offer a button.

On **19 November 2026** I finished the stable **v1.0.0** release, then deployed **v1.0.1** with a more usable phone and tablet layout. The application runs on my NAS and manages selected FreeRADIUS and network-access operations through OPNsense. I kept the code private, but the design and results are worth documenting.

## What I can do from one screen

The dashboard combines live, stale and ended RADIUS Accounting sessions, selected history, local RADIUS users and Captive Portal sessions. I can refresh the snapshot, search for a device and see what an action would target.

For **local FreeRADIUS accounts** I can manually enable or disable access and change the configured VLAN. Those settings affect future authentications; changing a VLAN does not magically move an already connected client. I can also manage personal Captive Portal access and the separate shared guest Wi-Fi identity, with explicit confirmation before disconnecting guest devices.

**Active Directory is a strict boundary.** Directory-backed accounts are not disabled or modified by this application. I can inspect their Accounting sessions and request a targeted Disconnect only where the network device supports it.

## Why I split it into three containers

The first prototype worked, but I didn't want my browser-facing app to hold network administration keys. The production stack now has three Docker services:

- **web:** authenticated FastAPI interface, four languages (English, German, Ukrainian and Russian), light/dark themes, responsive layout and a permanent action log.
- **sync:** regularly brings a limited, sanitized Accounting and client snapshot from the gateway to the NAS.
- **control:** handles approved operations through narrow helper interfaces. The web container has neither general SSH access nor unrestricted access to the gateway.

On OPNsense, restricted commands independently check the real session again. I log outcomes such as ACK, NAK, refused actions and errors. If the audit storage is unavailable, sensitive operations are blocked rather than silently continuing without a record. An earlier web redesign and the final v1.0.1 layout update didn't require restarting FreeRADIUS.

## Testing UniFi on actual phones

I tested a targeted RADIUS Disconnect on a connected phone: the AP acknowledged it, the client left Wi-Fi and completed EAP-TLS again. A separate EAPOL reauthentication request worked too. The interface can check for leftover PMKSA entries when the selected Wi-Fi connection has already ended.

I also tightened the authorization rules behind the tool. In real client tests, disabling a local identity produced **Access-Reject** at the next full EAP-TLS login; enabling it allowed access again. An EAP identity that didn't match the certificate, or a certificate without a permitted matching local user, was rejected. One personal Captive Portal account was also prevented from starting a second simultaneous session.

A live VLAN change through UniFi CoA is **not** a supported success in my setup: the AP returned an Unsupported-Attribute NAK. I don't present Disconnect followed by a new login as a seamless VLAN switch.

## Omada was a different challenge

The next step was a **wired 802.1X Disconnect** for my Omada switch. It wasn't a matter of reusing the UniFi command. Initial Omada replies included a NAK; reducing the request to the attributes actually needed by the switch produced an authenticated **Disconnect-ACK**.

Then I hit a subtler problem: Omada could accept the Disconnect and start a new session without closing the old RADIUS Accounting row. On another attempt, the new Accounting-Start arrived just after the tool's original waiting window. Simply marking every old row as stopped would have hidden the problem and risked changing the wrong record.

I changed the logic to wait for a **verified ACK and a unique successor Accounting-Start for the same client and switch port** before closing the unchanged old row. The wait has a limit, and unknown outcomes are not automatically retried. I tested the completed behavior on two physical switch ports, one with a workstation and one with a domain controller. Both showed the expected new session and correctly closed previous record.

The per-device action is now available for eligible wired 802.1X sessions on the configured Omada switch, not an arbitrary switch, unknown port or whole-device reboot.

[The full Omada Accounting investigation →](../docs/pages/notes.html#omada-accounting)

## What I deliberately left alone

I found that targeted PMKSA cleanup on UniFi did not remove the separate **802.11r fast-transition keys**. A disabled identity is rejected at the next *full* EAP-TLS check, but that doesn't promise immediate deletion of every cached Wi-Fi key. I kept fast transition enabled for my personal network and documented the residual risk.

I also captured a TLS 1.2 login where the client offered a previous session ID but the server completed a full handshake. Complete authentications took around 0.16–0.27 seconds in those samples. I chose not to add persistent TLS session caching for a marginal speed gain and a new authorization edge case.

## The release, and what it doesn't prove

The final **v1.0.1** web release was deployed with all three containers reporting healthy, the authenticated-service checks passing, and **257 Python tests passed (one skipped)**. Responsive and localization checks ran in a browser with a *mock API*; that verifies layout, not a new production Disconnect. The live UniFi and Omada operations were tested separately during development.

The software release is complete. I still have an infrastructure maintenance task: my NAS has two interfaces in the same subnet, and the temporary route used for reliable access to OPNsense has not been proven persistent after a full NAS reboot. I won't call a healthy container restart a complete boot-recovery test.

This is my own operating tool, not a commercial product or a turnkey network-access package. It taught me as much about partial failures and careful accounting as it did about building the interface.

[Certificate-based network access →](../docs/pages/identity-pki.html) · [Switching and wired 802.1X →](../docs/pages/switching-wireless.html) · [Network working notes →](../docs/pages/network-v3.8.html)
