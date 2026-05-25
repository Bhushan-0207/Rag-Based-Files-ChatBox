function DocumentCard({
  document,
  onDelete,
  selectedDocuments,
  toggleDocument,
}) {
  const getFileIcon = () => {
    switch (document.file_type) {
      case "pdf":
        return "📄";
      case "docx":
        return "📝";
      case "xlsx":
        return "📊";
      case "pptx":
        return "📽️";
      default:
        return "📁";
    }
  };
  return (
    <div className="bg-white p-4 rounded-2xl border shadow-sm hover:shadow-lg transition">
      <div className="flex justify-between items-center mb-4">
        <input
          type="checkbox"
          checked={selectedDocuments.includes(document.filename)}
          onChange={() => toggleDocument(document.filename)}
          className="w-5 h-5"
        />
      </div>

      <div className="text-4xl mb-2">{getFileIcon()}</div>

      <h2 className="font-semibold wrap-break-words mb-2">
        {document.filename}
      </h2>

      <p className="text-sm text-gray-500 mb-1">
        Type: {document.file_type.toUpperCase()}
      </p>

      <p className="text-sm text-gray-500 mb-1">Size: {document.size} KB</p>

      <p className="text-sm text-gray-500">Uploaded: {document.uploaded_at}</p>
      <button
        onClick={() => onDelete(document.filename)}
        className="mt-3 w-full bg-red-600 text-white py-2 rounded-lg hover:bg-red-700"
      >
        Delete
      </button>
    </div>
  );
}

export default DocumentCard;
