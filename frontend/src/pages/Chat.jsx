import React from 'react';
import { MessageSquare } from 'lucide-react';
import ChatInterface from '../components/ChatInterface';

export default function Chat() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
          <MessageSquare className="w-7 h-7 text-primary-600" />
          Chat con documentos
        </h1>
        <p className="text-gray-600 mt-1">
          Haz preguntas sobre tus documentos en lenguaje natural
        </p>
      </div>

      {/* Chat interface */}
      <ChatInterface />
    </div>
  );
}
