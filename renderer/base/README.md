# VPipeline Base Typography Renderer v2

Typography-only Remotion renderer.

Changes from v1:
- removed per-frame noise generation
- removed 90 radial gradients
- generated one 256x256 fine-grain noise tile
- reused the same tile for every frame
- much subtler effective noise
- audio remains relative to public/

Expected:
public/audio/2.wav

Run:
npx remotion studio ./index.ts

Render:
npx remotion render ./index.ts VPipelineBaseTypography out/base.mp4
