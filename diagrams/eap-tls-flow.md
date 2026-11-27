# How EAP-TLS works in BiXCore

```mermaid
flowchart LR
    Device[Wired or Wi-Fi client] -->|EAP-TLS| Access[Switch or access point]
    Access -->|RadSec / TLS 1.3 mTLS| Proxy[RadSecProxy on OPNsense]
    Proxy -->|Local RADIUS / EAP| AAA[FreeRADIUS on OPNsense]
    AAA -->|Certificate chain and revocation| CA[Trusted CA and CRL material]
    AAA -->|LDAPS authorization| DC1[Primary directory controller]
    AAA -.->|Tested fallback| DC2[Second directory controller]
    AAA -->|Access decision| Proxy
    Proxy -->|RadSec response| Access
```

The client authenticates with an EAP-TLS certificate; FreeRADIUS also applies access policy. For the two UniFi APs and the tested Omada switch, the separate RadSec transport authenticates the network device and proxy with their own certificates. This diagram shows that tested path, not every RADIUS client. The directory fallback was tested separately from issuing CA and SCEP availability.
