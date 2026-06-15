# AI-Powered Alcohol Label Verification App

## Overview

This project is a prototype alcohol label verification tool designed for compliance reviewers. The app extracts text from uploaded alcohol label artwork using OCR, then compares that text against expected application fields.

The goal is not to replace human compliance judgment. Instead, the tool helps reviewers quickly identify likely matches, mismatches, and items that need closer review.

## Features

- Upload one or more label images
- Extract label text using OCR
- Compare brand name against application data
- Compare class/type designation
- Verify alcohol content using ABV and proof detection
- Verify net contents
- Check for the required government warning statement
- Display field-by-field PASS, REVIEW, or FAIL results
- Support batch uploads
- Export results as a CSV report

## Stakeholder Needs Addressed

The prototype was designed around the discovery notes from compliance and IT stakeholders.

Sarah Chen emphasized that many reviews involve routine data matching. This app automates common matching tasks.

Sarah also stated that results need to be fast and easy to understand. The interface uses a simple upload form and clear result statuses.

Dave Morrison noted that label review requires judgment. The app uses PASS, REVIEW, and FAIL instead of automatic approval or rejection.

Jenny Park noted that warning statement wording and capitalization are important. The prototype checks for required wording and the all-caps GOVERNMENT WARNING introduction.

Marcus Williams noted that this should be a standalone proof of concept without direct COLA integration. This prototype runs independently.

## How It Works

1. The reviewer uploads one or more label images.
2. The reviewer enters the expected application values.
3. EasyOCR extracts text from the image.
4. The app runs rule-based and fuzzy-matching checks.
5. Results are displayed in a table.
6. Batch results can be downloaded as a CSV report.

## Tech Stack

- Python
- Streamlit
- EasyOCR
- RapidFuzz
- Pandas
- Pillow
- Pytest

## Setup Instructions

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd alcohol-label-verifier
