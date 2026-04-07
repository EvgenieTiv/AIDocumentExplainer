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
  "methodology": "string",
  "key_findings": ["string", "string", "string"],
  "limitations": ["string", "string"],
  "practical_implications": ["string", "string"],
  "simplified_explanation": "string",
  "suggested_questions": ["string", "string", "string"],
  "confidence": "high | medium | low"
}

Rules:
- title: infer the document title if possible; if unclear, provide a short descriptive title
- document_type: always use "research report"
- main_topic: short phrase describing the main subject
- research_goal: one sentence explaining the purpose of the document
- summary: concise but informative paragraph
- methodology: briefly describe the method, dataset, experiment, or analysis used; if not clearly stated, return "Not clearly stated"
- key_findings: 3 to 7 short findings or conclusions
- limitations: 0 to 5 short limitations or data issues explicitly stated or strongly supported; if none are clear, return []
- practical_implications: 0 to 5 short points describing why the results matter in practice; if unclear, return []
- simplified_explanation: explain the document in plain language
- suggested_questions: 3 useful follow-up questions a reader might ask
- confidence:
  - "high" if the document structure, goal, and findings are clear
  - "medium" if some parts are unclear or inferred
  - "low" if the document is incomplete, noisy, or hard to interpret
- do not invent facts that are not supported by the document
- if something is unclear, prefer "Not clearly stated" or [] instead of guessing
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


def build_news_prompt(document_text: str):
    system_prompt = """
You are an expert news document explainer.

Analyze the document strictly as a news article or journalistic report.

Return ONLY valid JSON.
Do not use markdown.
Do not include any text outside JSON.

Use exactly this schema:
{
  "title": "string",
  "document_type": "news article",
  "main_event": "string",
  "summary": "string",
  "key_points": ["string", "string", "string"],
  "people_or_organizations": ["string", "string"],
  "timeline": ["string", "string"],
  "why_it_matters": "string",
  "simplified_explanation": "string",
  "suggested_questions": ["string", "string", "string"],
  "confidence": "high | medium | low"
}

Rules:

IMAGE AND CAPTION FILTER (CRITICAL):
- The document may contain image captions, photo descriptions, media credits, or image-related text
- These are NOT part of the actual news content
- Completely IGNORE:
  - image captions
  - photo descriptions
  - text describing what is shown in an image
  - media credits
  - lines or fragments containing words such as:
    "Photo", "Image", "Caption", "Credit", "Getty", "Reuters"
  - text that describes a scene instead of reporting a news event
- Do NOT use image-related text in:
  - summary
  - key_points
  - people_or_organizations
  - timeline
  - why_it_matters
- If unsure whether text is a caption or real article content, IGNORE it

GENERAL:
- title: infer the article title if possible; if unclear, provide a short descriptive title
- document_type: always use "news article"
- main_event: one short sentence describing the central event or development
- summary: concise but informative paragraph focused only on facts from the document
- key_points: 3 to 7 short factual points about the main developments

GROUNDING (VERY IMPORTANT):
- Use ONLY information explicitly stated in the document
- Do NOT invent facts, names, numbers, entities, forces, programs, or institutions
- Do NOT rename organizations, forces, missions, or programs
- Keep names exactly as they appear in the document
- Prefer omitting a detail over inventing or normalizing it

ENTITY EXTRACTION (CRITICAL):
- When listing people, organizations, forces, agencies, or other entities:
  - copy names EXACTLY as they appear in the document
  - do NOT paraphrase
  - do NOT shorten
  - do NOT generalize
  - do NOT create cleaner or more descriptive replacement names
- If a name is not explicitly written in the document, DO NOT include it
- Never create or infer names of military forces, operations, or programs
- Prefer missing an entity over inventing one

PEOPLE / ORGANIZATIONS:
- Include only people, organizations, or entities explicitly mentioned in the document
- Do NOT add logical guesses such as "government", "military", or "police" unless explicitly named
- If unclear, return []

TIMELINE (STRICT MODE):
- Timeline is ONLY for concrete news events
- Include only explicit real-world events, actions, decisions, announcements, arrivals, deployments, official report releases, starts, ends, or clearly stated changes
- Keep events in chronological order

TIMELINE HARD FILTER (STRICT):
- A timeline item MUST describe a concrete action or change that happened in the real world
- VALID examples:
  - forces arrived
  - an operation started
  - a decision was made
  - a report was officially released
  - deployment began

- Do NOT include:
  - reports describing a situation (e.g. "report highlights", "report shows")
  - statistical findings even if tied to a date
  - humanitarian or social conditions (e.g. people becoming homeless)

- A timeline event must describe:
  - an action taken
  - a force arriving
  - a decision made
  - a deployment starting
  - an operation beginning

- If the item describes the state of the world instead of an action → EXCLUDE it

- INVALID examples:
  - descriptions of people, places, or situations
  - anything that could be a photo description
  - static conditions
  - general background facts
  - statistics presented only as context
  - explanatory analysis
  - consequences without a clearly stated event
- If a line describes what is happening in general rather than a specific event, EXCLUDE it
- If unsure, EXCLUDE it
- Timeline must contain ONLY clear, action-based events

DO NOT include in timeline:
- statistics
- measurements
- background facts
- descriptive counts
- trend descriptions unless the article presents them as a dated reported development
- general conditions
- explanatory context
- consequences without a dated event
- image captions
- descriptive photo references
- publication metadata
- inferred dates
- speculative sequencing
- vague references like "recently" unless tied to a clear event already described in the text

TIMELINE DECISION RULE:
- Ask: "Did something happen on this date or in this period?"
- If the text only says how many, how much, how often, or how bad the situation is, DO NOT include it
- If the text is a statistic or background context, DO NOT include it
- If the text is not clearly an event, DO NOT include it

TIMELINE QUALITY RULE:
- It is better to return 0 to 3 clean timeline items than to include weak or questionable ones
- Prefer an empty list over a noisy timeline

WHY IT MATTERS:
- Explain importance based ONLY on the document’s content
- Avoid adding outside knowledge or assumptions

SIMPLIFICATION:
- simplified_explanation: explain the article in plain language

FOLLOW-UP:
- suggested_questions: 3 useful questions based only on the document content

CONFIDENCE:
- "high" if the main event, actors, and facts are clearly stated
- "medium" if some parts required light interpretation
- "low" if the document is unclear, incomplete, or noisy

FALLBACK:
- If something is unclear, return [] instead of guessing

- return only valid JSON
""".strip()

    user_prompt = f"""
Analyze the following news document and return the JSON.

DOCUMENT:
{document_text}
""".strip()

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

