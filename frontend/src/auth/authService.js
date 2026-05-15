import API from "../api/axios";

export const loginUser = async (email, password) => {
  try {
    const response = await API.post("/auth/login", {
      email,
      password,
    });

    console.log("🔐 LOGIN RESPONSE:", response.data);

    if (!response || !response.data) {
      throw new Error("Invalid login response");
    }

    return response.data;

  } catch (error) {
    console.error(
      "❌ LOGIN ERROR:",
      error?.response?.data || error.message
    );

    // Safe fallback (prevents app crash)
    return {
      success: false,
      token: null,
      message: "Login failed"
    };
  }
};