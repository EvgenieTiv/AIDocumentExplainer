const MODE_OPTIONS = [
  { value: "research", label: "Research" },
  { value: "news_article", label: "News" },
  { value: "instruction", label: "Instruction" },
  { value: "insight", label: "Insight" },
  { value: "summary", label: "Summary" },
];

function ModeSelector({ value, onChange, disabled = false }) {
  return (
    <div>
      <label htmlFor="document-mode">Document type</label>
      <br />
      <select
        id="document-mode"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
      >
        {MODE_OPTIONS.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}

export default ModeSelector;