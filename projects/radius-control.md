# Building My Own RADIUS Session Management Tool

I already had FreeRADIUS handling certificate-based Wi-Fi, but managing one connected device still meant moving between the access point, accounting records and OPNsense. After I tried to disconnect a phone using an old session ID, I wanted a better way to see what was actually connected before touching it.

I built **BiXCore RADIUS Control** for that job. It's a small FastAPI application running in Docker on my NAS, connected to the existing FreeRADIUS service on OPNsense.

## What I wanted it to do

The interface brings current, ended and stale RADIUS Accounting sessions into one place. I can refresh the data, find a particular device and request a targeted action. It also shows local FreeRADIUS users and Captive Portal sessions.

I can enable or disable **local RADIUS accounts** and change their configured VLAN. That is deliberately different from domain-backed clients: for AD/LDAP devices I can view their sessions and disconnect a specific connection, **not** disable a directory account or change its permissions. Guest portal accounts have their own separate controls.

## Keeping a small tool from becoming a big privilege

The web container reads a filtered snapshot rather than a raw gateway configuration. Specific actions go through restricted helpers on the NAS and OPNsense; the target session is checked again before a request is sent. For UniFi operations, the access-point key stays on the NAS host, outside the web container.

The tool refuses ambiguous targets or reports a partial result if something changes during an operation. I preferred that to a green success message for a command that might have acted on the wrong session.

## Tests on real phones

By 16 November 2026, version **0.10.3** had passed selected tests on my two UniFi access points.

- **Reauthentication:** A targeted EAPOL reauthentication request worked. After one early attempt the phone left the access point about 30 seconds later; subsequent attempts did not interrupt Wi-Fi. I cannot prove why the earlier departure happened.
- **Online Disconnect:** The AP acknowledged the request, the phone disconnected and completed EAP-TLS again.
- **Offline cleanup:** I checked and cleared old PMKSA state without pretending the phone still had a live session.

I also tightened the underlying FreeRADIUS authorization policy and checked its behavior. Disabling a local identity led to **Access-Reject** on a new full EAP-TLS login; enabling it again allowed the phone to join. An identity that didn't match the certificate, and a certificate without a permitted matching local account, both failed new login tests. The guest portal refused a second simultaneous login to the same personal account.

Changing an active UniFi client's VLAN was another experiment. The CoA request received an **Unsupported-Attribute NAK**; I didn't get a live VLAN reassignment.

## The Wi-Fi cache was the interesting part

A Disconnect and PMKSA cleanup do not necessarily remove everything a Wi-Fi access point remembers. I inspected the separate **802.11r fast-transition (FT)** entries on both UniFi APs and found they were still there after PMKSA cleanup. On the tested firmware I did not find a safe, proven way to remove only one phone's FT entries.

This puts a limit on the word *disabled*. A disabled identity is refused at its next **full** EAP-TLS login, but I cannot promise that all previously established fast-transition keys immediately disappear. The tool doesn't claim to do that.

I also captured a TLS 1.2 login in which the phone offered an old session ID but FreeRADIUS completed a new handshake. The full authentications took about 0.16–0.27 seconds. Rather than introduce persistent session caching and another authorization edge case for a small speed gain, I left it off.

Almost all regular clients here are personal devices, and guests use a separate network. I decided to leave 802.11r enabled and document the remaining limitation rather than force global cache flushes or AP restarts.

## What is still open

These are real tests on selected clients, not proof of behavior on every device or firmware. I still want to check the custom FreeRADIUS policy after a full gateway reboot and test more AD computer authorization cases. The code and operational settings live in a private repository; this public article is about the design and results, not a deployment guide.

[Certificate-based Wi-Fi](../docs/pages/identity-pki.html) · [Switching and UniFi](../docs/pages/switching-wireless.html) · [Network project index](../docs/pages/network-v3.8.html)
