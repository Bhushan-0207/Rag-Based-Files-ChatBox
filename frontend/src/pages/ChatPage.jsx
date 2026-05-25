import Sidebar from "../components/Sidebar";
import ChatBox from "../components/ChatBox";

function ChatPage() {

  return (

    <div className="h-screen flex bg-gray-100">

      {/* Sidebar */}
      <Sidebar />

      {/* Chat */}
      <div className="flex-1">

        <ChatBox />

      </div>

    </div>
  );
}

export default ChatPage;