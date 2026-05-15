import { useState } from "react";
import Input from "../shared/Input";
import Button from "../shared/Button";

export default function CreatorForm({ onSubmit, loading }) {

  const [form, setForm] = useState({
    name: "",
    niche: "",
    platform: "",
    followers: "",
    engagement_rate: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const payload = {
      name: form.name,
      niche: form.niche,
      platform: form.platform,
      followers: Number(form.followers),
      engagement_rate: Number(form.engagement_rate),
    };

    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">

      <Input
        type="text"
        name="name"
        placeholder="Creator Name"
        value={form.name}
        onChange={handleChange}
      />

      <Input
        type="text"
        name="niche"
        placeholder="Niche"
        value={form.niche}
        onChange={handleChange}
      />

      <Input
        type="text"
        name="platform"
        placeholder="Platform"
        value={form.platform}
        onChange={handleChange}
      />

      <Input
        type="number"
        name="followers"
        placeholder="Followers"
        value={form.followers}
        onChange={handleChange}
      />

      <Input
        type="number"
        step="0.1"
        name="engagement_rate"
        placeholder="Engagement Rate"
        value={form.engagement_rate}
        onChange={handleChange}
      />

      <Button type="submit" loading={loading}>
        Analyze Creator
      </Button>

    </form>
  );
}