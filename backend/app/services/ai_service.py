"""AI service for embeddings and content generation using Anthropic Claude."""
from typing import List, Optional, Dict, Any
import anthropic
import google.generativeai as genai
import json
import re

from app.core.config import settings
from app.models.schemas import GenerationType


class AIService:
    """Handles AI operations including embeddings and text generation with Anthropic Claude."""

    GENERATION_PROMPTS = {
        GenerationType.REPORT: """Genera un informe profesional y detallado basado en la información proporcionada.
El informe debe incluir:
- Resumen ejecutivo
- Puntos principales
- Análisis detallado
- Conclusiones y recomendaciones

Usa un tono formal y estructura clara con secciones bien definidas.""",

        GenerationType.EMAIL: """Redacta un correo electrónico profesional basado en la información proporcionada.
El correo debe incluir:
- Asunto apropiado (marca como [ASUNTO]: )
- Saludo cordial
- Cuerpo del mensaje claro y conciso
- Cierre apropiado

Mantén un tono profesional pero amigable.""",

        GenerationType.SUMMARY: """Crea un resumen conciso y claro de la información proporcionada.
El resumen debe:
- Capturar los puntos más importantes
- Ser fácil de leer y entender
- Mantener la esencia de la información original
- Estar organizado de forma lógica""",

        GenerationType.ANALYSIS: """Realiza un análisis profundo de la información proporcionada.
El análisis debe incluir:
- Identificación de patrones y tendencias
- Puntos fuertes y áreas de mejora
- Comparaciones relevantes
- Insights y observaciones clave
- Recomendaciones basadas en el análisis""",

        GenerationType.PRESENTATION: """Crea el contenido para una presentación basada en la información proporcionada.
Estructura el contenido en diapositivas:
- Diapositiva de título
- Agenda/Índice
- Contenido principal (3-5 diapositivas con puntos clave)
- Conclusiones
- Siguientes pasos o llamada a la acción

Usa viñetas y mantén el texto conciso.""",

        GenerationType.LETTER: """Redacta una carta formal basada en la información proporcionada.
La carta debe incluir:
- Fecha
- Destinatario
- Saludo formal
- Cuerpo de la carta
- Despedida formal
- Firma""",

        GenerationType.MEMO: """Crea un memorando interno basado en la información proporcionada.
El memo debe incluir:
- Para:
- De:
- Fecha:
- Asunto:
- Cuerpo del mensaje
- Acciones requeridas (si aplica)""",

        GenerationType.CUSTOM: """Genera contenido basado en la información proporcionada siguiendo las instrucciones del usuario.""",
    }

    TONE_INSTRUCTIONS = {
        "professional": "Usa un tono profesional y formal.",
        "casual": "Usa un tono casual y conversacional.",
        "formal": "Usa un tono muy formal y corporativo.",
        "friendly": "Usa un tono amigable y cercano.",
    }

    LENGTH_INSTRUCTIONS = {
        "short": "Mantén la respuesta breve y al punto (máximo 200 palabras).",
        "medium": "Proporciona una respuesta de longitud moderada (300-500 palabras).",
        "long": "Proporciona una respuesta detallada y completa (más de 500 palabras).",
    }

    def __init__(self):
        """Initialize Anthropic and Google clients."""
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.chat_model = "claude-sonnet-4-20250514"

        # Initialize Google Gemini for charts/graphs
        genai.configure(api_key=settings.google_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for a list of texts using Gemini.
        """
        if not texts:
            return []

        embeddings = []
        for text in texts:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document"
            )
            embeddings.append(result['embedding'])

        return embeddings

    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for a single text using Gemini."""
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']

    def generate_content(
        self,
        prompt: str,
        context: str,
        generation_type: GenerationType,
        language: str = "es",
        tone: str = "professional",
        length: str = "medium",
        additional_instructions: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate content based on context and type using Claude.
        """
        system_prompt = self._build_system_prompt(
            generation_type, language, tone, length, additional_instructions
        )

        user_prompt = f"""Solicitud del usuario: {prompt}

Información de contexto de los documentos:
---
{context}
---

Por favor, genera el contenido solicitado basándote en esta información."""

        response = self.client.messages.create(
            model=self.chat_model,
            max_tokens=4000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )

        return {
            "content": response.content[0].text,
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
        }

    def chat_with_context(
        self,
        messages: List[Dict[str, str]],
        context: str,
    ) -> Dict[str, Any]:
        """
        Have a conversation with document context using Claude.
        """
        system_message = f"""Eres DocuMind AI, un asistente de IA especializado en analizar documentos y responder preguntas.
Tienes acceso a la siguiente información de los documentos del usuario:

---
{context}
---

Responde las preguntas basándote en esta información. Si no encuentras la respuesta en los documentos,
indícalo claramente. Siempre sé preciso y útil. Responde en español a menos que el usuario pida otro idioma.

IMPORTANTE: Si el usuario pide gráficos, tablas o visualizaciones, genera el contenido en formato Markdown
con tablas bien formateadas. Para gráficos, describe los datos y sugiere el tipo de gráfico apropiado."""

        # Convert messages to Anthropic format
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        response = self.client.messages.create(
            model=self.chat_model,
            max_tokens=2000,
            system=system_message,
            messages=anthropic_messages,
        )

        return {
            "message": response.content[0].text,
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
        }

    def answer_query(self, query: str, context: str) -> str:
        """
        Answer a simple query based on context using Claude.
        """
        system_prompt = """Eres un asistente experto en analizar documentos.
Responde la pregunta del usuario basándote únicamente en el contexto proporcionado.
Si la información no está en el contexto, indica que no tienes suficiente información.
Sé conciso pero completo. Responde en español.

Si te piden datos numéricos o estadísticas, formatea la respuesta con tablas Markdown cuando sea apropiado."""

        user_prompt = f"""Contexto de los documentos:
---
{context}
---

Pregunta: {query}"""

        response = self.client.messages.create(
            model=self.chat_model,
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )

        return response.content[0].text

    def generate_chart_data(self, prompt: str, context: str) -> Dict[str, Any]:
        """
        Generate chart/graph data based on context using Gemini.
        Returns structured data for frontend visualization.
        """
        chart_prompt = f"""Analiza el siguiente contexto y genera datos para un gráfico basado en la solicitud del usuario.

Contexto:
{context}

Solicitud: {prompt}

Responde SOLO con un JSON válido con esta estructura:
{{
    "chart_type": "bar" | "line" | "pie" | "table",
    "title": "Título del gráfico",
    "labels": ["etiqueta1", "etiqueta2", ...],
    "datasets": [
        {{
            "label": "Serie 1",
            "data": [valor1, valor2, ...]
        }}
    ],
    "table_data": [
        {{"columna1": "valor", "columna2": "valor"}}
    ]
}}

Si no hay datos numéricos claros, usa chart_type "table" y proporciona los datos en table_data."""

        try:
            response = self.gemini_model.generate_content(chart_prompt)
            text = response.text

            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                chart_data = json.loads(json_match.group())
                return {"success": True, "data": chart_data}
            else:
                return {"success": False, "error": "No se pudieron extraer datos para el gráfico"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _build_system_prompt(
        self,
        generation_type: GenerationType,
        language: str,
        tone: str,
        length: str,
        additional_instructions: Optional[str],
    ) -> str:
        """Build the system prompt for content generation."""
        base_prompt = self.GENERATION_PROMPTS.get(
            generation_type, self.GENERATION_PROMPTS[GenerationType.CUSTOM]
        )

        tone_instruction = self.TONE_INSTRUCTIONS.get(tone, self.TONE_INSTRUCTIONS["professional"])
        length_instruction = self.LENGTH_INSTRUCTIONS.get(length, self.LENGTH_INSTRUCTIONS["medium"])

        language_map = {
            "es": "español",
            "en": "inglés",
            "fr": "francés",
            "pt": "portugués",
            "de": "alemán",
        }
        language_name = language_map.get(language, "español")

        prompt = f"""{base_prompt}

{tone_instruction}
{length_instruction}
Escribe en {language_name}.

IMPORTANTE: Cuando sea apropiado, incluye:
- Tablas en formato Markdown para datos estructurados
- Listas numeradas o con viñetas para puntos clave
- Secciones claramente separadas con encabezados"""

        if additional_instructions:
            prompt += f"\n\nInstrucciones adicionales: {additional_instructions}"

        return prompt


# Singleton instance
ai_service = AIService()
