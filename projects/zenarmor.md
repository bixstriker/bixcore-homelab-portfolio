# Working with Zenarmor on OPNsense

## What I already use

I use Zenarmor for application and web-category filtering alongside OPNsense. I have tested a controlled category block on a client. Suricata is a separate IPS, and I have independently verified a controlled signature drop. Its current inspection path uses PF divert-to, not the Netmap interfaces that Zenarmor uses.

## Trying full TLS inspection with my own CA

On 27 November I gained access to the advanced Zenarmor features and tried full TLS inspection on two selected websites, not on all traffic. I issued a dedicated subordinate inspection CA from my existing Windows AD CS enterprise root. The root private key remained on the CA server. The subordinate certificate had CA constraints, a zero path-length limit and the Server Authentication extended key usage. Its chain and revocation checks passed on Windows.

The first import failed because I had placed the certificates in the wrong order. After correcting that, the root, intermediate and corresponding intermediate key were accepted. I verified the actual CA used by the inspection engine instead of assuming that the certificate shown in one GUI field was the active issuer.

On my test browser the selected HTTPS connections presented certificates issued by the BiXCore inspection CA. Zenarmor Live Sessions showed TLS-Inspected, including IPv6 connections. The pilot covered TCP-based HTTPS; I used the application policy to block QUIC during the test so the browser could use TCP instead of HTTP/3. I did not enable category-wide inspection or guest-network inspection.

## Why some HTTPS connections bypassed the policy

The site-specific rule looked correct, yet the browser sometimes received the original public certificate rather than the local issuer. I isolated a reproducible difference: enabling the option to exclude flows without DNS enrichment data made the selected connections bypass inspection; disabling that exclusion restored it.

My normal DNS path uses AdGuard Home on the NAS and Unbound on the gateway. It would have been easy to blame the separate DNS server. Instead, I temporarily pointed the Windows client at Unbound directly, then repeated the experiment with a DNS query and TLS connection bound to the same source address. The browser still received the public certificate with the exclusion enabled. I restored the normal DNS configuration.

This established the effect of the policy option, not the reason Zenarmor lacked the enrichment information. I have not isolated the effect of the separate certificate-pinning exclusion either. I am keeping the pilot results separate from any claim about decrypting every application.

## Performance and stability

The N305 gateway has 10GbE interfaces, but that says nothing about inspection throughput. My multi-core and Netmap experiments on 27 November exposed serious stability problems, so I returned to routed Emulated Netmap without multi-core. The two-domain TLS pilot succeeded with that fallback. I have no reliable comparative throughput numbers or long-running stress-test result after the final changes.

[The multi-core investigation →](../docs/pages/zenarmor-multicore.html) · [DNS enrichment case →](../docs/pages/notes.html#zenarmor-dns-enrichment) · [My next tests →](../docs/pages/roadmap.html#zenarmor-plans)
