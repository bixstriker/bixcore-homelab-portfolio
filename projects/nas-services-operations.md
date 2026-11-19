# NAS Services and Docker Networking

The NAS does more than store files. It runs some of the services my network depends on, so a missing IPv6 address or a wrong container route can cause problems well beyond the NAS itself.

## What runs there

The NAS hosts Docker-based infrastructure such as AdGuard, a reverse proxy, the UniFi controller, remote-support services, password management, PXE/ISO boot support and monitoring. I also run other applications on it, but this project is about their network connections and how they come back after maintenance.

## A closer look at the running containers

On 12 November I audited all **36 Docker entries**, including stopped ones, rather than just the containers visible in the live resource snapshot. I checked their images, published ports, Docker networks, mounts and restart policies without collecting secret values. That inventory helps me spot service dependencies, but it is not itself a tested restore procedure.

I also set up TACACS-NG-UI for switch administration. The backend connects to AD over LDAPS, while a separate UI and PostgreSQL container support management. I kept the FastAPI service at one Uvicorn worker; in a short measurement the three running components used about 122 MiB altogether. The NAS had used swap, but the brief system sample did not show heavy active paging. I wouldn't use that snapshot alone to justify a hardware change.

[The TACACS+ deployment and failover tests →](../docs/pages/tacacs-switch-aaa.html)

## Two networking problems I had to fix

**Missing IPv6 ULA.** Clients were relying on a stable internal IPv6 address for DNS, but that address could disappear after interface changes. My original hook was not reliable enough. I replaced it with an idempotent recovery script, a systemd oneshot service and a timer, then checked the address after the relevant events.

**Docker routing.** A reverse-proxy container attached to multiple networks could end up with an unsuitable default route or IPv6 address. I corrected the network and gateway preferences in the Compose configuration so that recreating the container wouldn't put the old problem back.

## Updates without losing the infrastructure

When updating the NAS operating system and Docker, I need more than a list of container names. I keep copies of Compose definitions, environment files, volumes, network settings, restart policies and supporting scripts. DNS is brought back early, followed by the reverse proxy and dependent services.

I tested this maintenance sequence during a real upgrade. It helped me spot service-order dependencies that are easy to miss if everything is simply set to restart automatically.

## A watchdog that fired during an update

After a NAS operating-system update on 17 November, I checked that its stable IPv6 DNS address returned, the important Docker services still had the right routes, and the published certificate revocation list matched across the CA, NAS and FreeRADIUS. This was a useful post-update consistency check, not a new revoked-client login test.

My Plex watchdog also got a real test. After three failed reachability checks it restarted OpenVPN. Plex became reachable later, but Docker was still starting after planned maintenance, so I cannot credit the VPN restart with the recovery. The script followed its rules at the wrong time. I'll pause it for future planned updates and enable it again after checking the services.

## Plex playback and VPN monitoring aren't the same thing

After measuring faster remote Plex streaming through Vodafone, I left normal playback on WAN. Windscribe still publishes a separate endpoint for the NAS watchdog, which checks the externally forwarded port. **It is a port-reachability test, not an HTTP health check of Plex.**

I kept the existing Windscribe and HomeWG recovery arrangement instead of trying to use the Plex watchdog to prove application or VPN failover behavior.

## Certificates and DNS service updates

I updated AdGuard Home to its 1.0.0 beta 2 image after keeping a rollback copy and checking that DNS, conditional Active Directory lookups, HTTPS, DNS-over-HTTPS and DNS-over-TLS still worked. A listening DoQ port is not the same as a completed QUIC test, so I have not claimed that.

I also renewed the certificates used by the NAS web interface, AdGuard Home and Home Assistant, checking the served TLS chain and hostname. Certificate issuance on OPNsense is automatic, but deploying the renewed files to those services is still a manual step.

## What I want to check next

The services have been brought back after maintenance, but I still want to restore selected applications from independent backups rather than only verify that their containers start. I also want to keep testing the NAS's IPv6 recovery after network changes and verify an independent restore of the TACACS+ database and configuration. I checked a consistent backup before the PostgreSQL 18.7 update, but haven't tested a restore.

[The disappearing IPv6 address →](../docs/pages/notes.html#nas-ula)   [The Docker gateway issue →](../docs/pages/notes.html#docker-route)

---
