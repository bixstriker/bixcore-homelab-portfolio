# Moving My Wi-Fi and Wired 802.1X Authentication to RadSec

Until November, my certificate-based Wi-Fi and wired 802.1X already worked. Clients had their own EAP-TLS identities, FreeRADIUS checked them, and I could follow the sessions in Accounting. What I wanted to change was **the RADIUS transport between my network devices and the gateway**. I didn't want that part of the journey to stay on ordinary RADIUS/UDP.

On 21 November 2026, I got **RADIUS over TLS (RadSec)** working with two UniFi Wi-Fi 7 access points and my TP-Link Omada switch. It took considerably more than turning on TLS.

## Two different layers of certificates

I run the OPNsense RadSecProxy plugin in front of FreeRADIUS. The access points and switch connect to the proxy over TLS 1.3, and the proxy forwards authentication and Accounting to FreeRADIUS. FreeRADIUS continues to make the actual EAP-TLS authorization decisions.

That distinction matters. **Transport mTLS** identifies the AP or switch to RadSecProxy and lets the network device check the proxy. **Client EAP-TLS** is a separate authentication inside that transport. My Windows/Android client certificates, domain checks and CRL policy did not need to be replaced just because I secured the RADIUS transport.

The two UniFi APs were the more straightforward part. I verified TLS 1.3 connections, client authentication and Accounting. The wired switch was not so cooperative.

## Why Omada kept rejecting my certificates

With certificate verification enabled on Omada, the switch repeatedly rejected server certificates issued by my own experimental CA. I tried a new root CA, then another root and intermediate chain, reissued server certificates and checked the chain with OpenSSL on my computers and the gateway. The switch still rejected it.

An OpenSSL verification result on a PC was useful evidence, but it wasn't proof the Omada firmware would accept the same chain. I couldn't get the exact X.509 verification error from the switch, so I don't know which particular extension or firmware rule caused those failures. Reissuing yet another certificate without that evidence didn't seem productive.

I eventually used a **Let's Encrypt certificate for the RadSecProxy server identity**, with a trusted public CA bundle on Omada. I left Omada's `verify enable` setting on. That solved the server-certificate part of the handshake, but the first attempt to return to the working setup exposed a second issue: RadSecProxy couldn't build a trusted chain for the switch's **client** certificate. This time the proxy gave me a useful X.509 issuer error.

The final arrangement uses the public Let's Encrypt chain for **server authentication** and my existing separate RadSec CA for **Omada client authentication**. Those are two distinct trust directions. Once I restored the right client CA, the switch completed TLS 1.3 and FreeRADIUS returned Access-Accept.

I removed the temporary CA and certificate experiments and kept the tested, working profiles. Both UniFi access points remained on their separate working TLS profile.

## What I tested, rather than just configured

I checked the TLS connection and Access-Accept on Omada with certificate verification still enabled. Accounting was observed on the working RadSec path; both UniFi access points also had tested TLS 1.3, EAP-TLS and Accounting. Importantly, I didn't treat the old Accounting records from before the transport change as evidence of a current failure. Those old sessions had their own history and were handled separately.

After the last certificate rollback I deliberately restarted RadSecProxy using the custom service action. The service came back on its TLS listener, a new handshake used the intended public certificate, and I confirmed another successful wired client login. I didn't have to restart FreeRADIUS or change the clients' EAP-TLS policy for that check.

## Certificate renewal: one test is still missing

I connected the existing ACME certificate to two actions: restart FreeRADIUS and restart RadSecProxy after renewal. OPNsense's built-in action list didn't expose a suitable RadSecProxy restart command in the ACME selector, so I registered a small named configd action instead of patching the plugin itself. I tested that action with a real service restart.

**This does not yet prove the whole renewal path.** RadSecProxy uses an exported PEM file. The first natural ACME renewal still needs to show that the renewed certificate actually reaches that file *before* the service comes back, with an updated fingerprint and a working TLS login. I have not forced an early renewal simply to make the portfolio claim look complete.

## What this changed elsewhere

Moving the APs to RadSec also exposed a problem in my own [RADIUS Control tool](../docs/pages/radius-control.html). Accounting Detail was now filed under the proxy's source rather than the AP's original transport source, and UniFi's Disconnect service did not accept the previous configuration. I adapted the helper checks and tested Disconnect, PMKSA cleanup and reauthentication with real clients. That was a separate source/helper maintenance release, **v1.0.2**, not a replacement of the NAS web containers.

Those RADIUS Control tests happened earlier on 21 November, before the last late-evening RadSec certificate cleanup and restart. They confirm the control path after the migration, but I haven't independently repeated the whole control regression suite after the final evening change.

The result is a working encrypted RADIUS transport for my two Wi-Fi APs and wired switch, with a clear understanding of what I verified and what will need attention at the next real certificate renewal.

[The Omada certificate investigation →](../docs/pages/notes.html#radsec-omada-certificate) · [RADIUS Control after RadSec →](../docs/pages/notes.html#radsec-unifi-das) · [Certificate-based network access →](../docs/pages/identity-pki.html)
