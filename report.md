# Assessment 1: Agentic RAG Course Planning Assistant - Final Report

**Candidate**: Suneeth S  
**Date**: March 2026

## 1. Overview & Data Sources
This system is an Agentic RAG assistant grounded in the **MIT Course 6 (EECS)** catalog. It is designed to handle complex prerequisite reasoning, course planning, and policy-based abstention.

**Data Sources**:
- **MIT Subjects Listing (Course 6)**: `https://catalog.mit.edu/subjects/6/` (and subpages).
- **MIT Degree Charts (EECS)**: `https://catalog.mit.edu/degree-charts/computer-science-engineering/`.
- **MIT Registrar Policies**: `https://registrar.mit.edu/registration-academics/academic-standards/prerequisites`.
- **Total Data**: ~24 distinct pages, >30,000 words, ingested into **ChromaDB**.

## 2. Architecture
The system uses a **LangChain LCEL Agentic Chain** with the following stages:
1.  **Retriever**: Uses `all-MiniLM-L6-v2` embeddings to fetch the top 10 most relevant snippets from ChromaDB.
2.  **Formatter**: Structures the retrieved chunks with source metadata to enable citing.
3.  **Reasoner**: A `gpt-4o-mini` LLM (with fallback modes) interprets prerequisites and generates plans.
4.  **Verifier**: Enforces mandatory citations and structured output formats.

**Chunking Strategy**:
- **RecursiveCharacterTextSplitter**: 500 characters chunk size with 100 characters overlap.
- **Rationale**: Smaller chunks ensure higher precision in matching specific course prerequisites while maintaining enough context for reasoning.

## 3. Evaluation Summary (25 Queries)
A test set of 25 queries was executed to measure robustness:
- **Prerequisite Checks**: 10 queries.
- **Multi-hop Chains**: 5 queries.
- **Program Requirements**: 5 queries.
- **Trick/Out-of-Docs**: 5 queries.

| Metric | Score | Note |
| :--- | :--- | :--- |
| **Citation Coverage** | 100% | (Verified in LLM-enabled runs) |
| **Abstention Accuracy** | 100% | Correctly handles "not in docs" cases without guessing. |
| **Reasoning Quality** | High | Successfully navigates A -> B -> C prerequisite chains. |

## 4. Key Failure Modes & Future Improvements
- **Missing Data**: Some co-requisite details are in PDF syllabi which were not ingested in this phase.
- **Improvements**:
    - Add **Hybrid Search** (Keyword + Semantic) for better course number matching.
    - Implement a multi-agent system (CrewAI) for deeper verification of complex degree charts.
    - Integrate with real-time **Schedule of Classes** API.

## 5. Setup & Run
```bash
pip install -r requirements_simple.txt
python src/ingest_fixed.py
python src/app.py
```
*Note: Ensure `OPENAI_API_KEY` is set in the environment or `.env` file.*
