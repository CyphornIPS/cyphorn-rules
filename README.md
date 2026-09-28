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
  `https://raw.githubusercontent.com/CyphornIPS/cyphorn-rules/main/channels/stable/manifest.json`
- **Detection Rules Artifact:**
  `https://raw.githubusercontent.com/CyphornIPS/cyphorn-rules/main/channels/stable/rules.rules`
- **File Intelligence Artifact:**
  `https://raw.githubusercontent.com/CyphornIPS/cyphorn-rules/main/channels/stable/file-intelligence.json`

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

## Current stable channel

| | version | contents |
|---|---|---|
| `rules.rules` | `2026.09.28.1` | 11,965 detection rules |
| `file-intelligence.json` | `2026.09.28.1` | 1,271 file hashes |

Published 2026-09-28. `cyphornctl status` prints what *your* appliance has loaded,
which is the only count that matters to you.

---

## Integrity & Verification

All artifacts distributed via this repository must have their SHA256 checksums recorded in `manifest.json`.

`manifest.json` is signed with Ed25519 and the signature is published beside it
as `manifest.json.sig`. The signature covers the file's **bytes**, so
reformatting or re-indenting the manifest invalidates it and every appliance
will refuse the update. Build the channel with `scripts/publish-rule-channel.sh`
rather than editing the manifest by hand, and commit the artifacts and the
manifest together: a manifest that becomes visible before the files it names
points at hashes that do not match yet. The CyphornIPS engine validates these checksums and parses candidate files in a temporary sandbox before applying any updates.
