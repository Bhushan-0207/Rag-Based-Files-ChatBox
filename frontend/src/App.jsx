import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import ChatPage from "./pages/ChatPage";
import DocumentsPage from "./pages/DocumentPage";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<ChatPage />}
        />

        <Route
          path="/documents"
          element={<DocumentsPage />}
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;