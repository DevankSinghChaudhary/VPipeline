export type TypographyLayoutItem = {
  id: string;
  width: number;
  height: number;
  gapAfter?: number;
};

export type PositionedTypographyItem = TypographyLayoutItem & {
  x: number;
  y: number;
};

export function layoutTypography(
  items: TypographyLayoutItem[],
  defaultGap = 0.35,
): PositionedTypographyItem[] {
  let cursorX = 0;

  return items.map((item) => {
    const positioned: PositionedTypographyItem = {
      ...item,
      x: cursorX + item.width / 2,
      y: 0,
    };

    cursorX += item.width + (item.gapAfter ?? defaultGap);

    return positioned;
  });
}

