# Certificate-Based Network Access

I wanted wired and Wi-Fi clients to use individual certificates instead of a shared network password. Getting that to work meant dealing with enrollment, trusted CAs, revocation and directory-backed authorization.

## How the pieces fit together

Windows Server provides Active Directory and an enterprise certification authority. NDES handles SCEP for supported Android devices. FreeRADIUS runs on OPNsense and checks the client certificate before applying the relevant access policy at the switch or wireless access point.

## Moving the RADIUS transport to TLS

I later put RadSecProxy in front of FreeRADIUS for my two UniFi access points and wired Omada switch. This encrypts and authenticates the **RADIUS transport**, not the certificate identity used by the Windows, Linux or Android client inside EAP-TLS.

Both UniFi and Omada completed TLS 1.3 sessions with the gateway, and I verified authentication and Accounting. Omada needed a trusted public server chain while the gateway kept a separate CA for the switch's client certificate; I left switch-side server verification enabled. I did not replace the client's enterprise CA, LDAPS or revocation checks as part of this change.

[Why I used RadSec and how I fixed Omada trust →](../docs/pages/radsec-mtls.html)

## What I have tested

- Certificate enrollment and wired EAP-TLS for selected Windows machines.
- Wired and Wi-Fi certificate authentication on Kubuntu.
- Android MDM profiles issuing SCEP identities and using them for enterprise Wi-Fi.
- Revocation-list publication and selected certificate-validation checks.
- LDAPS directory lookup using the second controller while the first was unavailable.
- A separate wired certificate/authorization design for the domain controllers, avoiding a bootstrap dependency on their own directory service.

## RADIUS Accounting and one targeted Disconnect

On 7 November I added RADIUS Accounting for my UniFi access points to the existing FreeRADIUS setup. I checked the session records and updates in its local database. My first Disconnect-Request was rejected because I used a session identifier that was no longer valid after Wi-Fi roaming.

With the current session information, the next request returned a Disconnect-ACK. The phone disconnected and authenticated again over EAP-TLS. This proves targeted session termination, **not** a dynamic VLAN change without disconnecting.

[The roaming/CoA incident →](../docs/pages/notes.html#radius-coa)

## When a disabled identity actually gets rejected

In November I tested stricter FreeRADIUS authorization with real phones. Disabling a local account gave an Access-Reject at its next full EAP-TLS login; enabling it again restored access. A mismatched EAP identity, and a certificate without a permitted matching local record, were also denied at new login.

My RADIUS Control tool added targeted reauthentication and Disconnect operations. It also exposed a limitation: after PMKSA cleanup, separate 802.11r fast-transition keys remained on the APs. A new full authentication checks the current access policy, but I don't claim instant revocation of every previously cached wireless key.

I also attempted live VLAN reassignment with CoA. The UniFi AP replied with an Unsupported-Attribute NAK; it did not move the client between VLANs.

[The RADIUS Control project →](../docs/pages/radius-control.html)

## Managing a wired session without managing the domain account

I extended my RADIUS Control tool to individual **wired 802.1X sessions on Omada**. It independently checks the live client and port, asks for Disconnect and closes the old Accounting row only after a verified ACK and a matching new session. Both a workstation and a domain controller passed the live test on separate ports.

The tool still **does not disable or change Active Directory accounts**. It handles the selected network session only. The EAP-TLS certificate rules remain separate, as do the previously documented Wi-Fi FT-cache limitations.

[The finished RADIUS Control project →](../docs/pages/radius-control.html)

## Problems and the next stage

The trickiest parts were [getting a domain controller through its own protected switch port](../docs/pages/notes.html#dc-eap), [proving LDAPS fallback](../docs/pages/notes.html#identity) and [understanding extra SCEP enrollment requests from Android](../docs/pages/notes.html#android-scep).

Now I want to make the certificate lifecycle more predictable: renewals, revocation of old device identities and recovery of the CA itself. The second domain controller helps directory queries, but it doesn't replace that work.

[Windows Server and CA details →](../docs/pages/windows-ad-pki.html)   [Linux and Android clients →](../docs/pages/linux-mobile-identity.html)

---
