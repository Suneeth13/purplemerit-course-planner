import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from rag import CoursePlannerRAG

def run_evaluation():
    eval_file = Path(__file__).parent / "queries.json"
    results_file = Path(__file__).parent / "results.json"
    
    with open(eval_file, "r") as f:
        queries = json.load(f)
        
    planner = CoursePlannerRAG()
    results = []
    
    citation_count: int = 0
    abstention_correct: int = 0
    total_abstention_queries: int = 0
    
    print(f"Starting evaluation on {len(queries)} queries...")
    
    for i, item in enumerate(queries):
        query = item["query"]
        category = item["category"]
        
        print(f"[{i+1}/{len(queries)}] Running {category}...")
        
        response = planner.prereq_check(query)
        
        # Calculate metrics
        has_citation = "[Source" in response or "[1]" in response
        if has_citation:
            citation_count += 1
            
        is_abstention_query = category == "Not in Docs / Trick"
        if is_abstention_query:
            total_abstention_queries += 1
            # Check if response correctly identifies missing info
            if "don’t have that information" in response.lower() or "not in catalog" in response.lower() or "[OFFLINE MODE]" in response:
                abstention_correct += 1
        
        results.append({
            "query": query,
            "category": category,
            "response": response,
            "has_citation": has_citation
        })
        
    # Summarize
    summary = {
        "total_queries": len(queries),
        "citation_coverage_rate": f"{(citation_count / len(queries)) * 100:.2f}%",
        "abstention_accuracy": f"{(abstention_correct / total_abstention_queries) * 100:.2f}%" if total_abstention_queries > 0 else "N/A",
        "results": results
    }
    
    with open(results_file, "w") as f:
        json.dump(summary, f, indent=2)
        
    print("\n--- Evaluation Summary ---")
    print(f"Total Queries: {summary['total_queries']}")
    print(f"Citation Coverage: {summary['citation_coverage_rate']}")
    print(f"Abstention Accuracy: {summary['abstention_accuracy']}")
    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    run_evaluation()
