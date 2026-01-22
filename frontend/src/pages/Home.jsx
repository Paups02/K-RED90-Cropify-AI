import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  FileText,
  Upload,
  Sparkles,
  MessageSquare,
  ArrowRight,
  Database,
  Zap,
  Shield
} from 'lucide-react';
import { statsApi } from '../services/api';

const features = [
  {
    icon: Upload,
    title: 'Sube tus documentos',
    description: 'PDF, Word, Excel, PowerPoint, Markdown y mas formatos soportados',
    color: 'bg-blue-500',
  },
  {
    icon: Sparkles,
    title: 'Genera contenido',
    description: 'Informes, correos, resumenes, analisis y mas con un solo clic',
    color: 'bg-purple-500',
  },
  {
    icon: MessageSquare,
    title: 'Chatea con tus datos',
    description: 'Haz preguntas en lenguaje natural y obtén respuestas precisas',
    color: 'bg-green-500',
  },
];

const benefits = [
  {
    icon: Zap,
    title: 'Rapido y eficiente',
    description: 'Procesa documentos en segundos',
  },
  {
    icon: Shield,
    title: 'Seguro y privado',
    description: 'Tus datos permanecen en tu servidor',
  },
  {
    icon: Database,
    title: 'Base de conocimiento',
    description: 'Construye tu repositorio inteligente',
  },
];

export default function Home() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await statsApi.get();
      setStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  return (
    <div className="space-y-12">
      {/* Hero */}
      <div className="text-center py-12">
        <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
          <FileText className="w-10 h-10 text-white" />
        </div>
        <h1 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
          DocuMind AI
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
          Tu repositorio inteligente de documentos. Sube, consulta y genera contenido
          con el poder de la inteligencia artificial.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/documents" className="btn btn-primary px-8 py-3 text-lg">
            <Upload className="w-5 h-5" />
            Empezar ahora
          </Link>
          <Link to="/generate" className="btn btn-outline px-8 py-3 text-lg">
            <Sparkles className="w-5 h-5" />
            Ver demo
          </Link>
        </div>
      </div>

      {/* Stats */}
      {stats && stats.total_documents > 0 && (
        <div className="grid grid-cols-3 gap-4 max-w-2xl mx-auto">
          <div className="card text-center">
            <p className="text-3xl font-bold text-primary-600">{stats.total_documents}</p>
            <p className="text-sm text-gray-500">Documentos</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl font-bold text-primary-600">{stats.total_chunks}</p>
            <p className="text-sm text-gray-500">Fragmentos</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl font-bold text-primary-600">{stats.total_size_mb}</p>
            <p className="text-sm text-gray-500">MB procesados</p>
          </div>
        </div>
      )}

      {/* Features */}
      <div>
        <h2 className="text-2xl font-bold text-center text-gray-900 mb-8">
          Como funciona?
        </h2>
        <div className="grid md:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div key={index} className="card hover:shadow-lg transition-shadow">
                <div className={`w-14 h-14 ${feature.color} rounded-xl flex items-center justify-center mb-4`}>
                  <Icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Benefits */}
      <div className="bg-gradient-to-br from-primary-50 to-primary-100 rounded-2xl p-8">
        <h2 className="text-2xl font-bold text-center text-gray-900 mb-8">
          Por que DocuMind AI?
        </h2>
        <div className="grid md:grid-cols-3 gap-6">
          {benefits.map((benefit, index) => {
            const Icon = benefit.icon;
            return (
              <div key={index} className="flex items-start gap-4">
                <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center flex-shrink-0 shadow-sm">
                  <Icon className="w-5 h-5 text-primary-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">{benefit.title}</h3>
                  <p className="text-sm text-gray-600">{benefit.description}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* CTA */}
      <div className="text-center py-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Listo para empezar?
        </h2>
        <p className="text-gray-600 mb-6">
          Sube tu primer documento y experimenta el poder de la IA
        </p>
        <Link to="/documents" className="btn btn-primary px-8 py-3 text-lg inline-flex">
          Subir documentos
          <ArrowRight className="w-5 h-5 ml-2" />
        </Link>
      </div>
    </div>
  );
}
