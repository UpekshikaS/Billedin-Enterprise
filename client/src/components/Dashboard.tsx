export default function Dashboard() {
  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  return (
    <div className="text-center mt-10">
      <h1 className="text-2xl">Welcome to Dashboard</h1>
      <button
        className="mt-4 px-4 py-2 bg-red-600 text-white rounded"
        onClick={handleLogout}
      >
        Logout
      </button>
    </div>
  );
}
