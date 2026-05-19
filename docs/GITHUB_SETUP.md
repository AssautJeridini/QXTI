# GitHub Setup Guide

## Purpose

This document is a short checklist for turning the local scaffold into a clean GitHub repository.

## Recommended Steps

1. Initialize Git if needed:

   ```bash
   git init -b main
   ```

2. Review the generated repository files:

   - `README.md`
   - `LICENSE`
   - `CONTRIBUTING.md`
   - `CODE_OF_CONDUCT.md`
   - `.github/ISSUE_TEMPLATE/`
   - `.github/pull_request_template.md`

3. Add the project files:

   ```bash
   git add .
   ```

4. Create the initial commit:

   ```bash
   git commit -m "Initial QXTI scaffold"
   ```

5. Create an empty GitHub repository and connect it:

   ```bash
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

## Before Publishing

- Confirm the chosen license matches how you want others to use the code.
- Replace placeholders if you want a different author name or contact details.
- Add at least one working example before sharing the repository broadly.
- Add tests as soon as the first executable module lands.
