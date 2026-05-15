import API from "./axios";

export const createCreatorPricing = async (payload) => {

  try {
    const res = await API.post("/creator", payload);

    return res.data;

  } catch (err) {
    console.error("❌ FULL ERROR:", err);
    console.error("❌ RESPONSE ERROR:", err?.response?.data);

    // IMPORTANT: DO NOT hide error anymore
    throw err;
  }
};