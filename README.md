![Logo](.assets/logo.png)

[![Mistral AI](https://img.shields.io/badge/Built%20with-Mistral%20AI-9B59B6?logo=mistralai&logoColor=orange)](https://mistral.ai/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://www.python.otg)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-blue?logo=langgraph&logoColor=skyblue)](https://langchain.com/langgraph)

VPipeline is an AI-powered video creation pipeline that transforms a single topic into a fully narrated documentary workflow. The current implementation generates formatted narration and high-quality audio, with the long-term goal of producing complete cinematic videos automatically. 

> [!NOTE] 
> **Current Status:** VPipeline generates narrated audio (`.wav`). 
> 
> **Final Goal:** Generate complete, fully automated `.mp4` documentary videos with narration, visuals, animations, typography, maps, and procedural graphics. 

---
## Vision
Traditional video creation requires researching, writing, recording, editing, sourcing visuals, synchronizing narration, and rendering everything together. 

Pipeline aims to automate that entire workflow through specialized AI agents.

---

## Planned Features 

- AI-generated visuals 
- Dynamic typography 
- Animated diagrams 
- Geographic maps 
- Point-cloud visualizations 
- Timeline animation
- Procedural graphics 
- Automatic video editing 
- MP4 rendering 
- Multiple TTS providers 
- Multiple LLM providers

> [!IMPORTANT]
> Already reached till `.mp4` in [previous version](https://github.com/DevankSinghChaudhary/video-creation-pipeline/).


## Project Status 
VPipeline is under active development. 

The audio generation pipeline is operational. Visual generation, animation, and final video rendering are currently being developed. 

---

## Clone & Run

### 1. Clone the repository

```bash
git clone https://github.com/DevankSinghChaudhary/VPipeline.git
cd VPipeline
```

---

### 2. Download the required dataset

VPipeline uses the **Natural Earth GeoPackage** as its base world dataset.

Download the latest GeoPackage:

* https://www.naturalearthdata.com/downloads/
* Direct download: https://naciscdn.org/naturalearth/packages/natural_earth_vector.gpkg.zip

Extract the downloaded archive and obtain:

```text
natural_earth_vector.gpkg
```

---

### 3. Place the dataset

Move the GeoPackage into:

```text
src/vcp/globe/packages/
```

Your structure should look like:

```text
src/
└── vcp/
    └── globe/
        ├── packages/
        │   └── natural_earth_vector.gpkg
        └── extracted/
```

---

### 4. Create extraction folders

```bash
cd src/vcp/globe

mkdir -p extracted/10m
mkdir -p extracted/50m
mkdir -p extracted/110m
```

Result:

```text
globe/
├── packages/
│   └── natural_earth_vector.gpkg
└── extracted/
    ├── 10m/
    ├── 50m/
    └── 110m/
```

---

### 5. Extract Natural Earth layers

Run:

```bash
uv run main.py
```

The extractor automatically:

* Reads every layer from the Natural Earth GeoPackage.
* Categorizes each layer into **10m**, **50m**, or **110m** datasets.
* Converts every layer into an individual GeoJSON file.
* Places the generated files inside the corresponding `extracted/` directory.

Example:

```text
extracted/
├── 10m/
│   ├── ne_10m_land.geojson
│   ├── ne_10m_coastline.geojson
│   ├── ...
├── 50m/
│   ├── ne_50m_land.geojson
│   ├── ...
└── 110m/
    ├── ne_110m_land.geojson
    └── ...
```

> The extraction process only needs to be performed once unless the Natural Earth dataset is updated.


## License 

[MIT](https://github.com/DevankSinghChaudhary/VPipeline/tree/main?tab=MIT-1-ov-file)
