export default function ConfidenceCard({ confidence }) {
  // SAFE EXTRACTION
  const rawScore = confidence?.score;

  // normalize score safely
  let score = typeof rawScore === "number" ? rawScore : 0;

  // clamp between 0 and 1 (very important for SaaS stability)
  score = Math.max(0, Math.min(score, 1));

  const label = confidence?.label || "Unknown";

  return (
    <div className="p-4 bg-zinc-900 rounded-xl">
      <h3 className="text-lg font-semibold mb-2">Confidence Score</h3>

      <div className="text-2xl font-bold text-white">
        {Math.round(score * 100)}%
      </div>

      <p className="text-sm text-zinc-400 mt-1">
        {label}
      </p>
    </div>
  );
}