# Windows Server Master v2.7: Project Index

The Windows Server notes grew as I added the second domain controller, built the PKI and automated more of the client setup. This index connects the original work and later changes to the related articles.

| Section | Work | Status | Read more |
| --- | --- | --- | --- |
| I.01 | Current directory roles, DNS/time and system topology | Operational | [Active Directory and PKI](../docs/pages/windows-ad-pki.html) |
| I.02 | AD OUs, groups, GPOs, Windows LAPS and desktop policies | Operational / selected checks | [Windows deployment and GPO](../docs/pages/windows-policy-deployment.html) |
| I.03 | Enterprise AD CS/CRL and NDES certificate issuance | Observed specific flows | [Active Directory and PKI](../docs/pages/windows-ad-pki.html) |
| I.04 | FreeRADIUS and AD local-first/LDAPS authorization design | Observed selected tests | [Active Directory and PKI](../docs/pages/windows-ad-pki.html) |
| I.05 | Windows/Kubuntu/Android certificate-based client identity | Observed selected clients | [Linux and Android enrollment](../docs/pages/linux-mobile-identity.html) |
| I.06 | NAS integration, SMB and backup storage | Operational / backup checks | [Monitoring and backups](../docs/pages/windows-monitoring-backup.html) |
| I.07 | WinRM, WAC, Sysmon and administration workflows | Observed selected tests | [Windows deployment and GPO](../docs/pages/windows-policy-deployment.html) |
| I.08 | Related monitoring and infrastructure applications | Observed selected integrations | [Monitoring and backups](../docs/pages/windows-monitoring-backup.html) |
| II.09 | Recovery runbooks for AD/PKI/clients | Runbook | [Monitoring and backups](../docs/pages/windows-monitoring-backup.html) |
| II.10 | Second domain-controller introduction | Observed replication and service checks | [Active Directory and PKI](../docs/pages/windows-ad-pki.html) |
| III.11 | Change history and superseded decisions | Recorded | [How the lab changed](../docs/pages/working-notes.html#changes-over-time) |
| III.12 | Original historical document registry | Private provenance | [Original working files](../docs/pages/working-notes.html#keeping-source-files) |
| III.13 | Second controller integration and DNS role testing | Observed | [Active Directory and PKI](../docs/pages/windows-ad-pki.html) |
| III.14 | LDAPS failover and wired EAP-TLS on a domain controller | Observed controlled failure | [LDAPS failover test](../docs/pages/notes.html#identity) |
| III.15 | DC-specific wired certificate and EAP-TLS migration | Observed | [Active Directory and PKI](../docs/pages/windows-ad-pki.html) |
| III.16 | IPv6 Neighbor Discovery security failure and restoration | Observed specific address tests | [Switching, Wi-Fi and 802.1X](../docs/pages/switching-wireless.html) |
| III.17 | Proxmox AD, trusted HTTPS and LDAP integration | Observed selected checks | [Proxmox host and storage](../docs/pages/proxmox-host-storage.html) |
| III.18 | Domain account-password aging policy change | Observed on two controllers | [Windows deployment and GPO](../docs/pages/windows-policy-deployment.html) |
| III.19 | NIC reset during System State backup, driver update and end-to-end CRL publication checks | Backup jobs later reported successful; CA restore untested | [Monitoring and backups](../docs/pages/windows-monitoring-backup.html) |
| IV.01 | Initial AD infrastructure guide | Historical source | [Active Directory and PKI](../docs/pages/windows-ad-pki.html) |
| IV.02 | Directory extension and initial policy work | Historical source | [Windows deployment and GPO](../docs/pages/windows-policy-deployment.html) |
| IV.03 | GPO and directory refinements | Historical source | [Windows deployment and GPO](../docs/pages/windows-policy-deployment.html) |
| IV.04 | AD deployment continuation | Historical source | [Active Directory and PKI](../docs/pages/windows-ad-pki.html) |
| IV.05 | AD deployment continuation and device issues | Historical source | [Windows deployment and GPO](../docs/pages/windows-policy-deployment.html) |
| IV.06 | Extended AD deployment / diagnostic sequence | Historical source | [Active Directory and PKI](../docs/pages/windows-ad-pki.html) |
| IV.07 | Extended AD/PKI engineering | Historical source | [Active Directory and PKI](../docs/pages/windows-ad-pki.html) |
| IV.08 | Additional platform integration notes | Historical source | [Monitoring and backups](../docs/pages/windows-monitoring-backup.html) |
| IV.09 | CA certificate revocation list publication | Observed CRL checks | [Active Directory and PKI](../docs/pages/windows-ad-pki.html) |
| IV.10 | LDAPS and VLAN/EAP-TLS interoperability | Observed selected checks | [LDAPS failover test](../docs/pages/notes.html#identity) |
| IV.11 | FreeRADIUS handling of two CA/CRL chains | Observed checks | [Two CA chains and CRL fix](../docs/pages/windows-ad-pki.html#two-ca-crls) |
| IV.12 | Wired 802.1X / AD / FreeRADIUS integration | Observed selected clients | [Active Directory and PKI](../docs/pages/windows-ad-pki.html) |
| IV.13 | Android SCEP and EAP-TLS provisioning automation | Observed enrollment | [Linux and Android enrollment](../docs/pages/linux-mobile-identity.html) |
| IV.14 | Android BYOD work-profile EAP-TLS lifecycle | Observed multiple devices | [Linux and Android enrollment](../docs/pages/linux-mobile-identity.html) |
| IV.15 | Kubuntu AD/EAP-TLS and certificate renewal | Observed selected services | [Linux and Android enrollment](../docs/pages/linux-mobile-identity.html) |
| IV.16 | Kubuntu VPN/login/display-manager integration | Observed selected operations | [Linux and Android enrollment](../docs/pages/linux-mobile-identity.html) |
| IV.17 | Windows 11 GPO and domain client integration | Observed selected clients | [Windows deployment and GPO](../docs/pages/windows-policy-deployment.html) |
| IV.18 | Older AD EAP-TLS workstation migration | Historical plus tests | [Windows deployment and GPO](../docs/pages/windows-policy-deployment.html) |
| IV.19 | Windows 11 WireGuard automatic off-site connectivity | Observed selected use | [Windows WireGuard automation](../docs/pages/windows-policy-deployment.html#windows-wireguard) |
| IV.20 | PowerShell remoting over WinRM and Kerberos | Observed selected source/target combinations | [WinRM and Kerberos remoting](../docs/pages/windows-policy-deployment.html#winrm-remoting) |
| IV.21 | PowerShell 7/Sysinternals/RSAT/WAC/Sysmon rollout | Observed documented client set | [Windows deployment and GPO](../docs/pages/windows-policy-deployment.html) |
| IV.22 | RustDesk OSS deployment by GPO/MSI | Observed existing and new-install paths | [Windows deployment and GPO](../docs/pages/windows-policy-deployment.html) |
| IV.23 | Windows Exporter, Prometheus, Grafana AD/PKI dashboard | Observed scraper and collector checks | [Monitoring and backups](../docs/pages/windows-monitoring-backup.html) |

### About the older notes

- The document's canonical chapters and the latest dated updates take precedence over older appendices when status conflicts.
- A historical *plan* may become a verified result later; it must not be presented as both concurrently.
- Two working directory controllers do not imply high availability of the enterprise CA, NDES or storage.
- A completed backup task does not prove full restoration from the backup.
- Certificate enrollment, revocation, authorization and client Wi-Fi access are related but distinct verification domains.
- AD GPO and remote admin operations are represented by their mechanism and verified outcome, not by private account or host identifiers.

---
