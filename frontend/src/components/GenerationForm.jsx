import React, { useState } from 'react';
import {
  FileText,
  Mail,
  FileSearch,
  BarChart,
  Presentation,
  PenTool,
  FileEdit,
  Sparkles,
  Loader2
} from 'lucide-react';
import { generateApi } from '../services/api';
import toast from 'react-hot-toast';

const generationTypes = [
  { id: 'report', name: 'Informe', icon: FileText, color: 'bg-blue-500' },
  { id: 'email', name: 'Correo', icon: Mail, color: 'bg-green-500' },
  { id: 'summary', name: 'Resumen', icon: FileSearch, color: 'bg-purple-500' },
  { id: 'analysis', name: 'Analisis', icon: BarChart, color: 'bg-orange-500' },
  { id: 'presentation', name: 'Presentacion', icon: Presentation, color: 'bg-pink-500' },
  { id: 'letter', name: 'Carta', icon: PenTool, color: 'bg-indigo-500' },
  { id: 'memo', name: 'Memo', icon: FileEdit, color: 'bg-yellow-500' },
  { id: 'custom', name: 'Personalizado', icon: Sparkles, color: 'bg-gray-500' },
];

const toneOptions = [
  { id: 'professional', name: 'Profesional' },
  { id: 'formal', name: 'Formal' },
  { id: 'casual', name: 'Casual' },
  { id: 'friendly', name: 'Amigable' },
];

const lengthOptions = [
  { id: 'short', name: 'Corto' },
  { id: 'medium', name: 'Medio' },
  { id: 'long', name: 'Largo' },
];

export default function GenerationForm({ onResult }) {
  const [selectedType, setSelectedType] = useState('report');
  const [prompt, setPrompt] = useState('');
  const [tone, setTone] = useState('professional');
  const [length, setLength] = useState('medium');
  const [additionalInstructions, setAdditionalInstructions] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) {
      toast.error('Por favor, escribe una solicitud');
      return;
    }

    setLoading(true);
    try {
      const result = await generateApi.content({
        prompt: prompt.trim(),
        generation_type: selectedType,
        language: 'es',
        tone,
        length,
        additional_instructions: additionalInstructions.trim() || null,
      });
      onResult(result);
      toast.success('Contenido generado correctamente');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Error al generar contenido');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Type selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Tipo de contenido
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {generationTypes.map((type) => {
            const Icon = type.icon;
            const isSelected = selectedType === type.id;
            return (
              <button
                key={type.id}
                type="button"
                onClick={() => setSelectedType(type.id)}
                className={`p-4 rounded-xl border-2 transition-all ${
                  isSelected
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className={`w-10 h-10 ${type.color} rounded-lg flex items-center justify-center mx-auto mb-2`}>
                  <Icon className="w-5 h-5 text-white" />
                </div>
                <span className={`text-sm font-medium ${
                  isSelected ? 'text-primary-700' : 'text-gray-600'
                }`}>
                  {type.name}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Prompt */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Que deseas generar?
        </label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Ej: Hazme un informe sobre las ventas del ultimo trimestre, o Escribe un correo solicitando una reunion..."
          className="textarea h-32"
          required
        />
      </div>

      {/* Options row */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tono
          </label>
          <select
            value={tone}
            onChange={(e) => setTone(e.target.value)}
            className="select"
          >
            {toneOptions.map((opt) => (
              <option key={opt.id} value={opt.id}>
                {opt.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Longitud
          </label>
          <select
            value={length}
            onChange={(e) => setLength(e.target.value)}
            className="select"
          >
            {lengthOptions.map((opt) => (
              <option key={opt.id} value={opt.id}>
                {opt.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Additional instructions */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Instrucciones adicionales (opcional)
        </label>
        <textarea
          value={additionalInstructions}
          onChange={(e) => setAdditionalInstructions(e.target.value)}
          placeholder="Ej: Incluye graficos de ejemplo, enfocate en los resultados positivos..."
          className="textarea h-20"
        />
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={loading || !prompt.trim()}
        className="btn btn-primary w-full py-3 text-lg"
      >
        {loading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Generando...
          </>
        ) : (
          <>
            <Sparkles className="w-5 h-5" />
            Generar contenido
          </>
        )}
      </button>
    </form>
  );
}
