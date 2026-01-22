"""AI service for embeddings and content generation using OpenAI."""
from typing import List, Optional, Dict, Any
from openai import OpenAI

from app.core.config import settings
from app.models.schemas import GenerationType


class AIService:
    """Handles AI operations including embeddings and text generation."""

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
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.embedding_model = "text-embedding-3-small"
        self.chat_model = "gpt-4o-mini"

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for a list of texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        # OpenAI has a limit on batch size
        embeddings = []
        batch_size = 100

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            response = self.client.embeddings.create(
                model=self.embedding_model, input=batch
            )
            embeddings.extend([item.embedding for item in response.data])

        return embeddings

    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for a single text."""
        response = self.client.embeddings.create(
            model=self.embedding_model, input=text
        )
        return response.data[0].embedding

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
        Generate content based on context and type.

        Args:
            prompt: User's prompt/request
            context: Relevant document context
            generation_type: Type of content to generate
            language: Output language
            tone: Tone of the content
            length: Desired length
            additional_instructions: Extra instructions

        Returns:
            Generated content and metadata
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

        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=4000,
        )

        return {
            "content": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens,
        }

    def chat_with_context(
        self,
        messages: List[Dict[str, str]],
        context: str,
    ) -> Dict[str, Any]:
        """
        Have a conversation with document context.

        Args:
            messages: Conversation history
            context: Relevant document context

        Returns:
            Assistant response and metadata
        """
        system_message = f"""Eres un asistente de IA especializado en analizar documentos y responder preguntas.
Tienes acceso a la siguiente información de los documentos del usuario:

---
{context}
---

Responde las preguntas basándote en esta información. Si no encuentras la respuesta en los documentos,
indícalo claramente. Siempre sé preciso y útil. Responde en español a menos que el usuario pida otro idioma."""

        chat_messages = [{"role": "system", "content": system_message}]
        chat_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=chat_messages,
            temperature=0.7,
            max_tokens=2000,
        )

        return {
            "message": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens,
        }

    def answer_query(self, query: str, context: str) -> str:
        """
        Answer a simple query based on context.

        Args:
            query: User's question
            context: Relevant document context

        Returns:
            Answer string
        """
        system_prompt = """Eres un asistente experto en analizar documentos.
Responde la pregunta del usuario basándote únicamente en el contexto proporcionado.
Si la información no está en el contexto, indica que no tienes suficiente información.
Sé conciso pero completo. Responde en español."""

        user_prompt = f"""Contexto de los documentos:
---
{context}
---

Pregunta: {query}"""

        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
            max_tokens=1000,
        )

        return response.choices[0].message.content

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
Escribe en {language_name}."""

        if additional_instructions:
            prompt += f"\n\nInstrucciones adicionales: {additional_instructions}"

        return prompt


# Singleton instance
ai_service = AIService()
