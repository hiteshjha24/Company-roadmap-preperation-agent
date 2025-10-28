# 🤖 AI Interview Roadmap Generator Agent

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green)](https://www.langchain.com/)
[![Gemini API](https://img.shields.io/badge/Gemini-API-orange)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

> ⚙️ **Project Type:** GENAI Task - Research Agent  
> 🧠 **Purpose:** Generate a *targeted interview preparation roadmap* using AI, tailored to the company and role.

---

## 🧩 Overview

This project leverages **Gemini API** and **LangChain** to convert a **Job Description (JD)** into a clear, structured **interview roadmap**.  
It fuses *company-specific data* with *public knowledge* to produce **JSON-based output** ready for integration or further processing.

---

## 🚨 Problem Statement

Preparing for a tech interview = 😵‍💫 chaos.  
Candidates struggle with:
- Extracting the right keywords from JDs manually.  
- Researching each company’s unique interview process.  
- Combining that info into a structured study plan.  

💡 **This AI Agent automates all of it** — from parsing the JD to researching interview rounds, difficulty, and generating a ready-to-use roadmap.

---

## 🧠 Tech Stack

| Component | Description |
|------------|-------------|
| **Language** | Python 🐍 |
| **LLM** | Gemini API (`gemini-2.5-flash-preview-09-2025`) |
| **Framework** | LangChain Expression Language (LCEL) |
| **Structured Output** | Pydantic (JSON Schema Validation) |
| **Env Management** | python-dotenv |

---

## 🏗️ Architecture & Flow

### 1️⃣ Input
The agent requires three inputs:
- `Company Name`
- `Job Role`
- `Job Description (JD)` text

---

### 2️⃣ Job Description Parsing
Performs in-depth analysis to extract and map required skills:

- **Skill Extraction:** Detects key skills like `Python`, `Microservices`, `Data Structures`.
- **Keyword Mapping:** Converts skills into broader domains (e.g., *REST APIs → Backend Development*).

---

### 3️⃣ Company & Difficulty Analysis
Uses **Google Search Tool** to find:
[{Company} {Role} interview process and difficulty]

From there, it infers:
- Interview round types (e.g., Coding, System Design, Behavioral)
- Estimated difficulty level (`Easy`, `Medium`, `Hard`)

---

### 4️⃣ Roadmap Synthesis
The agent merges internal and external findings to produce a **structured JSON** that includes:

| Field | Description |
|-------|--------------|
| `rounds` | Derived from JD & Google Search |
| `topics` | Categorized skills per round |
| `difficulty` | Based on company and role complexity |
| `recommended_order` | Logical learning path |

---

## ⚙️ How to Run

### **Setup**
```bash
# Clone the repository
git clone <your-repo-url>
cd AI-Interview-Roadmap-Agent

# Install dependencies
pip install langchain-google-genai pydantic python-dotenv

Run the Agent
python roadmap_agent.py

🧾 Example Outputs
<details> <summary>🧠 Google Example Output</summary>

{
    "company": "Google",
    "role": "Software Development Engineer (SDE) - L3",
    "rounds": [
        {
            "type": "Technical Coding",
            "topics": ["Data Structures and Algorithms", "Greedy Algorithms", "Dynamic Programming", "Graphs"]
        },
        {
            "type": "System Design",
            "topics": ["Distributed Systems", "Scaling", "Microservices Architecture", "Load Balancing"]
        },
        {
            "type": "Behavioral",
            "topics": ["Googliness & Leadership", "Communication", "Conflict Resolution"]
        }
    ],
    "difficulty": "Hard",
    "recommended_order": [
        "Data Structures and Algorithms",
        "System Design Fundamentals",
        "Python/Go Language Syntax",
        "Behavioral Interview Preparation"
    ]
}
</details>