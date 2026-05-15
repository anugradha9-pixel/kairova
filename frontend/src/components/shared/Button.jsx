const Button = ({ children, loading, ...props }) => {
  return (
    <button
      {...props}
      disabled={loading}
      style={{
        padding: "10px 14px",
        marginTop: "10px",
        cursor: loading ? "not-allowed" : "pointer",
        opacity: loading ? 0.7 : 1,
        borderRadius: "6px",
        border: "1px solid #ddd",
      }}
    >
      {loading ? "Loading..." : children}
    </button>
  );
};

export default Button;