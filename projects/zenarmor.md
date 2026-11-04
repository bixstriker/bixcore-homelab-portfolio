# Working with Zenarmor on OPNsense

I use Zenarmor alongside the firewall and Suricata on my OPNsense gateway. It started as another way to understand and control the traffic moving through the network. I want to explore the more advanced inspection features as well, using separate test clients.

## What I've already tested

Zenarmor is running on the gateway, and I have checked that a test client was blocked by a restricted web-category policy. I also checked the engine and service state after an OPNsense update. Those tests showed that the configured policy was working in that situation.

Suricata runs separately as the IPS. I've also triggered a controlled Suricata block, but that is a different test from Zenarmor's category filtering.

## Encrypted connections

One area I'm particularly interested in is the difference between inspecting TLS connection metadata and decrypting HTTPS content. Lightweight inspection can work with information visible during the TLS handshake. Full TLS inspection goes further and needs the test client to trust an inspection CA.

If I can use full TLS inspection in the lab, I'll try it on my own test devices. I want to see how the browser behaves, where certificate pinning causes problems, what changes with QUIC or encrypted client hello, and how to exclude sites that shouldn't be decrypted. The aim is to understand both the visibility it provides and the complications it introduces.

## Policies and reports

I'd like to compare web-category rules, application filtering and exceptions across a few different test clients. I'd also like to understand how accurately the live-session view and reports explain why a connection was allowed or blocked.

For controlled tests I can compare the client's result, Zenarmor's logs and, where relevant, Suricata events. That should make it easier to spot the difference between a rule behaving as expected and a client failing for some unrelated reason.

## How much traffic can the gateway inspect?

The Intel N305 appliance has 10GbE interfaces, but the link speed doesn't tell me how much traffic Zenarmor can inspect. I want to establish a routing baseline, then compare throughput, latency and CPU use with inspection enabled. A multi-core comparison is another part of that work if the feature is available.

There are no benchmark numbers yet. I keep the proposed measurements in a [separate performance test plan](../docs/pages/zenarmor-multicore.html) rather than mixing them into the results of the filtering tests I've already completed.

[All Zenarmor plans →](../docs/pages/roadmap.html#zenarmor-plans)   [OPNsense and IPv6 →](../docs/pages/opnsense-ipv6.html)   [Zenarmor TLS documentation →](https://www.zenarmor.com/docs/opnsense/policies/tls-inspection-rules)

---
