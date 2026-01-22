import React from 'react';
import { FileText, Trash2, Calendar, Database } from 'lucide-react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

const fileTypeColors = {
  pdf: 'bg-red-100 text-red-700',
  docx: 'bg-blue-100 text-blue-700',
  doc: 'bg-blue-100 text-blue-700',
  txt: 'bg-gray-100 text-gray-700',
  md: 'bg-purple-100 text-purple-700',
  xlsx: 'bg-green-100 text-green-700',
  xls: 'bg-green-100 text-green-700',
  pptx: 'bg-orange-100 text-orange-700',
  ppt: 'bg-orange-100 text-orange-700',
};

export default function DocumentList({ documents, onDelete, loading }) {
  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  if (loading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="card animate-pulse">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gray-200 rounded-lg" />
              <div className="flex-1">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
                <div className="h-3 bg-gray-200 rounded w-1/2" />
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (!documents || documents.length === 0) {
    return (
      <div className="card text-center py-12">
        <FileText className="w-16 h-16 mx-auto text-gray-300 mb-4" />
        <h3 className="text-lg font-medium text-gray-600 mb-2">
          No hay documentos
        </h3>
        <p className="text-gray-500">
          Sube documentos para empezar a usar el asistente de IA
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {documents.map((doc) => (
        <div
          key={doc.id}
          className="card hover:shadow-md transition-shadow"
        >
          <div className="flex items-start gap-4">
            <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
              fileTypeColors[doc.file_type] || 'bg-gray-100 text-gray-700'
            }`}>
              <span className="text-sm font-bold uppercase">
                {doc.file_type}
              </span>
            </div>

            <div className="flex-1 min-w-0">
              <h3 className="font-medium text-gray-900 truncate">
                {doc.filename}
              </h3>
              <div className="flex flex-wrap items-center gap-4 mt-2 text-sm text-gray-500">
                <span className="flex items-center gap-1">
                  <Database className="w-4 h-4" />
                  {formatFileSize(doc.file_size)}
                </span>
                <span className="flex items-center gap-1">
                  <Calendar className="w-4 h-4" />
                  {format(new Date(doc.upload_date), "d 'de' MMMM, yyyy", { locale: es })}
                </span>
                <span className="badge badge-blue">
                  {doc.chunk_count} fragmentos
                </span>
              </div>
            </div>

            <button
              onClick={() => onDelete(doc.id)}
              className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
              title="Eliminar documento"
            >
              <Trash2 className="w-5 h-5" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
