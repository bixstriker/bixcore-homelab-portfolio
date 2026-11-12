# Linux and Android on the Same PKI

Getting certificate-based network access working on Windows was only part of the project. I also wanted Kubuntu and Android devices to join the same enterprise Wi-Fi without sharing a password, and each platform needed a different enrollment approach.

## Kubuntu and Active Directory

I joined a Kubuntu workstation to the domain using realmd, SSSD and Kerberos, then checked domain account and group resolution. Wired and wireless NetworkManager profiles use managed EAP-TLS client certificates. I also set up certificate renewal automation and tested the resulting connection behavior.

I kept a separate local administrator account so that a directory or network problem wouldn't leave me without a recovery path. The Linux setup also has its own login-session and WireGuard integration notes.

## A dual-boot laptop and a KRDP login problem

On my physical Windows/Kubuntu laptop, I kept GRUB as the first UEFI entry but set the menu to boot Windows by default after a short timeout. I verified the result with a real restart.

I also tracked down an RDP login failure to how the Windows client passed the domain-style Linux username. TLS connected, but KRDP showed a black screen and disconnected. Using the full Linux UPN in a saved RDP connection with the appropriate local-account prefix worked; I haven't claimed that I proved the internal parser bug. I renewed the separate, self-signed KRDP TLS certificate and tested SSH key authentication from Windows using Ed25519. None of these certificates or keys replaces the EAP-TLS Wi-Fi identity.

[The KRDP login investigation →](../docs/pages/notes.html#krdp-credentials)

## Android and managed certificates

For Android, I used mobile device management with SCEP enrollment through the internal NDES service. The managed profile installs the relevant trust material and a client identity, which Android can then use for EAP-TLS Wi-Fi. I tested that on multiple devices, including work-profile scenarios.

One surprise was that applying the Wi-Fi configuration could trigger another SCEP request. I investigated that as part of the profile workflow rather than assuming Wi-Fi authentication was broken. The devices connected successfully.

## Renewal and cleanup

On Kubuntu, I have a documented certificate renewal process. I also tested an Android SCEP replacement in which the old certificate was revoked and the updated CRL reached FreeRADIUS. That is a useful single-device result, although I still need to cover more renewal and recovery scenarios.

The Proxmox host has its own Active Directory and HTTPS integration; I cover that under [the virtualization setup](../docs/pages/proxmox-host-storage.html) rather than mixing it into the workstation enrollment story.

[The extra Android SCEP request →](../docs/pages/notes.html#android-scep)   [How EAP-TLS works in BiXCore →](../docs/pages/identity.html)

---
