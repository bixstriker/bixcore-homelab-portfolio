# BiX Barox Config Tool — simplified architecture

```mermaid
flowchart LR
  Config[Exported switch config] --> Parser[Config parser]
  Parser --> Manual[Goal 1: manual CLI recovery guide]
  Parser --> Analyze[Goal 2: network settings analysis]
  Catalog[Live-help / firmware CLI evidence] --> Manual
  Manual -.-> Serial[Goal 3: serial preflight only]
  Analyze -.-> Future[Goal 4: proposed remediation]
```

**As of 4 November 2026:** Goal 1 and Goal 2 are implemented; the selected Goal 3 hardware probes and preflight exist, but the automated executor does not. Goal 4 is an unimplemented concept. The source repository is private and is not linked here because it contains device-specific research material.
