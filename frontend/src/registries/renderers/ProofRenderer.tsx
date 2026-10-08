import type { RendererProps } from "./types.ts";

export function ProofRenderer({ item }: RendererProps) {
  return (
    <p data-testid="proof-renderer">
      {item.segments.map((segment, index) => (
        <span key={index}>{segment.text}</span>
      ))}
    </p>
  );
}
