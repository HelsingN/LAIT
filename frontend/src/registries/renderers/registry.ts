import type { ComponentType } from "react";

import { GapFillRenderer } from "./GapFillRenderer.tsx";
import { ProofRenderer } from "./ProofRenderer.tsx";
import type { RendererProps } from "./types.ts";

const renderers = new Map<string, ComponentType<RendererProps>>();

export function registerRenderer(exerciseType: string, renderer: ComponentType<RendererProps>): void {
  renderers.set(exerciseType, renderer);
}

export function rendererFor(exerciseType: string): ComponentType<RendererProps> | undefined {
  return renderers.get(exerciseType);
}

registerRenderer("gap-fill", GapFillRenderer);
// Maintainer/test mount. Dropping proof removes this line and ProofRenderer.tsx only.
registerRenderer("proof", ProofRenderer);

export type { PracticeItemView, RendererAnswer, RendererFeedback, RendererProps, UnitLabel } from "./types.ts";
