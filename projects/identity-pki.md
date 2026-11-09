# Certificate-Based Network Access

I wanted wired and Wi-Fi clients to use individual certificates instead of a shared network password. Getting that to work meant dealing with enrollment, trusted CAs, revocation and directory-backed authorization.

## How the pieces fit together

Windows Server provides Active Directory and an enterprise certification authority. NDES handles SCEP for supported Android devices. FreeRADIUS runs on OPNsense and checks the client certificate before applying the relevant access policy at the switch or wireless access point.

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

## Problems and the next stage

The trickiest parts were [getting a domain controller through its own protected switch port](../docs/pages/notes.html#dc-eap), [proving LDAPS fallback](../docs/pages/notes.html#identity) and [understanding extra SCEP enrollment requests from Android](../docs/pages/notes.html#android-scep).

Now I want to make the certificate lifecycle more predictable: renewals, revocation of old device identities and recovery of the CA itself. The second domain controller helps directory queries, but it doesn't replace that work.

[Windows Server and CA details →](../docs/pages/windows-ad-pki.html)   [Linux and Android clients →](../docs/pages/linux-mobile-identity.html)

---
