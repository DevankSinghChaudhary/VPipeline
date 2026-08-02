# VPipeline
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

## CLONE & RUN

### Clone:
git clone https://github.com/DevankSinghChaudhary/VPipeline.git
cd VPipeline

### Necessary data:
go to [Natural Earth](https://www.naturalearthdata.com/downloads/) and download [GeoPackage](https://naciscdn.org/naturalearth/packages/natural_earth_vector.gpkg.zip)

cd VPipeline/src/vcp/globe/
mkdir packages
(extract that .gpkg.zip in packages)
mkdir extracted
mkdir 10m 50m 110m

uv run main.py

---
## License 

MIT
