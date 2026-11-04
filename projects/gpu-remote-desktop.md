# Intel GPU Passthrough and KRDP

I wanted a KDE virtual machine that could use the host's Intel graphics hardware and give me a usable Full HD remote desktop. It took several attempts to get the GPU, display mode and desktop session to cooperate.

## Getting the Intel GPU into the VM

After the CPU upgrade and VT-d checks, I passed the Intel integrated GPU through to the Linux guest. The early attempts kept an additional virtual graphics adapter alongside the Intel device, which led to KWin hangs and page-flip timeouts.

The stable arrangement uses the passed-through Intel GPU without a competing virtual display adapter.

## Why the desktop stayed at low resolution

The guest could start, but it did not get a usable Full HD display mode. The kernel logs pointed to a missing EDID firmware file. I provided an EDID for 1920 × 1080 and made sure it was available during early boot. That fixed the resolution problem.

KRDP then had two separate issues. A KWallet interaction affected login after enabling automatic desktop login, while the remote image quality setting was responsible for a poor-looking picture. Both were adjusted and the remote session worked after a reboot.

## What I verified about hardware encoding

The Intel graphics device worked for the guest, and I independently tested **hardware H.264 encoding through FFmpeg**. KRDP also reported VA-API use, and remote desktop worked at Full HD.

There is one measurement I couldn't make inside this VM: the virtual environment did not expose the GPU video-engine counters needed to see how much of KRDP's actual encoding workload went through Quick Sync. So hardware encoding capability is confirmed; per-frame KRDP hardware utilization was not measured.

## What I would do differently

Next time I would first test the guest's display mode and EDID, then check the remote desktop settings, instead of changing several graphics devices together. The current lab setup also uses a convenience-oriented desktop login, which I would not copy unchanged to a more exposed machine.

[The graphics troubleshooting case →](../docs/pages/notes.html#gpu)   [The Proxmox host →](../docs/pages/proxmox-host-storage.html)

---
