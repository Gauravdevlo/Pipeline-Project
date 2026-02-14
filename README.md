# VectorShift Pipeline Builder

A modern visual pipeline builder with drag-and-drop functionality, real-time validation, and stunning animated UI. Built as part of the VectorShift Frontend Technical Assessment.

## 🎥 Demo Video

[Click to Watch Demo](https://github.com/Gauravdevlo/Pipeline-Project/blob/main/Gourav_Yadav_screenrecording.mp4)

> **Note:** Replace the video URL above with your actual video. To add video to GitHub:
> 1. Edit this README on GitHub
> 2. Drag and drop your MP4 file into the editor
> 3. GitHub will automatically upload and generate a URL

Alternatively, [**watch the full demo here**](YOUR_GOOGLE_DRIVE_LINK).

## ✨ Features

### Core Functionality
- 🎨 **Drag & Drop Interface** - Intuitive node-based workflow builder
- 🔗 **Visual Connections** - Connect nodes with animated gradient edges
- ✅ **DAG Validation** - Real-time detection of circular dependencies
- 📊 **Pipeline Analysis** - Automatic counting of nodes and edges
- 📝 **Smart Text Node** - Auto-resizing with variable detection (`{{variable}}` syntax)

### UI/UX Highlights
- 💫 **Smooth Animations** - GSAP 3D tilt effects and Framer Motion transitions
- 🌈 **Glass Morphism** - Modern frosted glass design
- 🎪 **Animated Background** - Particle system with gradient orbs
- ⚡ **Live Stats** - Real-time node and edge counting
- 🎨 **Beautiful Alerts** - Custom modals with animations

### Available Nodes
- **Input/Output** 📥📤 - Data entry and exit points
- **LLM** 🤖 - Language model integration
- **Text** 📝 - Dynamic text with variable handles
- **Transform** 🔄 - Data transformation operations
- **Filter** 🔍 - Conditional filtering
- **Conditional** 🔀 - Branch logic
- **API** 🌐 - HTTP request handling
- **Delay** ⏱️ - Timed delays

## 🚀 Installation & Setup

### Prerequisites
- Node.js (v14+)
- Python (v3.8+)
- npm or yarn

### Backend Setup
```bash
cd backend

# Install dependencies
pip install fastapi uvicorn pydantic

# Start server
uvicorn main:app --reload
```

Backend runs on **http://localhost:8000**

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install --legacy-peer-deps

# Start development server
npm start
```

Frontend runs on **http://localhost:3000**

## 📖 Usage Guide

### Creating Your First Pipeline

1. **Add Nodes**
   - Drag any node from the palette at the top
   - Drop it onto the canvas
   - Configure the node's settings

2. **Connect Nodes**
   - Click and drag from a node's output handle (right side)
   - Connect to another node's input handle (left side)
   - Watch the animated connection appear

3. **Text Node Variables**
   - Type `{{variableName}}` in a text field
   - Purple handles automatically appear on the left
   - Connect data sources to these handles

4. **Submit Pipeline**
   - Click "Submit Pipeline" button
   - View results: node count, edge count, and DAG validation

### Example Pipelines

**Simple Chain (Valid DAG):**
```
Input → Text → LLM → Output
✅ Valid DAG
```

**With Branching (Valid DAG):**
```
        ┌→ Transform → Output1
Input → LLM
        └→ Filter → Output2
✅ Valid DAG
```

**With Cycle (Invalid):**
```
Input → LLM → Text → Output
  ↑                      ↓
  └──────────────────────┘
❌ Cycle Detected
```

**Text Node with Variables:**
```
Type: "Hello {{name}}, your order {{orderId}} is ready!"
Result: 2 purple handles appear for 'name' and 'orderId'
```

## 🏗️ Project Structure
```
vectorshift-pipeline-builder/
├── backend/
│   ├── main.py                      # FastAPI server with DAG validation
│   └── test_main.py                 # Backend unit tests
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── AnimatedBackground.js    # Particle background
│   │   ├── nodes/
│   │   │   ├── baseNode.js              # Node abstraction
│   │   │   ├── inputNode.js
│   │   │   ├── outputNode.js
│   │   │   ├── llmNode.js
│   │   │   ├── textNode.js              # With variable detection
│   │   │   ├── transformNode.js
│   │   │   ├── filterNode.js
│   │   │   ├── delayNode.js
│   │   │   ├── apiNode.js
│   │   │   └── conditionalNode.js
│   │   ├── App.js                       # Main application
│   │   ├── ui.js                        # React Flow canvas
│   │   ├── toolbar.js                   # Node palette
│   │   ├── draggableNode.js             # Draggable wrapper
│   │   ├── submit.js                    # Submit & validation
│   │   ├── store.js                     # Zustand state
│   │   └── index.css                    # Global styles
│   ├── package.json
│   └── tailwind.config.js
│
└── README.md
```

## 🔧 Technical Implementation

### Part 1: Node Abstraction
Created a flexible `BaseNode` component that allows rapid creation of new nodes through configuration objects. This reduces code duplication and ensures consistency across all node types.

### Part 2: Styling
Implemented modern UI with:
- Glass morphism effects with backdrop blur
- Gradient animations using GSAP
- Smooth transitions with Framer Motion
- Responsive Tailwind CSS design
- Dark theme with colorful accents

### Part 3: Text Node Logic
- **Auto-resizing**: Node dimensions adjust based on text length
- **Variable Detection**: Regex pattern `/\{\{\s*([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\}\}/g`
- **Dynamic Handles**: Purple handles auto-generate on the left for each variable

### Part 4: Backend Integration
- **Frontend**: Sends nodes/edges to `/pipelines/parse` endpoint
- **Backend**: Uses Kahn's algorithm for DAG validation
- **Response**: Returns `{num_nodes, num_edges, is_dag}`
- **UI**: Beautiful animated modal displays results

## 📡 API Documentation

### `GET /`
Health check endpoint
```json
Response: { "Ping": "Pong" }
```

### `POST /pipelines/parse`
Validate pipeline structure

**Request:**
```json
{
  "nodes": [
    { "id": "node-1" },
    { "id": "node-2" }
  ],
  "edges": [
    { "source": "node-1", "target": "node-2" }
  ]
}
```

**Response:**
```json
{
  "num_nodes": 2,
  "num_edges": 1,
  "is_dag": true
}
```

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pip install pytest
pytest test_main.py -v
```

**Test Coverage:**
- Simple DAG validation
- Circular dependency detection
- Empty pipeline handling
- Branching structures
- Self-loops
- Disconnected components
- Complex cycles

### Manual Testing Scenarios
1. ✅ Create simple chain: Input → LLM → Output
2. ❌ Create cycle: Input → LLM → Output → Input
3. ✅ Test text variables: `{{name}}` and `{{email}}`
4. ✅ Empty canvas submission
5. ✅ Disconnected node groups

## 🛠️ Tech Stack

### Frontend
- **React** 18.3.1 - UI framework
- **React Flow** - Node-based editor
- **Framer Motion** - Animation library
- **GSAP** - 3D animations
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **Lucide React** - Icons

### Backend
- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Algorithms
- **Kahn's Algorithm** - Topological sorting for DAG validation
- **DFS** - Cycle detection alternative

## 🐛 Troubleshooting

**Backend not connecting?**
```bash
# Check if backend is running
curl http://localhost:8000

# Restart backend
uvicorn main:app --reload
```

**Frontend dependency errors?**
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

**CORS errors?**
- Ensure backend is running on port 8000
- Check CORS configuration in `main.py`

## 📦 Deployment

### Backend (Railway/Render)
```bash
# Create requirements.txt
pip freeze > requirements.txt

# Deploy to your platform
```

### Frontend (Vercel/Netlify)
```bash
# Build production bundle
npm run build

# Deploy 'build' folder
```

## 🎯 Future Enhancements

- [ ] Undo/Redo functionality
- [ ] Copy/Paste nodes
- [ ] Export/Import pipeline JSON
- [ ] Node search and filtering
- [ ] Keyboard shortcuts
- [ ] Multi-select nodes
- [ ] Minimap enhancements
- [ ] Real-time collaboration
- [ ] Pipeline templates
- [ ] Custom node creation UI

## 📄 License

This project is created for the VectorShift Technical Assessment.

## 🙏 Acknowledgments

- VectorShift for the technical assessment opportunity
- React Flow for the excellent graph library
- Framer Motion for smooth animations
- FastAPI community

---

**⭐ If you found this project interesting, please give it a star!**

Built with ❤️ for VectorShift Technical Assessment
```
