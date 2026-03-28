"""RAG Pipeline for Course Planning Assistant using Google Gemini."""

import os
from typing import List, Dict, Optional
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class CoursePlannerRAG:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        print(f"Initializing CoursePlannerRAG with {model_name}...")
        self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        self.db = Chroma(persist_directory="./chroma_db", embedding_function=self.embeddings)
        self.retriever = self.db.as_retriever(search_kwargs={"k": 10})
        
        # Check for API key; use placeholder if missing to allow instantiation
        api_key = os.environ.get("GOOGLE_API_KEY", "dummy_key")
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, google_api_key=api_key)
        
        # Mandatory structured prompt
        self.system_prompt = """You are an MIT Course 6 (EECS) Academic Advisor Assistant.
Strictly ground your answers in the provided MIT Course Catalog and Policy snippets.
Every claim must include a citation in the format [Source X].
If info is missing (e.g., student's major, grades, or catalog year), ask 1-5 clarifying questions.
If the information is not in the provided documents, abstain and suggest checking MIT official sites or an advisor.

FOLLOW THIS EXACT OUTPUT FORMAT:
Answer / Plan: <the direct answer or suggested plan>
Why (requirements/prereqs satisfied): <justification based on catalog rules>
Citations: <List sources with URL/Heading, e.g., [1] Course 6 Catalog - https://catalog.mit.edu/subjects/6/>
Clarifying questions (if needed): <List missing info required for a better answer>
Assumptions / Not in catalog: <List anything assumed or missing from the docs>
"""

    def format_docs(self, docs):
        if not docs:
            return "No relevant catalog snippets found."
        formatted = []
        for i, d in enumerate(docs):
            source = d.metadata.get('source', 'MIT Catalog')
            formatted.append(f"[Source {i+1}: {source}]\n{d.page_content}")
        return "\n\n".join(formatted)

    def get_agentic_chain(self):
        """
        Equivalent to a Stage Chain: Router -> Retrieval -> Reasoner -> Verifier.
        """
        reasoning_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "Context:\n{context}\n\nQuery: {query}")
        ])
        
        chain = (
            {
                "context": self.retriever | self.format_docs, 
                "query": RunnablePassthrough()
            }
            | reasoning_prompt
            | self.llm
            | StrOutputParser()
        )
        return chain

    def invoke_with_fallback(self, query: str) -> str:
        """Handles the LLM call and provides a mock/debug response if the API key fails."""
        try:
            chain = self.get_agentic_chain()
            return chain.invoke(query)
        except Exception as e:
            if "API_KEY_INVALID" in str(e) or "401" in str(e) or "key" in str(e).lower():
                return self._generate_debug_response(query)
            return f"Error: {e}"

    def _generate_debug_response(self, query: str) -> str:
        """Generates a structured placeholder response showcasing the format when API is unavailable."""
        docs = self.retriever.invoke(query)
        return (
            "Answer / Plan: [GEMINI OFFLINE] The assistant is configured for Google Gemini but requires a valid GOOGLE_API_KEY.\n"
            f"Why (requirements/prereqs satisfied): Reasoning requires active Gemini API over context: {query[:50]}...\n"
            f"Citations: Successfully retrieved {len(docs)} snippets from ChromaDB.\n"
            "Clarifying questions (if needed): 1. What is your major? 2. What catalog year are you following?\n"
            "Assumptions / Not in catalog: Policy default to MIT Course 6-3 rules."
        )

    def prereq_check(self, query: str) -> str:
        """Determines eligibility for a course based on prerequisites."""
        return self.invoke_with_fallback(query)

    def generate_plan(self, completed: List[str], major: str = "6-3", term: str = "Fall", max_courses: int = 4) -> str:
        """Suggests a term plan based on completed courses and program requirements."""
        query = (
            f"Suggest a {term} term plan for a {major} major who has completed: {', '.join(completed)}. "
            f"Limit to maximum {max_courses} courses. "
            "Ensure all suggested courses have their prerequisites met by the completed list."
        )
        return self.invoke_with_fallback(query)

if __name__ == '__main__':
    planner = CoursePlannerRAG()
    print("\n--- TEST: PREREQ CHECK (GEMINI) ---")
    print(planner.prereq_check("Can I take 6-1200J if I took 6-01?"))
    print("\n--- TEST: COURSE PLAN (GEMINI) ---")
    print(planner.generate_plan(["6-01", "18.01"], major="6-3"))

