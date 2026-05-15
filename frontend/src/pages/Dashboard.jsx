import { useState } from "react";

import CreatorForm from "../components/forms/CreatorForm";
import PricingCard from "../components/cards/PricingCard";
import ConfidenceCard from "../components/cards/ConfidenceCard";
import ReasoningPanel from "../components/cards/ReasoningPanel";

import { createCreatorPricing } from "../api/creatorApi";

export default function Dashboard() {
  const [creatorData, setCreatorData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCreatorSubmit = async (formData) => {
    try {
      setLoading(true);
      setError(null);

      const response = await createCreatorPricing(formData);

      setCreatorData(response);

    } catch (err) {
      console.error("❌ DASHBOARD ERROR:", err);
      setError(err.message || "Failed to analyze creator");
      setCreatorData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white p-8">
      <div className="max-w-6xl mx-auto space-y-8">

        <h1 className="text-3xl font-bold">
          Creator Intelligence Dashboard
        </h1>

        <CreatorForm
          onSubmit={handleCreatorSubmit}
          loading={loading}
        />

        {loading && (
          <p className="text-zinc-400">
            Analyzing creator...
          </p>
        )}

        {error && (
          <div className="bg-red-500/10 border border-red-500 text-red-400 p-4 rounded-xl">
            {error}
          </div>
        )}

        <div className="text-green-400 text-sm">
          DEBUG: {creatorData
            ? JSON.stringify(creatorData, null, 2)
            : "waiting for data..."}
        </div>

        {creatorData?.pricing && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

            <PricingCard pricing={creatorData.pricing} />

            <ConfidenceCard confidence={creatorData.confidence} />

            <ReasoningPanel reasoning={creatorData.reasoning} />

          </div>
        )}

      </div>
    </div>
  );
}