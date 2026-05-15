export default function PricingCard({ pricing }) {

  const estimatedPrice = pricing?.estimated_price ?? 0;

  return (
    <div className="p-4 bg-zinc-900 rounded-xl">

      <h3 className="text-lg font-semibold">
        Estimated Price
      </h3>

      <div className="text-3xl font-bold mt-2">
        ${estimatedPrice.toLocaleString()}
      </div>

    </div>
  );
}