# LLM_evaluation: Evaluation Pipeline for RAG

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/nilesh666/LLM_evaluation?style=social)](https://github.com/nilesh666/LLM_evaluation/stargazers)

## 🎯 Overview

This repository provides a **robust, production-ready pipeline** designed for the comprehensive evaluation of Large Language Model (LLM) responses. It is built to seamlessly integrate into development workflows, offering objective and quantifiable metrics to measure the performance, consistency, and quality of various LLMs, especially within a Retrieval-Augmented Generation (RAG) framework.

## ✨ Key Features

* **Production Pipeline:** Structured for reliability and repeatability, suitable for CI/CD integration.
* **LLM Response Evaluation:** Contains scripts (`evals_1.py`, `evals/`) for various evaluation methodologies (e.g., faithfulness, correctness, coherence, fluency).
* **RAG Integration:** Dedicated modules (`rag.py`) for evaluating LLM performance when grounded in external knowledge sources.
* **Ollama Support:** Includes a batch file (`run_ollama.bat`) for easy local deployment and testing of open-source models using Ollama.
* **Modern Python Tooling:** Uses `pyproject.toml` and `uv.lock` for efficient dependency management and virtual environments.
* **Logging:** Centralized logging (`logs/`) for tracking evaluation results, model inputs, and outputs.

## 🛠️ Prerequisites

To run this project, you need:

* **Python:** Version 3.11 or newer (as indicated by `.python-version`).
* **Ollama (Optional):** Required if you intend to run local models using the provided `run_ollama.bat` script.

## 🚀 Installation

Follow these steps to set up your environment:

### 1. Clone the Repository

```bash
git clone [https://github.com/nilesh666/LLM_evaluation.git](https://github.com/nilesh666/LLM_evaluation.git)
cd LLM_evaluation
```
## 2. Set up the Environment

This project uses **uv** for ultra-fast dependency management (recommended) but can also use **pip**.

### Using uv (Recommended)

```bash
# Install uv if you don't have it
pip install uv

# Create and activate the virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies from uv.lock
uv sync
```

### Using pip
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt # Assuming a requirements.txt is generated from pyproject.toml/uv.lock
```

## 3. Ollama Configuration

I have used Ollama for inference. 
Model - gemma2:2b (Download and test first) 

Just open the run_ollama.bat file to serve the model.

# 💻 Usage
### 1. Running Local Models with Ollama

If you wish to test models locally, use the provided script to start the Ollama service:

Start the Ollama server and pull necessary models
./run_ollama.bat 

### 2. Evaluating a Simple LLM Response

The evals_1.py script serves as the main entry point for running a specific set of evaluations.

### 3. Evaluating RAG Performance

The rag.py module handles the RAG pipeline, which typically involves querying a document store, retrieving context, generating a response, and evaluating the result.

### 4. To run
```bash
uv run python evals_1.py
```

### 📂 Project Structure
```bash
LLM_evaluation/
├── evals/                    # Evaluation metrics and logic (e.g., FaithfulnessEvaluator)
├── logs/                     # Directory for all evaluation run logs
├── utils/                    # Common utility functions (e.g., API wrappers, data loading)
├── .gitignore                # Files/folders to ignore
├── .python-version           # Specifies the required Python version (e.g., 3.11)
├── __init__.py               # Makes the directory a Python package
├── evals_1.py                # Main script for running a single evaluation benchmark
├── pyproject.toml            # Project configuration and dependencies (Poetry/Hatch/PDM)
├── rag.py                    # Script to run the Retrieval-Augmented Generation pipeline
├── run_ollama.bat            # Windows batch script to start Ollama service/pull models
├── test.py                   # Unit tests for core functions and evaluation metrics
├── uv.lock                   # Lock file for exact dependency versions (used by uv)
└── README.md
```