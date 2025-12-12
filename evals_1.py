import asyncio
import time
import re
from ollama import AsyncClient
from rag import ExampleRAG, SimpleKeywordRetriever, DOCUMENTS
import pandas as pd
from datetime import datetime
from pathlib import Path

async def main():
    llm_client = AsyncClient()
    retriever = SimpleKeywordRetriever()
    rag_client = ExampleRAG(llm_client=llm_client, retriever=retriever, logdir="logs")
    rag_client.add_documents(DOCUMENTS)

    def extract_first_number(text: str) -> float:
        """Extract first numeric value from text, return 0.0 if none found"""
        match = re.search(r"\d*\.?\d+", text)
        if match:
            return float(match.group(0))
        return 0.0

    async def score_relevance(query: str, answer: str) -> (float, float):
        prompt = f"""
You are an evaluator. Score 0-1.
Question: {query}
Answer: {answer}
Return only a number between 0 and 1.
"""
        start = time.time()
        response = await llm_client.chat(model="gemma2:2b", messages=[{"role": "user", "content": prompt}])
        latency = time.time() - start
        score = extract_first_number(response['message']['content'])
        return score, latency

    async def score_completeness(query: str, answer: str) -> (float, float):
        prompt = f"""
You are an evaluator. Score 0-1.
Question: {query}
Answer: {answer}

Does the answer fully cover all parts of the question?
Return only a number between 0 and 1.
"""
        start = time.time()
        response = await llm_client.chat(model="gemma2:2b", messages=[{"role": "user", "content": prompt}])
        latency = time.time() - start
        score = extract_first_number(response['message']['content'])
        return score, latency

    async def score_factual_accuracy(answer: str) -> (float, float):
        prompt = f"""
You are an evaluator. Score 0-1.
Answer: {answer}

Is this answer factually correct? Penalize hallucinations.
Return only a number between 0 and 1.
"""
        start = time.time()
        response = await llm_client.chat(model="gemma2:2b", messages=[{"role": "user", "content": prompt}])
        latency = time.time() - start
        score = extract_first_number(response['message']['content'])
        return score, latency

    async def evaluate_rag(queries):
        results = []
        for q in queries:
            print(f"\nEvaluating query: {q}")
            start_time = time.time()
            r = await rag_client.query(q, top_k=3) 
            total_latency = time.time() - start_time

            answer = r["answer"]

            relevance, rel_latency = await score_relevance(q, answer)
            completeness, comp_latency = await score_completeness(q, answer)
            factuality, fact_latency = await score_factual_accuracy(answer)

            results.append({
                "query": q,
                "answer": answer,
                "relevance": relevance,
                "completeness": completeness,
                "factual_accuracy": factuality,
                "rag_latency_sec": total_latency,
                "evaluation_latency_sec": rel_latency + comp_latency + fact_latency,
                "total_latency_sec": total_latency + rel_latency + comp_latency + fact_latency
            })

        return results

    # Example queries
    queries = [
        "What is Ragas?",
        "Explain the types of ragas and their purposes.",
        "How are ragas performed and used in classical music?"
    ]

    eval_results = await evaluate_rag(queries)
    df = pd.DataFrame(eval_results)
    return df

if __name__ == "__main__":
    results_df = asyncio.run(main())
    
    date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_name = "rag_eval_report"+ date_time + ".csv"
    base_dir = Path("evals") / "experiments"
    full_path = base_dir / csv_name
    full_path.parent.mkdir(parents=True, exist_ok=True)

    results_df.to_csv(full_path, index=False)