def clean_llm_json_response(raw_text: str) -> str:
    cleaned = raw_text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    return cleaned


def summarize_document_to_json(document_mode: str, document_text: str) -> dict:
    if document_mode == "research":
        messages = build_research_prompt(document_text)
        max_new_tokens = 1800
    elif document_mode == "news_article":
        messages = build_news_prompt(document_text)
        max_new_tokens = 1800
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


def print_research_summary(result: dict):
    print("📘 Title:", result.get("title"))
    print("📄 Document type:", result.get("document_type"))
    print("🏷 Main topic:", result.get("main_topic"))

    print("\n🎯 Research goal:\n")
    print(result.get("research_goal"))

    print("\n🧾 Summary:\n")
    print(result.get("summary"))

    print("\n🧪 Methodology:\n")
    print(result.get("methodology"))

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

    print("\n💡 Practical implications:")
    implications = result.get("practical_implications", [])
    if implications:
        for item in implications:
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

    print("\n📊 Confidence:", result.get("confidence"))


def print_news_summary(result: dict):
    print("📰 Title:", result.get("title"))
    print("📄 Document type:", result.get("document_type"))

    print("\n🚨 Main event:\n")
    print(result.get("main_event"))

    print("\n🧾 Summary:\n")
    print(result.get("summary"))

    print("\n📌 Key points:")
    key_points = result.get("key_points", [])
    if key_points:
        for item in key_points:
            print("-", item)
    else:
        print("- None found")

    print("\n👥 People or organizations:")
    actors = result.get("people_or_organizations", [])
    if actors:
        for item in actors:
            print("-", item)
    else:
        print("- None identified")

    print("\n🕒 Timeline:")
    timeline = result.get("timeline", [])
    if timeline:
        for item in timeline:
            print("-", item)
    else:
        print("- None identified")

    print("\n❗ Why it matters:\n")
    print(result.get("why_it_matters"))

    print("\n🧠 Simplified explanation:\n")
    print(result.get("simplified_explanation"))

    print("\n❓ Suggested questions:")
    questions = result.get("suggested_questions", [])
    if questions:
        for item in questions:
            print("-", item)
    else:
        print("- None")

    print("\n📊 Confidence:", result.get("confidence"))


def print_summary(result: dict):
    document_type = (result.get("document_type") or "").lower()

    if document_type == "research report":
        print_research_summary(result)
    elif document_type == "news article":
        print_news_summary(result)
    else:
        print("📄 Document type:", result.get("document_type"))
        print("\n🧾 Raw result:\n")
        print(json.dumps(result, indent=2, ensure_ascii=False))