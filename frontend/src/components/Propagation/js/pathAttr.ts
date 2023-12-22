import type { ListData } from "@/types/Propagation/data";
import {
  SELECTED_COLOR,
  NEGATIVE_COLOR,
  NEUTRAL_COLOR,
  POSITIVE_COLOR,
  RIGHT_SELECTED_COLOR,
} from "@/components/Propagation/js/public_def";
import type { Path } from "@/types/Propagation/path";

export function findD(id: string, pathData: Path[]) {
  const res = pathData.find((item) => {
    return item.name === id;
  });
  return res?.d || "";
}

export function getColor(
  data: ListData,
  father: string[],
  son: string[],
  selected: string | undefined,
  rightSelected: string | undefined
) {
  let color: string;
  if (
    father.includes(data.ID) ||
    son.includes(data.ID) ||
    (!selected && rightSelected !== data.ID)
  ) {
    if (Number(data.data.emotion) > 0) color = POSITIVE_COLOR;
    else if (Number(data.data.emotion) < 0) color = NEGATIVE_COLOR;
    else color = NEUTRAL_COLOR;
  } else if (rightSelected === data.ID) color = RIGHT_SELECTED_COLOR;
  else color = SELECTED_COLOR;

  return color;
}
