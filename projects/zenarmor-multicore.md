# Zenarmor inspection performance on the N305

I want to find out what happens to throughput and latency when traffic inspection is enabled on the gateway, and whether using more CPU cores changes the result. I haven't measured it yet.

## The setup I want to compare

First I'll check the throughput of ordinary routing with the same clients and traffic generator. Then I'll enable Zenarmor inspection and repeat the runs under the same conditions. If the multi-core engine is available, I'll compare that too.

## Measurements

1. Record OPNsense and Zenarmor versions, inspected interfaces, policy settings, NIC offload options and the active feature set.
2. Check that the traffic generator and receiver are fast enough to avoid limiting the test.
3. Try several packet sizes, connection counts and TCP/UDP traffic mixes.
4. Record throughput, latency, jitter, packet loss and CPU use per core.
5. Where relevant, repeat tests with policy rules enabled and check that their decisions remain consistent.
6. Run each configuration several times and note thermal behavior and other background load on the gateway.

## Why the distinction matters

My gateway's 10GbE ports describe what the network interfaces support, not how quickly the inspection engine can process packets. Testing the same traffic with and without inspection should give me a more useful picture than the interface speed alone.

[Other Zenarmor experiments →](../docs/pages/zenarmor.html)   [All upcoming projects →](../docs/pages/roadmap.html)

---
