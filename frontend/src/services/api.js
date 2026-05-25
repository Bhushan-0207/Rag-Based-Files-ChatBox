import axios from "axios";

const API = axios.create({
    baseURL:"http://127.0.0.1:8000"
})

export const chat = (query) => API.post("/chat",{query});

export const getDocuments = () => API.get("/documents");

export const uploadDocument = (data) =>API.post("/upload",data,{
    headers:{
        "Content-Type":"multipart/form-data"
    }
}) 

export const deleteDocument = (filename) => API.delete(`/documents/${filename}`);