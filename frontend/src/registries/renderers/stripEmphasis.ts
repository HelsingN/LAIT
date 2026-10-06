/** Drop emphasis markers. Identifier underscores between letters or digits stay. */
export function stripEmphasis(text: string): string {
  const withoutStars = text.replaceAll("**", "").replaceAll("*", "");
  return withoutStars.replace(/_(?![A-Za-z0-9])|(?<![A-Za-z0-9])_/g, "");
}
