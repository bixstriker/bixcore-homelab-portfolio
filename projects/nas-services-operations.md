# NAS Services and Docker Networking

The NAS does more than store files. It runs some of the services my network depends on, so a missing IPv6 address or a wrong container route can cause problems well beyond the NAS itself.

## What runs there

The NAS hosts Docker-based infrastructure such as AdGuard, a reverse proxy, the UniFi controller, remote-support services, password management, PXE/ISO boot support and monitoring. I also run other applications on it, but this project is about their network connections and how they come back after maintenance.

## Two networking problems I had to fix

**Missing IPv6 ULA.** Clients were relying on a stable internal IPv6 address for DNS, but that address could disappear after interface changes. My original hook was not reliable enough. I replaced it with an idempotent recovery script, a systemd oneshot service and a timer, then checked the address after the relevant events.

**Docker routing.** A reverse-proxy container attached to multiple networks could end up with an unsuitable default route or IPv6 address. I corrected the network and gateway preferences in the Compose configuration so that recreating the container wouldn't put the old problem back.

## Updates without losing the infrastructure

When updating the NAS operating system and Docker, I need more than a list of container names. I keep copies of Compose definitions, environment files, volumes, network settings, restart policies and supporting scripts. DNS is brought back early, followed by the reverse proxy and dependent services.

I tested this maintenance sequence during a real upgrade. It helped me spot service-order dependencies that are easy to miss if everything is simply set to restart automatically.

## What I want to check next

The services have been brought back after maintenance, but I still want to restore selected applications from independent backups rather than only verify that their containers start. I also want to keep testing the NAS's IPv6 recovery after network changes.

[The disappearing IPv6 address →](../docs/pages/notes.html#nas-ula)   [The Docker gateway issue →](../docs/pages/notes.html#docker-route)

---
