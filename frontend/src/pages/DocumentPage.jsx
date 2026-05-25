import { useEffect, useState } from "react";

import Sidebar from "../components/Sidebar";
import DocumentCard from "../components/DocumentCard";
import { deleteDocument } from "../services/api";
import { uploadDocument } from "../services/api";
import { getDocuments } from "../services/api";

function DocumentsPage() {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectType, setSelectType] = useState("all");
  const [selectedDocuments, setSelectedDocuments] = useState([]);

  useEffect(() => {
    fetchDocuments();
    const savedDocs = localStorage.getItem("selectedDocuments");

    if (savedDocs) {
      setSelectedDocuments(JSON.parse(savedDocs));
    }
  }, []);

  const handleUpload = async (e) => {
    const files = e.target.files;

    if (!files.length) return;

    const formData = new FormData();

    for (let file of files) {
      formData.append("files", file);
    }

    setUploading(true);

    try {
      await uploadDocument(formData);
      fetchDocuments();
    } catch (error) {
      console.error(error);
    }

    setUploading(false);
  };

  const fetchDocuments = async () => {
    try {
      const res = await getDocuments();

      setDocuments(res.data.documents || []);
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  const handleDelete = async (filename) => {
    const confirmed = window.confirm(
      `Are you sure you want to delete ${filename}?`,
    );
    if (!confirmed) return;

    try {
      await deleteDocument(filename);

      fetchDocuments();
    } catch (error) {
      console.error(error);
    }
  };

  const filteredDcuments = documents.filter((doc) => {
    const matchesSearch = doc.filename
      .toLowerCase()
      .includes(searchTerm.toLowerCase());

    const matchesType = selectType === "all" || doc.file_type === selectType;

    return matchesSearch && matchesType;
  });

  const toggleDocument = (filename) => {
    let updatedDocs = [];

    setSelectedDocuments((prev) => {
      if (prev.includes(filename)) {
        updatedDocs = prev.filter((doc) => doc !== filename);
      } else {
        updatedDocs = [...prev, filename];
      }

      localStorage.setItem("selectedDocuments", JSON.stringify(updatedDocs));

      return updatedDocs;
    });
  };

  return (
    <div className="h-screen flex bg-gray-100">
      <Sidebar />

      <div className="flex-1 p-7 overflow-auto">
        <h1 className="text-3xl font-bold mb-6">Uploaded Documents</h1>
        <div className="bg-white p-6 rounded-xl border mb-6">
          <h2 className="text-xl font-semibold mb-4">Upload Documents</h2>

          <input type="file" multiple onChange={handleUpload} />

          {uploading && (
            <p className="mt-3 text-sm text-gray-500">
              Uploading and processing...
            </p>
          )}
        </div>

        <div className="flex gap-4 mb-8">
          <input
            type="text"
            placeholder="Search documents..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 p-3 rounded-xl border bg-white outline-none"
          />

          <select
            value={selectType}
            onChange={(e) => setSelectType(e.target.value)}
            className="p-3 rounded-xl border bg-white"
          >
            <option value="all">All</option>

            <option value="pdf">PDF</option>

            <option value="docx">DOCX</option>

            <option value="xlsx">XLSX</option>

            <option value="pptx">PPTX</option>
          </select>
        </div>
        <div className="mb-6">
          <p className="text-gray-600">
            Selected Documents: {selectedDocuments.length}
          </p>
        </div>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div className="grid grid-cols-3 gap-4">
            {filteredDcuments?.map((doc, index) => (
              <DocumentCard
                key={index}
                document={doc}
                onDelete={handleDelete}
                selectedDocuments={selectedDocuments}
                toggleDocument={toggleDocument}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default DocumentsPage;
