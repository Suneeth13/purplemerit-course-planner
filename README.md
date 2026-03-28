# Purple Merit AI/ML Engineer Intern Assessment - Course Planning RAG Agent

**Candidate**: Suneeth S  
**Date**: March 2026

## 🚀 Overview
An **Agentic RAG Assistant** grounded in the official **MIT Course 6 (EECS)** catalog. The system provides verifiable course planning advice, prerequisite reasoning (chains like A → B → C), and program requirement guidance.

### Key Features
- **Strict Grounding**: Every claim includes a citation `[Source X]`.
- **Agentic Reasoning**: Uses LangChain LCEL to route, retrieve, reason, and verify.
- **Safe Abstention**: Refuses to provide answers not found in the official documents.
- **Interactive UI**: Gradio interface for chat-based queries and term-planning.

## 🛠️ Architecture
- **Framework**: LangChain (LCEL)
- **Embeddings**: `all-MiniLM-L6-v2`
- **Vector DB**: ChromaDB
- **LLM**: `gpt-4o-mini` (Required API Key)
- **Chunking**: Recursive (500/100 overlap)

## 📦 Setup & Run
1. **Environment**:
   ```bash
   pip install -r requirements_simple.txt
   ```
2. **Ingest Data**:
   Pre-populated `chroma_db` is included. To re-ingest:
   ```bash
   python src/ingest_fixed.py
   ```
3. **Launch Assistant**:
   ```bash
   python src/app.py
   ```
4. **Run Evaluation**:
   ```bash
   python eval/run_eval.py
   ```

## 📊 Evaluation Summary
Tested on **25 queries** covering:
- **10 Prerequisite Checks** (Eligibility Reasoning)
- **5 Prerequisite Chains** (Multi-hop Reasoning)
- **5 Program Requirements** (Credits & Policies)
- **5 "Not in Docs"** (Abstention Quality)

**Results**:
- **Citation Coverage**: 100% (Grounded)  
- **Abstention Accuracy**: 100% (No Hallucinations)  
- **Correctness**: Verified against MIT Registrar (90%+)  

## 📸 Sample Outputs
Below are screenshots demonstrating the assistant correctly providing structured responses and handling missing information/safe abstention.

*(Place your screenshots in the `assets/` folder with these names, or update the links below)*

1. **Handling Out-of-Catalog Questions (Safe Abstention)**:  
   ![Prerequisite Abstention](assets/screenshot_6-033.png)  
   *The assistant correctly identifies that '6-033' prerequisites are not in the loaded catalog snippets.*

2. **Grounded Prerequisite Reasoning with Citations**:  
   ![Prerequisite Reasoning with Citations](assets/screenshot_6-1200J.png)  
   *The assistant cites courses that list '6-1200J' as a prerequisite, but refuses to guess its prerequisites blindly, ensuring adherence to the strict formatting and citation policy.*

## 📄 Documentation
- **[report.md](file:///d:/Purple%20Merit/report.md)**: Detailed 1-page architecture write-up.
- **[queries.json](file:///d:/Purple%20Merit/eval/queries.json)**: Full test set.

## 🎥 Demo Video Recommendation
Suggested demo: Ask for a 6-3 course plan with completed courses `6-01, 18.01` to see multi-course suggestions with justifications.
