import React, { useState } from 'react';
import { BarChart3, Loader2, Send, Table, LineChart, PieChart } from 'lucide-react';
import { generateApi } from '../services/api';
import ChartDisplay from '../components/ChartDisplay';
import toast from 'react-hot-toast';

export default function Charts() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [chartData, setChartData] = useState(null);
  const [sources, setSources] = useState([]);

  const exampleQueries = [
    "Genera un grafico de barras con los datos del documento",
    "Muestra una tabla con la informacion principal",
    "Crea un grafico de lineas con las tendencias",
    "Haz un grafico circular con la distribucion de datos",
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    setLoading(true);
    setChartData(null);

    try {
      const result = await generateApi.chart({ query: query.trim() });

      if (result.success) {
        setChartData(result.chart_data);
        setSources(result.sources || []);
        toast.success('Grafico generado correctamente');
      } else {
        toast.error(result.error || 'No se pudo generar el grafico');
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Error generando grafico');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Graficos y Tablas
        </h1>
        <p className="text-gray-600 mt-1">
          Genera visualizaciones a partir de tus documentos
        </p>
      </div>

      {/* Query Form */}
      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Describe el grafico que necesitas
            </label>
            <div className="flex gap-3">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ej: Genera un grafico de barras con las ventas mensuales..."
                className="input flex-1"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="btn btn-primary px-6"
              >
                {loading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </button>
            </div>
          </div>

          {/* Example queries */}
          <div className="flex flex-wrap gap-2">
            <span className="text-sm text-gray-500">Ejemplos:</span>
            {exampleQueries.map((example, index) => (
              <button
                key={index}
                type="button"
                onClick={() => setQuery(example)}
                className="text-sm px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-gray-700 transition-colors"
              >
                {example}
              </button>
            ))}
          </div>
        </form>
      </div>

      {/* Chart Types Info */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card bg-blue-50 border-blue-200">
          <div className="flex items-center gap-3">
            <BarChart3 className="w-8 h-8 text-blue-600" />
            <div>
              <h3 className="font-medium text-blue-900">Barras</h3>
              <p className="text-sm text-blue-700">Comparar valores</p>
            </div>
          </div>
        </div>
        <div className="card bg-green-50 border-green-200">
          <div className="flex items-center gap-3">
            <LineChart className="w-8 h-8 text-green-600" />
            <div>
              <h3 className="font-medium text-green-900">Lineas</h3>
              <p className="text-sm text-green-700">Tendencias</p>
            </div>
          </div>
        </div>
        <div className="card bg-purple-50 border-purple-200">
          <div className="flex items-center gap-3">
            <PieChart className="w-8 h-8 text-purple-600" />
            <div>
              <h3 className="font-medium text-purple-900">Circular</h3>
              <p className="text-sm text-purple-700">Distribuciones</p>
            </div>
          </div>
        </div>
        <div className="card bg-orange-50 border-orange-200">
          <div className="flex items-center gap-3">
            <Table className="w-8 h-8 text-orange-600" />
            <div>
              <h3 className="font-medium text-orange-900">Tablas</h3>
              <p className="text-sm text-orange-700">Datos estructurados</p>
            </div>
          </div>
        </div>
      </div>

      {/* Chart Result */}
      {chartData && (
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Resultado</h2>
          <ChartDisplay chartData={chartData} />

          {sources.length > 0 && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-sm text-gray-500">
                Fuentes: {sources.join(', ')}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Empty State */}
      {!chartData && !loading && (
        <div className="card text-center py-12">
          <BarChart3 className="w-16 h-16 mx-auto text-gray-300 mb-4" />
          <h3 className="text-lg font-medium text-gray-600 mb-2">
            No hay graficos generados
          </h3>
          <p className="text-gray-500 max-w-md mx-auto">
            Escribe una descripcion de lo que necesitas visualizar y generare
            un grafico basado en tus documentos.
          </p>
        </div>
      )}
    </div>
  );
}
