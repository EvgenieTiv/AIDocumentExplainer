function renderList(items) {
  if (!items || items.length === 0) {
    return <div>- None identified</div>;
  }

  return (
    <ul style={{ marginTop: "8px", paddingLeft: "20px" }}>
      {items.map((item, index) => (
        <li key={index}>{item}</li>
      ))}
    </ul>
  );
}

function Section({ title, children }) {
  return (
    <div style={{ marginTop: "20px" }}>
      <h3 style={{ marginBottom: "8px" }}>{title}</h3>
      <div>{children}</div>
    </div>
  );
}

function ResearchView({ result }) {
  return (
    <>
      <h2>{result.title}</h2>
      <div><strong>Type:</strong> {result.document_type}</div>
      <div><strong>Main topic:</strong> {result.main_topic}</div>

      <Section title="Research goal">
        <div>{result.research_goal}</div>
      </Section>

      <Section title="Summary">
        <div>{result.summary}</div>
      </Section>

      <Section title="Methodology">
        <div>{result.methodology}</div>
      </Section>

      <Section title="Key findings">
        {renderList(result.key_findings)}
      </Section>

      <Section title="Limitations">
        {renderList(result.limitations)}
      </Section>

      <Section title="Practical implications">
        {renderList(result.practical_implications)}
      </Section>

      <Section title="Simplified explanation">
        <div>{result.simplified_explanation}</div>
      </Section>

      <Section title="Suggested questions">
        {renderList(result.suggested_questions)}
      </Section>

      <Section title="Confidence">
        <div>{result.confidence}</div>
      </Section>
    </>
  );
}

function NewsView({ result }) {
  return (
    <>
      <h2>{result.title}</h2>
      <div><strong>Type:</strong> {result.document_type}</div>

      <Section title="Main event">
        <div>{result.main_event}</div>
      </Section>

      <Section title="Summary">
        <div>{result.summary}</div>
      </Section>

      <Section title="Key points">
        {renderList(result.key_points)}
      </Section>

      <Section title="People or organizations">
        {renderList(result.people_or_organizations)}
      </Section>

      <Section title="Timeline">
        {renderList(result.timeline)}
      </Section>

      <Section title="Why it matters">
        <div>{result.why_it_matters}</div>
      </Section>

      <Section title="Simplified explanation">
        <div>{result.simplified_explanation}</div>
      </Section>

      <Section title="Suggested questions">
        {renderList(result.suggested_questions)}
      </Section>

      <Section title="Confidence">
        <div>{result.confidence}</div>
      </Section>
    </>
  );
}

function InstructionView({ result }) {
  return (
    <>
      <h2>{result.title}</h2>
      <div><strong>Type:</strong> {result.document_type}</div>

      <Section title="Goal">
        <div>{result.goal}</div>
      </Section>

      <Section title="Summary">
        <div>{result.summary}</div>
      </Section>

      <Section title="Prerequisites">
        {renderList(result.prerequisites)}
      </Section>

      <Section title="Main steps">
        {result.main_steps && result.main_steps.length > 0 ? (
          <ol style={{ marginTop: "8px", paddingLeft: "20px" }}>
            {result.main_steps.map((item, index) => (
              <li key={index} style={{ marginBottom: "6px" }}>{item}</li>
            ))}
          </ol>
        ) : (
          <div>- None identified</div>
        )}
      </Section>

      <Section title="Warnings or common mistakes">
        {renderList(result.warnings_or_common_mistakes)}
      </Section>

      <Section title="Expected result">
        <div>{result.expected_result}</div>
      </Section>

      <Section title="Simplified explanation">
        <div>{result.simplified_explanation}</div>
      </Section>

      <Section title="Confidence">
        <div>{result.confidence}</div>
      </Section>
    </>
  );
}

function InsightView({ result }) {
  return (
    <>
      <h2>{result.title}</h2>
      <div><strong>Type:</strong> {result.document_type}</div>
      <div><strong>Main topic:</strong> {result.main_topic}</div>

      <Section title="Summary">
        <div>{result.summary}</div>
      </Section>

      <Section title="Key insights">
        {renderList(result.key_insights)}
      </Section>

      <Section title="Important patterns or trends">
        {renderList(result.important_patterns_or_trends)}
      </Section>

      <Section title="Notable facts">
        {renderList(result.notable_facts)}
      </Section>

      <Section title="Limitations or uncertainties">
        {renderList(result.limitations_or_uncertainties)}
      </Section>

      <Section title="Simplified explanation">
        <div>{result.simplified_explanation}</div>
      </Section>

      <Section title="Confidence">
        <div>{result.confidence}</div>
      </Section>
    </>
  );
}

function SummaryModeView({ result }) {
  return (
    <>
      <h2>{result.title}</h2>
      <div><strong>Type:</strong> {result.document_type}</div>
      <div><strong>Main subject:</strong> {result.main_subject}</div>

      <Section title="Summary">
        <div>{result.summary}</div>
      </Section>

      <Section title="Key points">
        {renderList(result.key_points)}
      </Section>

      <Section title="Simplified explanation">
        <div>{result.simplified_explanation}</div>
      </Section>

      <Section title="Confidence">
        <div>{result.confidence}</div>
      </Section>
    </>
  );
}

function ResultsView({ result }) {
  if (!result) {
    return null;
  }

  const documentType = (result.document_type || "").toLowerCase();

  return (
    <div
      style={{
        marginTop: "24px",
        padding: "20px",
        border: "1px solid #ccc",
        borderRadius: "8px",
        backgroundColor: "#fafafa",
      }}
    >
      {documentType === "research report" && <ResearchView result={result} />}
      {documentType === "news article" && <NewsView result={result} />}
      {documentType === "instruction" && <InstructionView result={result} />}
      {documentType === "insight" && <InsightView result={result} />}
      {documentType === "summary" && <SummaryModeView result={result} />}

      {![
        "research report",
        "news article",
        "instruction",
        "insight",
        "summary",
      ].includes(documentType) && (
        <>
          <h2>{result.title || "Document result"}</h2>
          <div>This document type is not yet supported in the UI.</div>
        </>
      )}
    </div>
  );
}

export default ResultsView;