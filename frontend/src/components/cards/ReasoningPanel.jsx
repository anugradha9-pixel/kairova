export default function ReasoningPanel({ reasoning }) {
  // SAFE NORMALIZATION
  const safeReasoning = Array.isArray(reasoning) ? reasoning : [];

  return (
    <div className="p-4 bg-zinc-900 rounded-xl">
      <h3 className="text-lg font-semibold mb-3">AI Reasoning</h3>

      {safeReasoning.length === 0 ? (
        <p className="text-sm text-zinc-500">
          No reasoning available
        </p>
      ) : (
        <ul className="space-y-2 text-sm text-zinc-300">
          {safeReasoning.map((item, index) => (
            <li key={index} className="flex gap-2">
              <span className="text-green-400">•</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}