import React, { useState } from 'react';
import { Sparkles } from 'lucide-react';
import GenerationForm from '../components/GenerationForm';
import ContentResult from '../components/ContentResult';

export default function Generate() {
  const [result, setResult] = useState(null);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
          <Sparkles className="w-7 h-7 text-primary-600" />
          Generar contenido
        </h1>
        <p className="text-gray-600 mt-1">
          Crea informes, correos, resumenes y mas basados en tus documentos
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Form */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Configura tu solicitud
          </h2>
          <GenerationForm onResult={setResult} />
        </div>

        {/* Result */}
        <div>
          {result ? (
            <ContentResult result={result} />
          ) : (
            <div className="card text-center py-16 bg-gray-50 border-dashed">
              <Sparkles className="w-16 h-16 mx-auto text-gray-300 mb-4" />
              <h3 className="text-lg font-medium text-gray-600 mb-2">
                Tu contenido aparecera aqui
              </h3>
              <p className="text-gray-500 max-w-md mx-auto">
                Selecciona un tipo de contenido, escribe tu solicitud y haz clic
                en "Generar contenido"
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
