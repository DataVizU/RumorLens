import type { ListData } from "@/types/Propagation/data";
import type { Text } from "@/types/Propagation/path";

export function getKeyword(data: ListData) {
  return data.data.key_words ? data.data.key_words[0] : "";
}

export function getTextStyle(data: ListData, textData: Text[]) {
  const pos = textData.find((item: Text) => item.name === data.ID);
  const wordLen = getKeyword(data)?.length;
  if (!pos) return;
  const angle =
    pos.angle > Math.PI / 2 && pos.angle < 1.5 * Math.PI
      ? -Math.PI + pos.angle
      : pos.angle;
  const translateX = pos.x;
  const tranlateY = pos.y;
  let display = "block";
  if (pos.radius * pos.angleDistance < wordLen * 9 || pos.radiusDistance < 12)
    display = "none";
  return `
        transform:translate(${translateX}px,${tranlateY}px) rotate(${angle}rad);
        display:${display};
    `;
}
