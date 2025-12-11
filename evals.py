import os
import sys
from pathlib import Path

from openai import OpenAI
import google.generativeai as genai
from utils.config import google_api
from litellm import acompletion

from ragas import Dataset, experiment
from ragas.llms import llm_factory
from ragas.metrics import DiscreteMetric

from litellm import acompletion

# Add the current directory to the path so we can import rag module when run as a script
sys.path.insert(0, str(Path(__file__).parent))
from rag import default_rag_client

genai.configure(api_key=google_api)
client = genai.GenerativeModel("gemini-2.0-flash")
rag_client = default_rag_client(llm_client=client, logdir="evals/logs")

async def gemini_chat(messages):
    """LiteLLM wrapper for ragas"""
    response = await acompletion(
        model="gemini/gemini-1.5-flash",
        messages=messages,
        temperature=0
    )
    return {"role": "assistant", "content": response.choices[0].message.content}

# Ragas-compatible LLM object
class LiteLLMForRagas:
    async def achat(self, messages, **kwargs):
        return await gemini_chat(messages)

llm = LiteLLMForRagas()

def load_dataset():
    dataset = Dataset(
        name="test_dataset",
        backend="local/csv",
        root_dir="evals",
    )

    data_samples = [
        {
            "question": "What is ragas 0.3",
            "grading_notes": "- experimentation as the central pillar - provides abstraction for datasets, experiments and metrics - supports evals for RAG, LLM workflows and Agents",
        },
        {
            "question": "how are experiment results stored in ragas 0.3?",
            "grading_notes": "- configured using different backends like local, gdrive, etc - stored under experiments/ folder in the backend storage",
        },
        {
            "question": "What metrics are supported in ragas 0.3?",
            "grading_notes": "- provides abstraction for discrete, numerical and ranking metrics",
        },
    ]

    for sample in data_samples:
        row = {"question": sample["question"], "grading_notes": sample["grading_notes"]}
        dataset.append(row)

    # make sure to save it
    dataset.save()
    return dataset


my_metric = DiscreteMetric(
    name="correctness",
    prompt="Check if the response contains points mentioned from the grading notes and return 'pass' or 'fail'.\nResponse: {response} Grading Notes: {grading_notes}",
    allowed_values=["pass", "fail"],
)


@experiment()
async def run_experiment(row):
    response = rag_client.query(row["question"])
    score = my_metric.score(
        llm=llm,
        response=response.get("answer", " "),
        grading_notes=row["grading_notes"],
    )

    experiment_view = {
        **row,
        "response": response.get("answer", ""),
        "score": score.value,
        "log_file": response.get("logs", " "),
    }
    return experiment_view


async def main():
    dataset = load_dataset()
    print("dataset loaded successfully", dataset)
    experiment_results = await run_experiment.arun(dataset)
    print("Experiment completed successfully!")
    print("Experiment results:", experiment_results)

    # Save experiment results to CSV
    experiment_results.save()
    csv_path = Path(".") / "experiments" / f"{experiment_results.name}.csv"
    print(f"\nExperiment results saved to: {csv_path.resolve()}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
