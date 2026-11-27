# Zenarmor inspection performance on the N305

## What I wanted to measure

I wanted to know whether using more CPU cores would raise inspection throughput on my Intel N305 gateway. I already had 10GbE network interfaces, and I planned to compare ordinary routing, single-core inspection and multi-core inspection with the same clients and traffic generator.

On 27 November I tried Zenarmor 2.7.4 on OPNsense 26.7.9_3, varying native and emulated Netmap, the number of workers and selected L3 settings. I used iperf as part of the experiments. Stability became the more important question before I could finish a meaningful benchmark.

## What happened during testing

Several configurations caused kernel panics or loss of the inspection process. My investigation recorded **seven crash dumps and two further failures without a new dump**. In native Netmap I also saw uplink flaps and increasing receive-miss counters. Some multi-worker configurations exhausted buffers or respawned after a segmentation fault.

A repeating kernel stack included `generic_mbuf_dtor`, `mb_free_ext` and `iflib_completed_tx_reclaim`. Together with the Netmap lifecycle and buffer messages, it suggests a problem in the interaction between the FreeBSD networking stack, driver framework, Netmap and the inspection engine. I cannot assign a proven root cause to Zenarmor or the NIC driver from these observations alone.

## Returning to the working mode

I returned to routed Emulated Netmap with multi-core disabled. The two logical worker mappings cover separate interfaces; they are not evidence that multi-core inspection is enabled. Suricata remains separate on PF divert-to. I restored the intended Netmap ring size through the OPNsense tunables interface and checked the allocated buffer pool.

The gateway returned to service in this fallback, and I subsequently verified a narrow TLS inspection pilot. I am not going to run more disruptive native Netmap or multi-core experiments on the production gateway before the crash evidence has been investigated. I have not performed a long stress test or another reboot after the final inspection changes.

## The benchmark is still a plan, not a result

I have no defensible multi-core versus single-core speed comparison. For a future comparison I want to record the exact engine and interface settings, establish a routing baseline, repeat equal TCP/UDP workloads at several packet sizes, and measure throughput, latency, loss and per-core CPU use. Thermal conditions and other gateway services also matter.

The link rate alone does not tell me the inspection rate. The useful result of this session was identifying a reproducible stability boundary and returning the firewall to a workable configuration, rather than producing a misleading performance number.

[The crash case →](../docs/pages/notes.html#zenarmor-netmap) · [TLS inspection tests →](../docs/pages/zenarmor.html) · [Remaining work →](../docs/pages/roadmap.html)
