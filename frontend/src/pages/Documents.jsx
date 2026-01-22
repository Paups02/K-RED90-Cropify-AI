import React, { useState, useEffect } from 'react';
import { FileText, RefreshCw } from 'lucide-react';
import FileUpload from '../components/FileUpload';
import DocumentList from '../components/DocumentList';
import { documentsApi } from '../services/api';
import toast from 'react-hot-toast';

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    setLoading(true);
    try {
      const data = await documentsApi.list();
      setDocuments(data.documents || []);
    } catch (error) {
      toast.error('Error al cargar documentos');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (docId) => {
    if (!window.confirm('Estas seguro de eliminar este documento?')) return;

    try {
      await documentsApi.delete(docId);
      setDocuments((prev) => prev.filter((d) => d.id !== docId));
      toast.success('Documento eliminado');
    } catch (error) {
      toast.error('Error al eliminar documento');
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
            <FileText className="w-7 h-7 text-primary-600" />
            Documentos
          </h1>
          <p className="text-gray-600 mt-1">
            Gestiona tu repositorio de documentos
          </p>
        </div>
        <button
          onClick={loadDocuments}
          className="btn btn-secondary"
          disabled={loading}
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          Actualizar
        </button>
      </div>

      {/* Upload section */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Subir nuevos documentos
        </h2>
        <FileUpload onUploadComplete={loadDocuments} />
      </div>

      {/* Documents list */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Documentos cargados ({documents.length})
        </h2>
        <DocumentList
          documents={documents}
          onDelete={handleDelete}
          loading={loading}
        />
      </div>
    </div>
  );
}
