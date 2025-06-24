# 😈 Evil Advice API

A simple, sarcastic, and slightly malicious advice-giving API built with **FastAPI** and **MongoDB**.

Host your own or contribute evil wisdom to the world.

---

## 🧠 What It Does

This API lets you:

- Fetch a random evil advice 😈
- Submit new advice 📝
- Filter advice by category 📚
- Get all advice in the database 🗃️
- List all unique categories 🔍

---

## 🚀 Live Demo

> 🔗 [https://evil-advice-as-a-service.onrender.com/docs](https://evil-advice-as-a-service.onrender.com/docs)

Interactive Swagger documentation powered by FastAPI.

## 📚 API Routes
All responses are in JSON.
| Method   | Endpoint              | Description                                                | Params                                                  |
| -------- | --------------------- | ---------------------------------------------------------- | ------------------------------------------------------- |
| **GET**  | `/evil-advice`        | Returns a random piece of evil advice from all categories. | None                                                    |
| **GET**  | `/evil-advice/random` | Returns a random advice, optionally filtered by category.  | `category` (query param, optional)                      |
| **GET**  | `/evil-advices`       | Returns all advice, optionally filtered by category.       | `category` (query param, optional)                      |
| **GET**  | `/categories`         | Returns a list of all unique advice categories.            | None                                                    |
| **POST** | `/evil-advice`        | Submit a new evil advice entry.                            | JSON Body: `{ "category": "string", "text": "string" }` |


---
## Get Random Advice
```bash
GET /evil-advice
```
## Get All Advice in "tech" Category
```bash
GET /evil-advices?category=tech
```
## Add New Advice
```bash
POST /evil-advice
Content-Type: application/json

{
  "category": "social",
  "text": "Post your ex’s phone number for fun."
}

```
## 🔧 Tech Stack

- **Python 3.12+**
- **FastAPI**
- **MongoDB**
- **Uvicorn**
- **Docker** (optional)
- **Render** (for deployment)
- **dotenv** for environment variables

---

## 📦 Installation

```bash
git clone https://github.com/your-username/evil-advice-api.git
cd evil-advice-api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
