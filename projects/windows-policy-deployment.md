# Managing Windows with Group Policy

Once I joined more Windows machines to Active Directory, I wanted common settings and administration tools to follow them automatically. I use Group Policy to make that repeatable instead of configuring every PC from scratch.

## Moving existing PCs into the domain

I didn't want to lose years of local user profiles while joining the Windows PCs to Active Directory. I used ForensiT User Profile Wizard to associate existing profiles with domain accounts, then checked that the desktop, applications and files still belonged to the right user.

One migration wasn't smooth: Windows loaded a temporary profile because of an old ProfileList entry and permissions on the profile's user data. I corrected the registry mapping and file permissions, then verified that normal sign-in worked. I kept that recovery sequence in the working notes for future PC migrations.

## Workstation policies

The policies cover domain organisation, managed local administrator passwords with Windows LAPS, machine certificate enrollment, wired EAP-TLS settings and selected user preferences. I also adjusted the domain password-aging policy and checked the resulting configuration on both domain controllers.

I also changed the keyboard-layout policies so they add only missing input methods instead of overwriting each user's preferred order or extra layouts. The script checks succeeded on selected machines and both controllers; the sign-in-screen language selector still needs a visual follow-up after a fresh logon.

## Remote administration

I configured Kerberos-based PowerShell remoting through WinRM and tested several workstation-to-workstation and workstation-to-server connections. That is separate from RDP access: the target still needs the right authorization rules for the task being performed.

## Tools I deploy centrally

- **PowerShell 7.7:** I replaced the earlier MSI deployment with a verified ZIP package distributed through the existing GPO and SYSTEM task. The script checks the package hash, registers the remoting endpoint, and skips reinstalling a matching version. Six Windows machines were checked; some startup-trigger behavior still needs a reboot test.
- **Sysinternals and RSAT:** centrally distributed tools, with RSAT limited to the designated administration machine.
- **Windows Admin Center:** HTTPS setup and certificate/HTTP.sys troubleshooting, not just installation of the web console.
- **Sysmon:** installed with a managed configuration and scheduled deployment tasks; the events are useful for investigation, although I haven't built a complete SIEM.
- **RustDesk 1.5.3:** the existing GPO now checks the installed version, verifies the package signature/hash and follows the correct MSI or EXE upgrade path. I tested both types of installation without replacing the self-hosted server configuration.

## WireGuard that connects only when I'm away

On a Windows laptop, I set up WireGuard to start automatically when the machine is outside the home network and disconnect when it comes back. A PowerShell script checks the active physical network interfaces and is triggered by Windows startup and network-change events. The tasks run as SYSTEM, so the tunnel can come up before a user signs in.

I tested home Wi-Fi and Ethernet, switching to a phone hotspot, returning home, a restart while away and manual control through the WireGuard app. The script also remembers the current network state so it doesn't immediately undo a manual disconnect. I did see overlapping connect events in the logs, which is worth checking further.

## One RustDesk upgrade that stalled

On one workstation an MSI update returned error 1603. The EXE upgrade installed the new client, but the deployment script waited for RustDesk child processes and never finished cleanly. I changed the wait logic to target the installer process and verify the actual installed version. The next manual run completed. I kept this as a deployment-script problem rather than changing the remote-support server.

[The deployment investigation →](../docs/pages/notes.html#rustdesk-upgrade)

## Problems and follow-up work

Some of these took a few iterations. The PowerShell installation method had to change, and [Windows Admin Center needed its HTTPS listener checked](../docs/pages/notes.html#wac). The RustDesk update worked on the Windows machines available for testing, including MSI and EXE installations. One powered-off workstation still needs its upgrade checked when it is next used.

I also want to validate more combinations of source and destination for PowerShell remoting and keep checking that policy-driven installs behave correctly after a rebuild. Those are practical follow-up tests, not missing descriptions of the deployment itself.

[Active Directory and certificates →](../docs/pages/windows-ad-pki.html)   [Windows monitoring and backups →](../docs/pages/windows-monitoring-backup.html)

---
