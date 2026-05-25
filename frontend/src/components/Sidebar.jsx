import {
  Link,
  useLocation
} from "react-router-dom";

function Sidebar() {

  const location =
    useLocation();

  return (

    <div className="w-72 bg-white border-r p-6">

      <h1 className="text-3xl font-bold mb-10">

        AI RAG ChatBot

      </h1>

      <div className="space-y-3">

        <Link
          to="/"
          className={`block p-3 rounded-lg ${
            location.pathname === "/"
              ? "bg-black text-white"
              : "bg-gray-100"
          }`}
        >
          RAG Chatbot
        </Link>

        <Link
          to="/documents"
          className={`block p-3 rounded-lg ${
            location.pathname === "/documents"
              ? "bg-black text-white"
              : "bg-gray-100"
          }`}
        >
          Documents
        </Link>

      </div>

    </div>
  );
}

export default Sidebar;