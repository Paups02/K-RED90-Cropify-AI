import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Copy, Check, Download, FileText } from 'lucide-react';
import toast from 'react-hot-toast';

export default function ContentResult({ result }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result.content);
      setCopied(true);
      toast.success('Copiado al portapapeles');
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      toast.error('Error al copiar');
    }
  };

  const handleDownload = () => {
    const blob = new Blob([result.content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${result.generation_type}_${Date.now()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success('Archivo descargado');
  };

  if (!result) return null;

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
            <FileText className="w-5 h-5 text-primary-600" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">
              Contenido generado
            </h3>
            <p className="text-sm text-gray-500">
              Tipo: {result.generation_type} | Tokens: {result.tokens_used}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="btn btn-secondary"
          >
            {copied ? (
              <Check className="w-4 h-4" />
            ) : (
              <Copy className="w-4 h-4" />
            )}
            {copied ? 'Copiado' : 'Copiar'}
          </button>
          <button
            onClick={handleDownload}
            className="btn btn-secondary"
          >
            <Download className="w-4 h-4" />
            Descargar
          </button>
        </div>
      </div>

      {result.sources_used && result.sources_used.length > 0 && (
        <div className="mb-4 p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">
            <strong>Fuentes utilizadas:</strong> {result.sources_used.join(', ')}
          </p>
        </div>
      )}

      <div className="prose prose-sm max-w-none bg-gray-50 p-6 rounded-lg border border-gray-200 markdown-content">
        <ReactMarkdown>{result.content}</ReactMarkdown>
      </div>
    </div>
  );
}
