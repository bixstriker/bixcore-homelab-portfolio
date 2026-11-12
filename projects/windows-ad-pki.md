# Active Directory, Certificates and EAP-TLS

BiXCore has its own Windows domain and certificate infrastructure. I built it because I wanted to understand how devices can authenticate to a network using individual certificates, including what happens when one of the supporting services goes down.

## Building the domain

I run two Windows Server 2025 domain controllers, with replicated Active Directory and DNS. Adding the second controller meant checking replication, SYSVOL/DFSR, name resolution, authentication and the services that depend on them.

The enterprise certification authority and NDES service are hosted on one controller. I can fall back to the second controller for directory lookups, but that does not automatically give me a second CA or SCEP enrollment server.

## Certificates and authorization

The CA issues different types of certificates for Windows machines, domain controllers and managed Android devices. NDES provides SCEP enrollment for mobile clients. FreeRADIUS on OPNsense checks the certificate chain and revocation information, then makes a separate authorization decision.

I use local policies for certain infrastructure identities and LDAPS for eligible domain computer identities. I tested directory fallback with the primary controller unavailable, and verified wired and wireless EAP-TLS on the supported client types.

## Two certificate authorities and their revocation lists

Before I switched to the Windows enterprise CA, some managed Android devices already had client certificates from an earlier local CA. I kept that CA trusted during the migration so those devices could continue connecting.

When I enabled strict CRL checking in FreeRADIUS, those older devices stopped authenticating. Their certificates were still trusted, but the generated CA bundle contained the new CA's revocation list and not the old one's. The TLS validation failed because it could not find the matching CRL.

I created a valid CRL for the earlier CA and added a small helper to append it *after* OPNsense regenerates FreeRADIUS's certificate bundle. A startup/configuration hook reapplies that change when the plugin rebuilds its files. I then checked that both CRLs were present, identified their issuers and retested the older Android clients. EAP-TLS worked again with revocation checking still enabled.

The important lesson was that trusting a certificate issuer isn't enough when CRL checking is required: FreeRADIUS needs a usable revocation list for every issuing CA it accepts.

## CRL publication through the whole chain

On 5 November I checked that the revocation list produced by the Windows enterprise CA matched what the NAS served over HTTP and what OPNsense had loaded into its FreeRADIUS bundle. The checked stages agreed on the issuer, CRL revision and revocation entries.

I also fixed a failure-reporting bug in my PKI publication script. Previously, remote file comparison or replacement errors could be mistaken for a successful update. I tested error cases with temporary files and confirmed that the scheduled service-account run succeeded. This makes the publication result more trustworthy, but it's not a substitute for a tested CA restore.

## Testing certificate replacement and revocation

On 12 November I followed a managed Android client's certificate replacement beyond enrollment. The CA issued a new SCEP certificate, a scheduled task revoked the superseded one, and the refreshed CRL was published to the NAS and picked up in the FreeRADIUS trust bundle. I compared the actual CRL content at those stages. The phone then connected to Wi-Fi using its replacement certificate.

This is a verified end-to-end result for one device, not proof that every future certificate lifecycle event will be handled correctly. I also did not capture a separate RADIUS Access-Accept packet for that connection.

## Preventing two PKI publishing tasks from colliding

The revocation event started two PKI publication paths close together. They both used the same temporary filename on the NAS, and one task logged a missing-file error after the other moved it. A separate scheduled publication still succeeded, so the active CRL was not lost.

I gave the publisher a named mutex and a unique temporary filename for each transfer. A normal publish completed, and a controlled test showed a second run waiting for a held lock and then completing. I have not repeated a simultaneous two-writer test with changing certificate files.

[The PKI publication collision →](../docs/pages/notes.html#pki-publish-race)

## Problems I had to solve

### Domain controller on a protected switch port

A controller can need the network before it can contact the very directory services used for access decisions. I gave the controller's wired EAP-TLS identity its own appropriate certificate and authorization path, then checked the result against the switch and RADIUS.

[The bootstrap issue →](../docs/pages/notes.html#dc-eap)

### Checking LDAPS fallback

It wasn't enough to list a second LDAP endpoint in the configuration. I took the primary endpoint out of service and checked that authorization-related lookups could continue through the other controller.

[The failover test →](../docs/pages/notes.html#identity)

### IPv6 on a domain controller

The server's IPv6 DNS records looked right, but not all addresses were reachable. Packet inspection and the switch's ND security settings led to a fix for the addresses tested.

[The Neighbor Discovery problem →](../docs/pages/notes.html#omada-nd)

### Certificates don't maintain themselves

I set up certificate renewal and CRL publication, but I still want to improve how superseded mobile certificates are retired and test full recovery of the issuing CA.

[Android and Linux enrollment →](../docs/pages/linux-mobile-identity.html)

## What still needs attention

The directory failover test worked, but restoring the CA and NDES service from an independent backup is a different exercise. The switch's IPv6 neighbor bindings also need to be checked after future upstream prefix changes.

[The certificate-based access overview →](../docs/pages/identity-pki.html)   [Windows workstation policies →](../docs/pages/windows-policy-deployment.html)   [Monitoring and recovery →](../docs/pages/windows-monitoring-backup.html)

---
