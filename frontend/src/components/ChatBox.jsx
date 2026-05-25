import MessageBubble from "../components/MessageBubble";
import { chat } from "../services/api";
import { useState } from "react";

function ChatBox(setSelectedFile, setSelectedPage) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  
  const sendMessage = async () => {
    if (!query.trim()) return;
    
    const selectedDocuments = JSON.parse(
      localStorage.getItem("selectedDocuments") || "[]",
    );

    const userMessage = {
      id: Date.now(),
      sender: "user",
      text: query,
      filters: {
        sources:selectedDocuments
      }
    };

    setMessages((prev) => [...prev, userMessage]);

    const currentQuery = query;
    console.log(currentQuery);

    setQuery("");
    
    setLoading(true);

    try {
      const response = await chat(currentQuery);
      const aiMessage = {
        id: Date.now() + 1,

        sender: "ai",

        text: response.data.answer,

        sources: response.data.sources,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {loading && (
          <div className="text-gray-500">
            <span className="inline-block h-5 w-5 border-2 border-t-blue-500 rounded-full animate-spin"></span>{" "}
            Thinking...
          </div>
        )}
      </div>

      <div className="p-4 border-t bg-white">
        <div className="flex gap-3">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Ask anything..."
            className="flex-1 border rounded-lg p-3 outline-none"
          />

          <button
            onClick={sendMessage}
            className="bg-black text-white px-5 rounded-lg"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatBox;
