# CyphornIPS Official Rules & Intelligence Repository

This repository provides the official detection rule sets and File Intelligence datasets for **CyphornIPS**.

---

## Repository Layout

```
cyphorn-rules/
├── README.md
└── channels/
    ├── stable/
    │   ├── manifest.json              # Canonical update manifest for stable channel
    │   ├── rules.rules                # Production detection rules dataset
    │   └── file-intelligence.json     # Threat intelligence & malicious hash dataset
    └── beta/                          # (Optional) Pre-release candidate channel
```

---

## Channels & Endpoints

### 1. Stable Channel (`channels/stable`)
- **Manifest URL:**
  `https://raw.githubusercontent.com/<OWNER>/cyphorn-rules/main/channels/stable/manifest.json`
- **Detection Rules Artifact:**
  `https://raw.githubusercontent.com/<OWNER>/cyphorn-rules/main/channels/stable/rules.rules`
- **File Intelligence Artifact:**
  `https://raw.githubusercontent.com/<OWNER>/cyphorn-rules/main/channels/stable/file-intelligence.json`

---

## Updating CyphornIPS

To check for and install updates from this repository:

```bash
# Check update availability
cyphornctl update check

# Update and hot-reload detection rules
cyphornctl update rules

# Update and hot-reload File Intelligence
cyphornctl update intelligence

# Update and atomically hot-reload both components
cyphornctl update all
```

---

## Integrity & Verification

All artifacts distributed via this repository must have their SHA256 checksums recorded in `manifest.json`. The CyphornIPS engine validates these checksums and parses candidate files in a temporary sandbox before applying any updates.
