# DocuMind AI - Repositorio Inteligente de Documentos

Una aplicacion web que permite subir documentos y generar contenido inteligente usando IA. Funciona como un repositorio de datos donde puedes:

- **Subir documentos**: PDF, Word, Excel, PowerPoint, Markdown, texto plano
- **Hacer preguntas**: "Que dice el documento sobre X tema?"
- **Generar informes**: "Hazme un informe basado en estos documentos"
- **Crear correos**: "Escribe un correo sobre este tema"
- **Obtener resumenes**: "Resume los puntos principales"
- **Analizar datos**: "Analiza las tendencias en estos documentos"

## Arquitectura

```
DocuMind AI/
├── backend/                 # API FastAPI (Python)
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   ├── core/           # Configuracion
│   │   ├── models/         # Schemas Pydantic
│   │   └── services/       # Logica de negocio
│   ├── uploads/            # Documentos subidos
│   └── chroma_db/          # Base de datos vectorial
│
└── frontend/               # Interfaz React
    └── src/
        ├── components/     # Componentes reutilizables
        ├── pages/          # Paginas de la aplicacion
        ├── services/       # Cliente API
        └── styles/         # Estilos CSS/Tailwind
```

## Tecnologias

### Backend
- **FastAPI**: Framework web moderno y rapido
- **ChromaDB**: Base de datos vectorial para embeddings
- **OpenAI**: Embeddings y generacion de texto
- **LangChain**: Orquestacion de LLM
- **PyPDF2, python-docx, openpyxl**: Procesamiento de documentos

### Frontend
- **React 18**: Interfaz de usuario
- **Vite**: Build tool moderno
- **Tailwind CSS**: Estilos utilitarios
- **React Router**: Navegacion SPA
- **Axios**: Cliente HTTP

## Requisitos

- Python 3.9+
- Node.js 18+
- OpenAI API Key

## Instalacion

### 1. Clonar el repositorio

```bash
git clone https://github.com/Paups02/K-RED90-Cropify-AI.git
cd K-RED90-Cropify-AI
```

### 2. Configurar el backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o: venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tu OPENAI_API_KEY
```

### 3. Configurar el frontend

```bash
cd frontend

# Instalar dependencias
npm install
```

## Ejecucion

### Iniciar el backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El API estara disponible en: http://localhost:8000
Documentacion Swagger: http://localhost:8000/docs

### Iniciar el frontend

```bash
cd frontend
npm run dev
```

La aplicacion estara disponible en: http://localhost:3000

## Uso

### 1. Subir documentos

1. Ve a la seccion "Documentos"
2. Arrastra archivos o haz clic para seleccionar
3. Espera a que se procesen

### 2. Generar contenido

1. Ve a la seccion "Generar"
2. Selecciona el tipo de contenido (informe, correo, resumen, etc.)
3. Escribe tu solicitud
4. Configura tono y longitud
5. Haz clic en "Generar contenido"

### 3. Chat con documentos

1. Ve a la seccion "Chat"
2. Escribe preguntas sobre tus documentos
3. Recibe respuestas basadas en la informacion cargada

## API Endpoints

### Documentos

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| POST | `/api/documents/upload` | Subir documento |
| GET | `/api/documents/` | Listar documentos |
| GET | `/api/documents/{id}` | Obtener documento |
| DELETE | `/api/documents/{id}` | Eliminar documento |

### Generacion

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| POST | `/api/generate/content` | Generar contenido |
| POST | `/api/generate/query` | Consultar documentos |
| POST | `/api/generate/chat` | Chat conversacional |
| GET | `/api/generate/types` | Tipos de generacion |

## Tipos de contenido

- **report**: Informe profesional con resumen ejecutivo
- **email**: Correo electronico profesional
- **summary**: Resumen conciso
- **analysis**: Analisis detallado
- **presentation**: Contenido para diapositivas
- **letter**: Carta formal
- **memo**: Memorando interno
- **custom**: Contenido personalizado

## Formatos soportados

- PDF (.pdf)
- Microsoft Word (.docx, .doc)
- Microsoft Excel (.xlsx, .xls)
- Microsoft PowerPoint (.pptx, .ppt)
- Texto plano (.txt)
- Markdown (.md)

## Configuracion

### Variables de entorno (.env)

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Aplicacion
APP_NAME=DocuMind AI
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Subida de archivos
MAX_UPLOAD_SIZE=52428800  # 50MB
ALLOWED_EXTENSIONS=pdf,docx,txt,md,xlsx,pptx

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_db

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Desarrollo

### Estructura del backend

```
backend/app/
├── api/
│   ├── documents.py    # Endpoints de documentos
│   └── generate.py     # Endpoints de generacion
├── core/
│   └── config.py       # Configuracion
├── models/
│   └── schemas.py      # Modelos Pydantic
├── services/
│   ├── document_processor.py  # Extraccion de texto
│   ├── vector_store.py        # ChromaDB
│   └── ai_service.py          # OpenAI
└── main.py             # Aplicacion FastAPI
```

### Estructura del frontend

```
frontend/src/
├── components/
│   ├── Layout.jsx          # Layout principal
│   ├── FileUpload.jsx      # Zona de subida
│   ├── DocumentList.jsx    # Lista de documentos
│   ├── GenerationForm.jsx  # Formulario de generacion
│   ├── ContentResult.jsx   # Resultado generado
│   └── ChatInterface.jsx   # Interfaz de chat
├── pages/
│   ├── Home.jsx            # Pagina principal
│   ├── Documents.jsx       # Gestion de documentos
│   ├── Generate.jsx        # Generacion de contenido
│   └── Chat.jsx            # Chat con documentos
└── services/
    └── api.js              # Cliente API
```

## Licencia

MIT License

## Autor

Desarrollado para Cropify-AI
