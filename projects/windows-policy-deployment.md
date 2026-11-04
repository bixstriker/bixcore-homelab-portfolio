# Managing Windows with Group Policy

Once I joined more Windows machines to Active Directory, I wanted common settings and administration tools to follow them automatically. I use Group Policy to make that repeatable instead of configuring every PC from scratch.

## Moving existing PCs into the domain

I didn't want to lose years of local user profiles while joining the Windows PCs to Active Directory. I used ForensiT User Profile Wizard to associate existing profiles with domain accounts, then checked that the desktop, applications and files still belonged to the right user.

One migration wasn't smooth: Windows loaded a temporary profile because of an old ProfileList entry and permissions on the profile's user data. I corrected the registry mapping and file permissions, then verified that normal sign-in worked. I kept that recovery sequence in the working notes for future PC migrations.

## Workstation policies

The policies cover domain organisation, managed local administrator passwords with Windows LAPS, machine certificate enrollment, wired EAP-TLS settings and selected user preferences. I also adjusted the domain password-aging policy and checked the resulting configuration on both domain controllers.

## Remote administration

I configured Kerberos-based PowerShell remoting through WinRM and tested several workstation-to-workstation and workstation-to-server connections. That is separate from RDP access: the target still needs the right authorization rules for the task being performed.

## Tools I deploy centrally

- **PowerShell 7:** a managed MSI installation after moving away from an earlier package approach that caused problems.
- **Sysinternals and RSAT:** centrally distributed tools, with RSAT limited to the designated administration machine.
- **Windows Admin Center:** HTTPS setup and certificate/HTTP.sys troubleshooting, not just installation of the web console.
- **Sysmon:** installed with a managed configuration and scheduled deployment tasks; the events are useful for investigation, although I haven't built a complete SIEM.
- **RustDesk:** a self-hosted support setup, with an MSI/GPO process that can install or update the client and refresh its configuration.

## WireGuard that connects only when I'm away

On a Windows laptop, I set up WireGuard to start automatically when the machine is outside the home network and disconnect when it comes back. A PowerShell script checks the active physical network interfaces and is triggered by Windows startup and network-change events. The tasks run as SYSTEM, so the tunnel can come up before a user signs in.

I tested home Wi-Fi and Ethernet, switching to a phone hotspot, returning home, a restart while away and manual control through the WireGuard app. The script also remembers the current network state so it doesn't immediately undo a manual disconnect. I did see overlapping connect events in the logs, which is worth checking further.

## Problems and follow-up work

Some of these took a few iterations. The PowerShell installation method had to change, and [Windows Admin Center needed its HTTPS listener checked](../docs/pages/notes.html#wac). The RustDesk deployment was exercised on both an existing installation and a fresh install, but the latter still had an outstanding GUI readiness check in the source notes.

I also want to validate more combinations of source and destination for PowerShell remoting and keep checking that policy-driven installs behave correctly after a rebuild. Those are practical follow-up tests, not missing descriptions of the deployment itself.

[Active Directory and certificates →](../docs/pages/windows-ad-pki.html)   [Windows monitoring and backups →](../docs/pages/windows-monitoring-backup.html)

---
