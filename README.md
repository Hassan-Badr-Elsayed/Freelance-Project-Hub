# Freelance Management System

A comprehensive offline system for managing a freelance marketplace written in Python. It fully applies Object-Oriented Programming (OOP) principles, advanced data validation, and state persistence using JSON files.

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Roles & Dashboards](#roles--dashboards)
4. [Architecture & Design Principles](#architecture--design-principles)
5. [Requirements](#requirements)
6. [How to Run](#how-to-run)
7. [Project Structure](#project-structure)

---

## Overview

The system manages relationships between Clients, Freelancers, and Admins. It allows Clients to create projects, set budgets and deadlines, and assign freelancers to tasks. Freelancers can track their assigned work, update project statuses, and generate invoices. Admins have complete system oversight, with the ability to generate financial reports and track active or overdue projects.

---

## Key Features

- User Management:
  - Multi-role account creation (Client / Freelancer / Admin).
  - Auto-generated formatted IDs for each user (e.g., U0001, U0002).

- Advanced Data Validation:
  - Phone number validation matching Egyptian mobile prefixes (010, 011, 012, 015).
  - Password strength verification (minimum 8 characters, containing uppercase, lowercase, numbers, and no spaces).
  - Regex format verification for emails and deadlines (DD-MM-YYYY).

- Automated Data Persistence (JSON):
  - Automatic saving and loading of users, projects, and invoices into `data.json`.
  - Object relation restoration upon application restart.

- Invoicing & Commission System:
  - Automatic platform commission calculation at a fixed 10% rate using Closures and Higher-Order Functions.
  - Export detailed invoice receipts as plain text files (.txt).

- Financial & Project Reports:
  - Total net earnings calculation from paid invoices using `reduce`.
  - Filtering overdue and active projects using `filter` and date comparisons via the `datetime` module.

---

## Roles & Dashboards

### 1. Client

- Create new projects with defined deadlines and allowable budgets (1000, 2500, 5000, 10000, 20000).
- Assign open projects to freelancers using Freelancer ID.
- Track project progress and current statuses.
- Manage and pay invoices (marked as Paid).
- Cancel owned projects.

### 2. Freelancer

- View assigned tasks and projects.
- Update project status (open, in progress, closed, cancelled).
- Update deadlines when necessary.
- Generate project invoices.

### 3. Admin

- Platform-wide monitoring of all projects and invoices.
- Generate comprehensive financial and progress reports.
- Delete projects with confirmation prompts.

---

## Architecture & Design Principles

The project was built adhering to clean code practices and the following core programming principles:

1. Inheritance & Polymorphism:
   - Base class `User` extended by `Client`, `Freelancer`, and `Admin`, implementing `display_profile()`.
2. Custom Exception Handling:
   - Custom `ValidationError` and `InvalidInvoiceAmount` classes for precise input error management.
3. Functional Concepts & Closures:
   - `create_commission_rule` closure keeping track of total commissions using `nonlocal`.
   - Usage of `filter`, `reduce`, and `lambda` functions for data processing.
4. Encapsulation:
   - Setters/Getters enforcing validation rules on status, budget, and deadline attributes before assignment.

---

## Requirements

- Runtime: Python 3.8 or higher.
- External Dependencies: None. Built entirely using standard Python modules:
  - `re` (Regular expressions)
  - `json` (Data serialization)
  - `datetime` (Date handling)
  - `functools` (Functional tools like `reduce`)

---

## How to Run

1. Clone or download the project and ensure `main.py` is in the working directory.

2. Run the application via Terminal or Command Prompt:
   ```bash
   python main.py
   ```
