# TACACS+ for Switch Administration

I wanted to use my Active Directory accounts to manage switches without giving every user the same level of access. I already had RADIUS for network clients, but administrative login to a switch is a different job. I set up a TACACS+ service on my NAS and tested it with two different switch vendors.

## How I put it together

I run **tac_plus-ng** in a Docker-based TACACS-NG-UI stack. Its interface is separate from the TACACS+ daemon, and directory lookups use LDAPS with certificate validation against my internal CA. Both domain controllers are configured as directory endpoints. The web interface is reached through my existing reverse proxy; I don't expose the database as a separate service.

I gave the switches a simple authorization rule: my designated administrator has configuration access, while other authenticated directory users get restricted access. Omada and Barox use different privilege models, so I checked what their interfaces actually allowed instead of assuming that the same numeric privilege level meant the same thing on both.

Authentication and restricted roles worked on both switches. TACACS+ authentication, authorization and accounting are configured where supported; I have not audited every possible CLI command or accounting record.

## The failure test was more revealing

I deliberately stopped the TACACS+ daemon and tried the emergency local account on each switch.

- **Barox:** local administrator login worked while TACACS+ was unavailable. After restoring the service, domain authentication worked again.
- **Omada:** local web login worked when I explicitly selected local authentication. With the configured TACACS+-then-local method and an unreachable TACACS+ server, the same local account was rejected. I also saw a similar SSH symptom.
- **Packet capture:** the Omada switch sent repeated TCP connection attempts to the TACACS+ endpoint without a reply. I repeated the unavailability test with a targeted network drop rather than relying on a single service restart.

This demonstrates a reproducible fallback problem **in my tested configuration**. It does not establish where the switch firmware fails internally. I reported the evidence to TP-Link support on 12 November 2026 and have not treated the issue as resolved.

## Operating it and what remains open

The TACACS+ backend, web frontend and PostgreSQL run as separate containers. I reduced the FastAPI process to a single Uvicorn worker and checked the resource usage; the stack was roughly **122 MiB** in one snapshot. That is not a benchmark or a claim about peak load.

This adds another dependency to switch administration, so I want an independently tested restore procedure for the service and its database. Until the Omada fallback behavior is understood, I keep recovery access planning separate from the convenient domain-login path.

[Switching and enterprise Wi-Fi](../docs/pages/switching-wireless.html) · [NAS and Docker operations](../docs/pages/nas-services-operations.html) · [Fallback investigation](../docs/pages/notes.html#tacacs-fallback)
