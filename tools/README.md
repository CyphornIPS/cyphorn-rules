# CyphornIPS File Intelligence Generator 🛡️

`generate_intel.py` is a lightweight utility for creating and maintaining **CyphornIPS File Intelligence datasets** from local files.

The tool calculates multiple cryptographic hashes, detects the file MIME type, adds optional tags, and generates records compatible with the CyphornIPS File Intelligence schema.

---

## ✨ Features

For every file, the generator calculates:

* 🔐 MD5
* 🔐 SHA-1
* 🔐 SHA-256
* 🔐 SHA3-384
* 📄 File name
* 📦 File size
* 🧩 MIME type
* 🏷️ Custom tags

The generated record can then be used by the CyphornIPS File Intelligence engine for **exact cryptographic hash matching**.

---

## 🎯 Why use this tool?

CyphornIPS does not require File Intelligence to come from a single centralized provider.

Users can create their own datasets from files they are authorized to analyze.

This allows CyphornIPS to support:

* 👤 Personal File Intelligence databases
* 🏢 Private organizational databases
* 🔬 Security research datasets
* 🧪 Security-lab datasets
* 👥 Community-maintained datasets
* 🛡️ Internal security datasets
* ✅ CyphornIPS test datasets

The generator operates on **local files supplied by the user**.

It does not automatically download threat intelligence from external providers.

---
# 🚀 Installation

## 🐧 Linux

### Option 1 — Download directly

Download `generate_intel.py` directly from the CyphornIPS repository:

