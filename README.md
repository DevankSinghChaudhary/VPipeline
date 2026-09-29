![VPipeline Logo](.github/images/logo.png)

[![Mistral AI](https://img.shields.io/badge/Built%20with-Mistral%20AI-9B59B6?logo=mistralai\&logoColor=orange)](https://mistral.ai/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python\&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Built%20with-LangGraph-blue)](https://langchain.com/langgraph)

> [!IMPORTANT]
> **Current platform:** Linux tested. Windows and macOS are currently untested.

# VPipeline

**VPipeline is an AI-native video production pipeline that turns a topic into a structured documentary workflow.**

The project is designed to automate the repetitive parts of documentary production through specialized stages for research, writing, narration, visual planning, asset handling, composition, and rendering.

## Current Status

**Current working pipeline:**

```text
Topic
  ↓
Research
  ↓
Story
  ↓
Narration
  ↓
TTS
  ↓
WAV
```

The current implementation produces a narrated audio file (`.wav`).

The final goal is a complete automated documentary pipeline:

```text
Topic
  ↓
Research
  ↓
Story
  ↓
Narration
  ↓
TTS
  ↓
Visual Planning
  ↓
Asset Retrieval / Generation
  ↓
Composition
  ↓
Rendering
  ↓
MP4
```

> [!NOTE]
> A previous version of VPipeline already reached MP4 generation. See the [previous repository](https://github.com/DevankSinghChaudhary/video-creation-pipeline/).

## Vision

Creating a documentary normally requires research, writing, narration, visual sourcing, editing, synchronization, animation, and rendering.

VPipeline aims to turn those separate tasks into an automated, modular pipeline.

The long-term visual system includes:

* Dynamic typography
* Charts and data visualization
* Animated diagrams
* Geographic maps
* Timeline animation
* Procedural graphics
* Image and video assets
* Automated composition
* Final MP4 rendering

## Architecture

![VPipeline Structure](https://raw.githubusercontent.com/DevankSinghChaudhary/VPipeline/refs/heads/main/.github/images/vpipeline-structure.png)

VPipeline is built as a sequence of specialized stages rather than one model being responsible for the entire process.

## Project Status

VPipeline is under active development.

### Working

* Research
* Story generation
* Narration generation
* Text-to-speech
* Audio output

### In development

* Visual planning
* Asset retrieval
* Visual decomposition
* Composition
* Animation
* Final video rendering
* More independent AI components

## Requirements

### Software

* Python 3.12
* [uv](https://docs.astral.sh/uv/)
* Linux for the currently tested setup

### Hardware

The current local setup uses NVIDIA CUDA for AI workloads.

A GPU with approximately **6 GB VRAM** is recommended for the current local configuration because model memory is shared between components such as TTS/STT.

> [!NOTE]
> VRAM requirements may change as the pipeline evolves and models are replaced or optimized.

## Installation

### 1. Clone

```bash
git clone https://github.com/DevankSinghChaudhary/VPipeline.git
cd VPipeline
```

### 2. Install dependencies

```bash
uv sync
```

Install `uv` using the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

### 3. Run

```bash
uv run ...
```

Replace the command above with the current VPipeline entry point.

## Output

The current pipeline produces narrated audio:

```text
output/
└── narration.wav
```

## Development

VPipeline is experimental and actively changing.

The architecture, models, visual system, and interfaces may change significantly between releases.

## Roadmap

```text
[x] Research
[x] Story
[x] Narration
[x] TTS
[ ] Visual planning
[ ] Asset retrieval
[ ] Visual decomposition
[ ] Composition
[ ] Animation
[ ] Automated editing
[ ] MP4 rendering
[ ] Specialized decision models
```

## Contributing

VPipeline is open source. Contributions, experimentation, and ideas are welcome.

## License

[MIT License](LICENSE)

---

Built by **Devank Singh Chaudhary**.

