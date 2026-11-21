# Building My Own RADIUS Session Management Tool

I originally built BiXCore RADIUS Control because I was tired of switching between the UniFi controller, RADIUS Accounting and OPNsense just to figure out which device was connected. My first attempt to disconnect a roaming phone used an old Session ID and failed. That was a useful reminder: a management tool should know what it is acting on, not just offer a button.

On **19 November 2026** I finished stable **v1.0.0** and deployed the **v1.0.1** responsive web interface. On **21 November**, the **v1.0.2 source/helper release** repaired UniFi control after the migration to RadSec. The NAS web, control and sync containers did not get new images in that maintenance release. The application runs on my NAS and manages selected FreeRADIUS and network-access operations through OPNsense. I kept the code private, but the design and results are worth documenting.

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

## Making the controls work again after moving to RadSec

A successful client EAP-TLS login wasn't the end of my RadSec migration. My own UniFi Disconnect initially stopped returning ACKs. The proxy also changed where Accounting Detail appeared: the proxy was now the transport sender, while the real AP remained the NAS identified inside the RADIUS record.

I updated the two restricted UniFi gateway helpers to accept only the known direct or proxy Accounting sources, and still require a unique matching AP, session, client MAC and identifier. I didn't turn this into a broad fallback that accepts whichever sender happens to answer.

The other problem was Dynamic Authorization (DAS): the APs were rejecting Disconnect requests under the old pre-RadSec secret assumptions. I traced that using the AP diagnostics and made the helpers verify the exact, active RadSec TLS client identity before selecting the corresponding, locally verified DAS setting. This is a control-plane check, separate from the EAP-TLS user certificate and from the proxy's backend secret.

**The v1.0.2 acceptance was real:** one UniFi phone received Disconnect-ACK and scoped PMKSA cleanup, then started a new Accounting session. A wired Omada workstation returned authenticated ACK with safe closure of the previous Accounting record after the new Start, leaving the domain-controller port alone. Another UniFi phone received an EAPOL reauthentication request, followed by a recorded Stop/Start. The suite reported **287 tests passed and one skipped**.

The **v1.0.2 release applies to the source and two OPNsense UniFi helpers**, not to newly built NAS Docker images. Web still runs the v1.0.1 image; the separate control and sync worker images also stayed unchanged. I did not restart FreeRADIUS, APs or the NAS containers for those helper changes.

These selected control tests were completed earlier on 21 November. The final RadSec certificate cleanup and restart happened later that evening, so I won't claim I repeated the full RADIUS Control acceptance suite after the final rollback.

[Why I moved the network to RadSec →](../docs/pages/radsec-mtls.html) · [The UniFi DAS investigation →](../docs/pages/notes.html#radsec-unifi-das)

## The release, and what it doesn't prove

The final **v1.0.1** web release was deployed with all three containers reporting healthy, the authenticated-service checks passing, and **257 Python tests passed (one skipped)**. Responsive and localization checks ran in a browser with a *mock API*; that verifies layout, not a new production Disconnect. The live UniFi and Omada operations were tested separately during development.

The software release is complete. I still have an infrastructure maintenance task: my NAS has two interfaces in the same subnet, and the temporary route used for reliable access to OPNsense has not been proven persistent after a full NAS reboot. I won't call a healthy container restart a complete boot-recovery test.

This is my own operating tool, not a commercial product or a turnkey network-access package. It taught me as much about partial failures and careful accounting as it did about building the interface.

[Certificate-based network access →](../docs/pages/identity-pki.html) · [Switching and wired 802.1X →](../docs/pages/switching-wireless.html) · [Network working notes →](../docs/pages/network-v3.8.html)
