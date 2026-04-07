import json

from llm_client import llm_call


def build_research_prompt(document_text: str):
    system_prompt = """
You are an expert research document explainer.

Analyze the document as a research report, analytical report, or research-style article.

Return ONLY valid JSON.
Do not use markdown.
Do not include any text outside JSON.

Use exactly this schema:
{
  "title": "string",
  "document_type": "research report",
  "main_topic": "string",
  "research_goal": "string",
  "summary": "string",
  "key_findings": ["string", "string", "string"],
  "limitations": ["string", "string"],
  "simplified_explanation": "string",
  "suggested_questions": ["string", "string", "string"]
}

Rules:
- title: infer the document title if possible; if unclear, provide a short descriptive title
- document_type: always use "research report"
- main_topic: short phrase describing the main subject
- research_goal: one sentence explaining the purpose of the document
- summary: concise but informative paragraph
- key_findings: 3 to 7 short findings or conclusions
- limitations: 0 to 5 short limitations, weaknesses, or data issues explicitly stated or strongly supported by the document; if none are clear, return []
- simplified_explanation: explain the document in plain language
- suggested_questions: 3 useful follow-up questions a reader might ask
- return only valid JSON
""".strip()

    user_prompt = f"""
Analyze the following research document and return the JSON.

DOCUMENT:
{document_text}
""".strip()

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def clean_llm_json_response(raw_text: str) -> str:
    """
    Clean raw LLM output before JSON parsing.
    """
    cleaned = raw_text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    return cleaned


def summarize_document_to_json(document_mode: str, document_text: str) -> dict:
    """
    Summarize a document into structured JSON depending on document_mode.
    """
    if document_mode == "research":
        messages = build_research_prompt(document_text)
        max_new_tokens = 1600
    else:
        raise ValueError(f"Unsupported document type: {document_mode}")

    raw_response = llm_call(
        messages,
        max_new_tokens=max_new_tokens
    )

    cleaned = clean_llm_json_response(raw_response)

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        print("⚠️ JSON parsing failed. Raw response:\n")
        print(raw_response)
        raise

    return parsed


def print_summary(result: dict):
    """
    Pretty-print research summary result.
    """
    print("📘 Title:", result.get("title"))
    print("📄 Document type:", result.get("document_type"))
    print("🏷 Main topic:", result.get("main_topic"))

    print("\n🎯 Research goal:\n")
    print(result.get("research_goal"))

    print("\n🧾 Summary:\n")
    print(result.get("summary"))

    print("\n🔍 Key findings:")
    findings = result.get("key_findings", [])
    if findings:
        for item in findings:
            print("-", item)
    else:
        print("- None found")

    print("\n⚠️ Limitations:")
    limitations = result.get("limitations", [])
    if limitations:
        for item in limitations:
            print("-", item)
    else:
        print("- None identified")

    print("\n🧠 Simplified explanation:\n")
    print(result.get("simplified_explanation"))

    print("\n❓ Suggested questions:")
    questions = result.get("suggested_questions", [])
    if questions:
        for item in questions:
            print("-", item)
    else:
        print("- None")