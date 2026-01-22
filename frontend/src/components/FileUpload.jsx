import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { documentsApi } from '../services/api';
import toast from 'react-hot-toast';

const ACCEPTED_TYPES = {
  'application/pdf': ['.pdf'],
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
  'application/msword': ['.doc'],
  'text/plain': ['.txt'],
  'text/markdown': ['.md'],
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
  'application/vnd.ms-excel': ['.xls'],
  'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
  'application/vnd.ms-powerpoint': ['.ppt'],
};

export default function FileUpload({ onUploadComplete }) {
  const [uploadingFiles, setUploadingFiles] = useState([]);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const newFiles = acceptedFiles.map((file) => ({
      file,
      id: Math.random().toString(36).substr(2, 9),
      status: 'uploading',
      progress: 0,
    }));

    setUploadingFiles((prev) => [...prev, ...newFiles]);

    for (const fileObj of newFiles) {
      try {
        await documentsApi.upload(fileObj.file);
        setUploadingFiles((prev) =>
          prev.map((f) =>
            f.id === fileObj.id ? { ...f, status: 'success' } : f
          )
        );
        toast.success(`${fileObj.file.name} subido correctamente`);
      } catch (error) {
        setUploadingFiles((prev) =>
          prev.map((f) =>
            f.id === fileObj.id
              ? { ...f, status: 'error', error: error.response?.data?.detail || 'Error al subir' }
              : f
          )
        );
        toast.error(`Error al subir ${fileObj.file.name}`);
      }
    }

    if (onUploadComplete) {
      onUploadComplete();
    }
  }, [onUploadComplete]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED_TYPES,
    maxSize: 50 * 1024 * 1024, // 50MB
  });

  const removeFile = (id) => {
    setUploadingFiles((prev) => prev.filter((f) => f.id !== id));
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
        {isDragActive ? (
          <p className="text-lg font-medium text-primary-600">
            Suelta los archivos aqui...
          </p>
        ) : (
          <>
            <p className="text-lg font-medium text-gray-700">
              Arrastra archivos aqui o haz clic para seleccionar
            </p>
            <p className="text-sm text-gray-500 mt-2">
              PDF, DOCX, TXT, MD, XLSX, PPTX (max. 50MB)
            </p>
          </>
        )}
      </div>

      {uploadingFiles.length > 0 && (
        <div className="space-y-2">
          {uploadingFiles.map((fileObj) => (
            <div
              key={fileObj.id}
              className="flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-200"
            >
              <File className="w-8 h-8 text-gray-400" />
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-800 truncate">
                  {fileObj.file.name}
                </p>
                <p className="text-sm text-gray-500">
                  {formatFileSize(fileObj.file.size)}
                </p>
              </div>
              <div className="flex items-center gap-2">
                {fileObj.status === 'uploading' && (
                  <Loader2 className="w-5 h-5 text-primary-600 animate-spin" />
                )}
                {fileObj.status === 'success' && (
                  <CheckCircle className="w-5 h-5 text-green-500" />
                )}
                {fileObj.status === 'error' && (
                  <AlertCircle className="w-5 h-5 text-red-500" />
                )}
                <button
                  onClick={() => removeFile(fileObj.id)}
                  className="p-1 hover:bg-gray-100 rounded"
                >
                  <X className="w-4 h-4 text-gray-400" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