[Download generate_intel.py](https://github.com/CyphornIPS/cyphorn-rules/blob/main/tools/generate_intel.py)

Or download the raw Python file from:

[Raw generate_intel.py](https://raw.githubusercontent.com/CyphornIPS/cyphorn-rules/main/tools/generate_intel.py)

## Using `curl`:

```bash
curl -L \
  https://raw.githubusercontent.com/CyphornIPS/cyphorn-rules/main/tools/generate_intel.py \
  -o generate_intel.py
```

## Or using `wget`:

```bash
wget \
  https://raw.githubusercontent.com/CyphornIPS/cyphorn-rules/main/tools/generate_intel.py \
  -O generate_intel.py
```

---

## Make the script executable:

```bash
chmod +x generate_intel.py
```
---

## Run it:

```bash
./generate_intel.py /path/to/file
```

## Or run it directly with Python:

```bash
python3 generate_intel.py /path/to/file
```

---


## 🪟 Windows

Download:

[generate_intel.py](https://github.com/CyphornIPS/cyphorn-rules/blob/main/tools/generate_intel.py)

Or download the raw file:

[Raw generate_intel.py](https://raw.githubusercontent.com/CyphornIPS/cyphorn-rules/main/tools/generate_intel.py)

Save the file, for example, as:

```text
C:\CyphornIPS\generate_intel.py
```

Open PowerShell:

```powershell
cd C:\CyphornIPS
```

Run:

```powershell
python .\generate_intel.py "C:\Samples\sample.exe"
```

If your Windows installation uses the Python launcher:

```powershell
py .\generate_intel.py "C:\Samples\sample.exe"
```

No additional Python packages are required.



---


# 🔐 Hash Calculation

The generator calculates four cryptographic hashes:

```text
MD5
SHA-1
SHA-256
SHA3-384
```

Example:

```text
SHA256:
470c8513480684ce00c3c1063c853623e149b43680d69951e3df70f7ccdc7cde

SHA3-384:
31f0842ecd3ddb93e383364031374318eb19270c70da7ad5da5db8264cbe51a3b074289a8b99ae2eeb5893464dd304da

SHA1:
96bd45b314fdd29541f388f6072fe5bfaa2a7151

MD5:
b107273dd70de96ed25a2ce6af47a142
```

Files are processed in **1 MiB chunks**, so the complete file does not need to be loaded into memory.

This allows the utility to process large files more efficiently.

---

# 🏷️ Adding Tags

Tags can be added using `--tag`.

Example:

```bash
./generate_intel.py sample.exe \
    --tag MALWARE \
    --tag TROJAN \
    --tag INTERNAL
```

Multiple `--tag` arguments are supported.

The resulting record contains:

```json
"tags": [
  "MALWARE",
  "TROJAN",
  "INTERNAL"
]
```

---

# 📁 Creating a File Intelligence Dataset

The generator can be executed multiple times.

For example:

```bash
./generate_intel.py sample-001.exe \
    --tag INTERNAL \
    --tag TEST-001
```

Then:

```bash
./generate_intel.py sample-002.exe \
    --tag INTERNAL \
    --tag TEST-002
```

Then:

```bash
./generate_intel.py sample-003.bin \
    --tag INTERNAL \
    --tag TEST-003
```

All records are added to the same:

```text
output/file-intelligence.json
```

The dataset follows the CyphornIPS schema:

```json
{
  "schema_version": 1,
  "generated_at": "...",
  "source": "...",
  "records": [
    {
      "sha256_hash": "...",
      "sha3_384_hash": "...",
      "sha1_hash": "...",
      "md5_hash": "...",
      "file_name": "...",
      "file_type_mime": "...",
      "tags": []
    }
  ]
}
```

---

# 🛑 Duplicate Protection

The generator uses **SHA-256** to detect duplicate files.

If the same file is processed again, the existing record will not be duplicated.

For example:

```text
sample.exe
     ↓
SHA-256
     ↓
Already exists
     ↓
No duplicate record
```

Changing the filename does not bypass this protection because the file contents and therefore the SHA-256 remain the same.

---

# 👤 Personal File Intelligence Database

A user can create a private File Intelligence database for personal security research or analysis.

Example:

```bash
./generate_intel.py suspicious-001.exe \
    --tag INTERNAL \
    --tag ANALYSIS
```

Then:

```bash
./generate_intel.py suspicious-002.exe \
    --tag INTERNAL \
    --tag ANALYSIS
```

The resulting database can be loaded locally by CyphornIPS.

```text
📄 Local files
      ↓
🔐 Hash calculation
      ↓
🗄️ Personal File Intelligence
      ↓
🛡️ CyphornIPS
      ↓
🔎 Exact Hash Matching
```

---

# 🏢 Organizational File Intelligence Database

Organizations can create private datasets for their own environments.

Examples include:

* Internal malware-analysis samples
* Known malicious files
* Known unwanted software
* Security research samples
* Incident-response artifacts
* Organization-specific indicators

Example:

```bash
./generate_intel.py internal-sample.exe \
    --tag COMPANY \
    --tag MALWARE \
    --tag INCIDENT-RESPONSE
```

The resulting dataset can remain private and be distributed only inside the organization.

---

# 👥 Community File Intelligence

The same generator can be used to create a community-maintained File Intelligence dataset.

A security community can:

```text
🔬 Analyze authorized samples
          ↓
🔐 Calculate hashes
          ↓
📝 Add metadata and tags
          ↓
🗄️ Build dataset
          ↓
🌍 Publish dataset
          ↓
🛡️ CyphornIPS users
```

Community datasets should clearly document:

* 👤 Dataset owner
* 🎯 Dataset purpose
* 📚 Data sources
* 🔬 Collection methodology
* 📜 License
* 🔄 Update frequency
* 🏷️ Dataset version
* 📧 Contact information
* 📤 Distribution policy

Only data that the publisher is authorized to redistribute should be included in a public dataset.

---

# ⚠️ External Threat Intelligence

`generate_intel.py` does **not** automatically import data from:

* MalwareBazaar
* VirusTotal
* abuse.ch
* Other external intelligence providers

The tool only processes files supplied locally.

If a user creates a dataset using information obtained from an external provider, the user is responsible for complying with that provider's applicable terms, licenses, and redistribution requirements.

CyphornIPS does not grant permission to redistribute third-party data.

---

# 🧪 CyphornIPS Test Dataset

CyphornIPS also provides test files for validating File Intelligence functionality.

Example:

```bash
./generate_intel.py cyphorn-test-001.txt \
    --tag CYPHORN-TEST \
    --tag FILE-INTELLIGENCE \
    --tag TEST-001
```

Additional test files can be added to the same dataset.

These datasets are useful for:

* ✅ Exact-hash matching tests
* 🔄 Regression testing
* 🧪 Engine validation
* 🚀 CI/CD testing
* 🔎 Hash calculation validation
* 🚨 Alert generation testing
* 📦 File Intelligence update testing
* 🔥 Hot-reload testing

---

# 🔎 How CyphornIPS Uses the Dataset

CyphornIPS calculates the cryptographic hash of an inspected file and compares it against the loaded File Intelligence dataset.

The basic workflow is:

```text
📄 File
   ↓
🔐 Calculate hash
   ↓
🗄️ File Intelligence database
   ↓
⚡ Exact hash lookup
   ↓
┌─────────────────┐
│                 │
│    MATCH        │──────→ 🚨 File Intelligence Alert
│                 │
└─────────────────┘

        OR

┌─────────────────┐
│                 │
│   NO MATCH      │──────→ Continue inspection
│                 │
└─────────────────┘
```

A hash match means that the calculated cryptographic hash exists in the loaded dataset.

The meaning of the match depends on the dataset metadata and its publisher.

---

# 📤 Custom Output Location

The default output is:

```text
output/file-intelligence.json
```

A different location can be specified using `--output`:

```bash
./generate_intel.py sample.exe \
    --tag INTERNAL \
    --output /path/to/my-file-intelligence.json
```

Windows example:

```powershell
python .\generate_intel.py "C:\Samples\sample.exe" `
    --tag INTERNAL `
    --output "C:\CyphornIPS\file-intelligence.json"
```

---

# 🧰 Command Reference

Basic:

```bash
./generate_intel.py FILE
```

With tags:

```bash
./generate_intel.py FILE \
    --tag TAG1 \
    --tag TAG2
```

Custom output:

```bash
./generate_intel.py FILE \
    --output OUTPUT.json
```

Combined:

```bash
./generate_intel.py suspicious.exe \
    --tag MALWARE \
    --tag INTERNAL \
    --tag INCIDENT-RESPONSE \
    --output output/file-intelligence.json
```

---

# 🛡️ Security and Legal Responsibility

The generator only calculates hashes and creates metadata records.

It does **not** determine whether a file is malicious.

A hash match means that the file's cryptographic hash exists in the loaded dataset.

Users are responsible for ensuring that they have the appropriate rights to:

* Analyze files
* Store files
* Generate datasets
* Publish datasets
* Redistribute datasets

When creating community datasets, publishers should verify the licensing and redistribution rights of all included data.

---

# 🌐 Building an Open File Intelligence Ecosystem

CyphornIPS is designed so that File Intelligence can be decentralized.

Instead of depending on a single intelligence provider, different users and communities can create datasets for different purposes:

```text
                    🛡️ CyphornIPS
                           │
                 File Intelligence
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
       ▼                   ▼                   ▼
   👤 Personal          🏢 Private          👥 Community
    Dataset              Dataset              Dataset
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                           ▼
                  file-intelligence.json
                           │
                           ▼
                  🔎 Exact Hash Engine
```

This architecture allows the CyphornIPS engine to remain independent from any single external intelligence provider.

The engine consumes a standardized dataset format, while the source and ownership of the intelligence remain separate from the detection engine.

