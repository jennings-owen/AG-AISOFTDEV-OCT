# Ascend Onboarding Platform API

Welcome to the Ascend Onboarding Platform API, the backend service powering a revolutionary new hire experience. This project aims to transform a typically fragmented process into a structured, engaging, and efficient journey.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-green)](https://fastapi.tiangolo.com/)

---

## Overview

The Ascend Onboarding Platform is designed to solve the common challenges of new hire onboarding. New employees often face an overwhelming amount of information, while HR and managers lack centralized tools to track progress and provide support.

This API provides the core infrastructure to:
-   **For New Hires (`Eager Contributors`):** Create personalized learning paths and provide a central hub for resources.
-   **For HR Specialists (`Onboarding Orchestrators`):** Streamline administrative tasks and monitor the progress of all new hires from a single dashboard.
-   **For Managers (`Team Integrators`):** Easily assign mentors, track skill development, and accelerate a new member's integration into the team.

This repository contains the foundational User Management service, built with FastAPI and SQLAlchemy, which serves as the backbone for the entire platform.

## Features

This API provides the core functionality for managing users within the Ascend platform.

-   **Comprehensive User Model:** The database schema includes detailed user attributes such as role, department, manager, mentor, start date, and experience level.
-   **CRUD Operations for Users:** Full Create, Read, Update, and Delete functionality for all user profiles.
-   **Role-Based User Types:** Differentiates between user types (`new_hire`, `manager`, `hr_specialist`, `employee`) to enable tailored experiences.
-   **Relational Mapping:** Establishes clear relationships between users, including manager-to-direct-report and mentor-to-mentee pairings.
-   **Scalable Architecture:** Built on FastAPI for high performance and automatic interactive API documentation.
-   **SQLite Database:** Uses a simple, file-based SQLite database for easy setup and local development.

## API Endpoints

All endpoints are available under the base URL: `http://127.0.0.1:8000`

### Users

#### 1. Create a New User

Creates a new user in the system. The email address must be unique.

-   **Method:** `POST`
-   **Path:** `/users/`
-   **Request Body:** A JSON object matching the `UserCreate` schema.

**Example `curl` Request:**