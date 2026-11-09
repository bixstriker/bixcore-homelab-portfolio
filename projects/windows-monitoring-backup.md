# Monitoring and Backing Up Windows Server

Once Active Directory and the certificate services were running, I wanted to see problems before they turned into login or network-access failures. I also wanted a recovery plan that went beyond having a second domain controller.

## Monitoring the services

I installed Windows Exporter with collectors for system performance, Active Directory, DNS, certificate services, IIS and scheduled tasks. Prometheus collects those metrics, and I built a Grafana dashboard around the areas I need to check most often.

That gives me a view of server load, directory services, certificate publication and whether the scheduled jobs are running. I use Sysmon separately for Windows event investigations; I have not tried to turn this setup into a full SIEM.

## System State backups

I configured and checked scheduled System State backups for the domain controllers, using NAS storage as part of the backup arrangement. The recovery notes also cover DNS, certificates, access permissions and the services that need to come back in a sensible order.

The second domain controller helps when a directory service is unavailable. It does not replace a backup of the CA database or guarantee that a server's storage can be recovered after a disk failure.

## A failed System State job and the follow-up

On 1 November one controller's weekly backup failed after a Realtek NIC reset. The SMB connection dropped during the write. The logs were consistent with a real failed job, not just a bad monitoring panel.

I updated the network drivers on both controllers. The next weekly System State jobs on 8 November were reported successful. I haven't independently inspected those latest backup catalogs or restored a controller from them, and the absence of one repeated NIC failure doesn't prove the driver was the only cause.

The backup rotation also needs a safer success check: simply keeping the most recent dated directories could retain a partial backup.

[The failure and follow-up →](../docs/pages/notes.html#dc-backup-nic)

## What I still want to test

The latest scheduled jobs were reported successful, but I haven't rebuilt either controller and the CA from a complete verified backup set. That is the exercise I want to finish before treating the recovery plan as tested end to end.

[Directory and certificate services →](../docs/pages/windows-ad-pki.html)   [Recovery work on the roadmap →](../docs/pages/roadmap.html)

---
