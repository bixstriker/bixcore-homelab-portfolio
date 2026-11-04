# How EAP-TLS works in BiXCore

```mermaid
flowchart LR
    Device[Wired or Wi-Fi client] -->|EAP-TLS| Access[Switch or access point]
    Access -->|RADIUS / EAP| AAA[FreeRADIUS on OPNsense]
    AAA -->|Certificate chain and revocation| CA[Trusted CA and CRL material]
    AAA -->|LDAPS authorization| DC1[Primary directory controller]
    AAA -.->|Tested fallback| DC2[Second directory controller]
    AAA -->|Access decision| Access
```

The client authenticates with a certificate; FreeRADIUS also applies access policy. The directory fallback was tested separately from issuing CA and SCEP availability.
