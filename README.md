# Multi-Source Candidate Data Transformer


A configurable data transformation pipeline that ingests candidate information from multiple structured and unstructured sources, normalizes and merges conflicting data into a single canonical profile, tracks provenance and confidence, and supports runtime-configurable output schemas.

---

# Features

- Parse candidate data from multiple sources
  - Recruiter CSV
  - ATS JSON
  - Resume PDF

- Merge duplicate candidate profiles

- Normalize candidate information
  - Phone numbers (E.164)
  - Canonical skill names

- Track provenance for every extracted field

- Assign confidence scores to merged data

- Runtime configurable output schema
  - Field selection
  - Field renaming
  - Array projection
  - Missing value handling

- Output validation

- Unit tests

---

# Architecture

```

                 +---------------------+
                 | Recruiter CSV       |
                 +----------+----------+
                            |
                            |
                 +----------v----------+
                 |     CSV Parser      |
                 +---------------------+

                 +---------------------+
                 | ATS JSON            |
                 +----------+----------+
                            |
                            |
                 +----------v----------+
                 |     ATS Parser      |
                 +---------------------+

                 +---------------------+
                 | Resume PDF          |
                 +----------+----------+
                            |
                            |
                 +----------v----------+
                 |   Resume Parser     |
                 +---------------------+

                            |
                            |
                +-----------v-----------+
                | Canonical Candidate   |
                |      Data Model       |
                +-----------+-----------+
                            |
                            |
                +-----------v-----------+
                |    Merge Engine       |
                +-----------+-----------+
                            |
                            |
                +-----------v-----------+
                | Projection Engine     |
                +-----------+-----------+
                            |
                            |
                +-----------v-----------+
                | Output Validator      |
                +-----------+-----------+
                            |
                            |
                    Final JSON Output

```

---

# Canonical Candidate Schema

```json
{
  "candidate_id": "...",
  "full_name": "...",
  "emails": [],
  "phones": [],
  "location": {},
  "headline": "...",
  "skills": [],
  "experience": [],
  "education": [],
  "provenance": [],
  "overall_confidence": 0.95
}
```

---

# Project Structure

```
candidate-transformer/

│

├── config/
│   ├── default.json
│   └── custom.json
│
├── input/
│   ├── recruiter.csv
│   ├── ats.json
│   └── resume.pdf
│
├── output/
│   └── output.json
│
├── src/
│   ├── merger/
│   ├── models/
│   ├── normalizers/
│   ├── parsers/
│   ├── projection/
│   └── validation/
│
├── tests/
│   ├── test_merge.py
│   ├── test_projection.py
│   └── test_validator.py
│
├── requirements.txt
│
└── main.py
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/shravyaalake/Multi-Source-Candidate-Data-Transformer.git

cd candidate-transformer
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

## Default Output Schema

```bash
python main.py \
--csv input/recruiter.csv \
--ats input/ats.json \
--resume input/resume.pdf \
--config config/default.json
```

---

## Custom Output Schema

```bash
python main.py \
--csv input/recruiter.csv \
--ats input/ats.json \
--resume input/resume.pdf \
--config config/custom.json
```

---

# Runtime Configuration

The projection layer supports runtime configuration without code changes.

Example:

```json
{
  "fields": [
    {
      "path": "candidate_name",
      "from": "full_name"
    },
    {
      "path": "primary_email",
      "from": "emails[0]"
    },
    {
      "path": "skills",
      "from": "skills[].name"
    }
  ],
  "include_confidence": false,
  "include_provenance": false,
  "on_missing": "omit"
}
```

---

# Merge Strategy

Candidate profiles from multiple sources are merged into a canonical profile using deterministic rules.

Priority:

1. Recruiter CSV
2. ATS JSON
3. Resume PDF

Conflict resolution:

- Prefer more complete names
- Remove duplicate emails
- Normalize phone numbers
- Remove duplicate experiences
- Remove duplicate skills
- Preserve provenance
- Keep highest confidence score

---

# Provenance Tracking

Every extracted field records:

- Source
- Extraction Method

Example

```json
{
    "field":"emails",
    "source":"Resume PDF",
    "method":"Regex + Section Parsing"
}
```

---

# Confidence Policy

| Source | Confidence |
|---------|-----------|
| Recruiter CSV | 0.95 |
| ATS JSON | 0.90 |
| Resume PDF | 0.80 |

The merged profile keeps the highest confidence for trusted values.

---

# Validation

The output validator verifies

- Required fields
- Expected types
- Missing value handling
- Runtime configuration

---

# Testing

Run all tests

```bash
python -m pytest
```

Expected

```
=====================
3 passed
=====================
```

---

# Sample Output

## Default Output

```json
{
    "full_name":"Shravya Alake",
    "emails":[
        "shravya.alake1@gmail.com"
    ],
    "phones":[
        "+919876543210"
    ]
}
```

---

## Custom Output

```json
{
    "candidate_name":"Shravya Alake",
    "primary_email":"shravya.alake1@gmail.com",
    "skills":[
        "Python",
        "Docker",
        "React"
    ]
}
```

---

# Assumptions

- Candidate uniqueness is determined using merged profile logic.
- Resume parsing uses deterministic regex and section parsing.
- Phone numbers are normalized to E.164.
- Unknown values are never fabricated.
- Missing values are handled according to runtime configuration.

---

# Future Improvements

- LinkedIn API integration
- GitHub API integration
- OCR for scanned resumes
- Machine Learning based entity extraction
- Fuzzy candidate matching
- Confidence learning model
- Batch processing support
- Docker deployment

---

# Tech Stack

- Python
- Pandas
- Pydantic
- pdfplumber
- phonenumbers
- pytest

---

# Test Results

```
==================================
3 tests passed
==================================
```
---
