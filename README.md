# 📦 ShelfSense

### Modern, Containerized Retail POS & Intelligent Inventory Architecture

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.63-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

---

## 📌 Overview

**ShelfSense** is an express Point of Sale (POS) and inventory control system designed for high-velocity counter operations in retail and grocery stores (*karyana* stores). 

It replaces slow, manual bookkeeping and bloated commercial software with an ultra-responsive billing terminal backed by an asynchronous FastAPI engine, running entirely inside isolated Docker containers.

---

## ⚡ Test & Access Endpoints

Once your containers or local servers are running, access the interfaces here:

| Interface | URL | Purpose |
| :--- | :--- | :--- |
| **Cashier Terminal (POS)** | [http://localhost:8501](http://localhost:8501) | Main billing counter, quick-add catalog, receipt generation, and live metrics |
| **Interactive API Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger UI to test backend endpoints, validation schemas, and database calls |
| **ReDoc Specifications** | [http://localhost:8000/redoc](http://localhost:8000/redoc) | Alternative clean API documentation and data models |

---

## 🎯 Features

* **Instant Counter Billing:** Point-and-click item drawer with automatic calculations and real-time stock deduction on checkout.
* **Live Revenue Tracking:** Daily gross sales totals, receipt counts, and average bill value with historical date-range filters.
* **Automated Stock Alerts:** Low-stock badges, out-of-stock locks, and an instant restock slider interface.
* **Persistent SQLite Storage:** Uses Docker host volume mounts (`./store.db:/app/store.db`) so transaction records survive updates and restarts.
* **Zero Dependency Setup:** Pre-configured Docker Compose environment—no Python installation or environment wrestling required on target machines.

---

## 🛠️ Architecture

* **Frontend:** Streamlit running reactive counter interfaces on port `8501`.
* **Backend:** FastAPI running asynchronous REST endpoints via Uvicorn on port `8000`.
* **Database:** Embedded SQLite (`store.db`) with host volume persistence.
* **Orchestration:** Multi-container Docker bridge network managing service discovery and restart policies.

---

## 🚀 Quick Launch (Docker)

```bash
# Clone and enter
git clone [https://github.com/SaranshMinocha/ShelfSense.git](https://github.com/SaranshMinocha/ShelfSense.git)
cd ShelfSense

# Build and run
docker compose up --build -d

# Stop anytime
docker compose down