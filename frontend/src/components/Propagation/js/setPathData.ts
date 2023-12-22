import type { ListData, RawData } from "@/types/Propagation/data";
import type {
  TimeData,
  TimeDataValueValue,
  TimeDataValueValueChild,
} from "@/types/Propagation/data";
import * as d3 from "d3";
import type { Path, Text } from "@/types/Propagation/path";
import type { DefaultArcObject } from "d3";
import { LEVEL_MARGIN } from "@/components/Propagation/js/public_def";

export function getListData(data: RawData): ListData[] {
  const listData: ListData[] = [];
  Object.entries(data).forEach(([id, item]) => {
    const tmp: ListData = {
      ID: id,
      data: item,
    };
    listData.push(tmp);
  });
  return listData;
}

export function getPathData(
  data: TimeData,
  sumArr: number[],
  actualRadius: number
) {
  let innerR = 0;
  const pathData: Path[] = [];
  const textData: Text[] = [];
  const levelNum = sumArr.length;
  // 不懂scale，interval这些数据的公式是怎么得到的
  const scale = (actualRadius / (actualRadius + 15 * levelNum)) * 1.1;
  const sumTotal = d3.sum(sumArr);
  Object.entries(data).forEach(([level, item]) => {
    const levelSum = sumArr[Number(level.slice(5))];
    const interval =
      (Math.sqrt(actualRadius ** 2 * (levelSum / sumTotal) + innerR ** 2) -
        innerR) *
      scale; // 每个圆环之间的间隔
    let angle = 0; // 每个圆环的起始角度
    Object.entries(item).forEach(([, value]) => {
      const ratio = value.sum / levelSum; // 每个圆环的占比
      const { path, text } = getSinglePath(
        ratio,
        value,
        innerR,
        interval,
        angle
      );
      pathData.push(...path);
      textData.push(...text);
      angle += ratio * 2 * Math.PI; // 下一个圆环的起始角度
    });
    innerR += interval + LEVEL_MARGIN; // 下一个圆环的内半径
  });
  return {
    path: pathData,
    text: textData,
  };
}

export function getSinglePath(
  ratio: number,
  data: TimeDataValueValue,
  innerR: number,
  interval: number,
  angle: number
) {
  const pathData: Path[] = [];
  const textData: Text[] = [];
  const width = 100 * (interval / 2 + innerR) * 3.14,
    height = 100 * interval;
  // @ts-ignore d3-error
  const root = d3.hierarchy(data).sum((d: TimeDataValueValueChild) => {
    return d.size;
  });
  const treemap = d3.treemap().size([width, height]); // 创建一个treemap布局，设置大小和内边距
  const tree = treemap(root); // 传入根结点，得到处理后的根结点
  const leaves = tree.leaves(); // 获得叶子节点
  leaves.forEach((item) => {
    const arc = d3
      .arc()
      .innerRadius(innerR + (item.y0 * interval) / height) // 不懂公式咋来的
      .outerRadius(innerR + (item.y1 * interval) / height);
    const angles = {
      startAngle: (item.x0 / (width / ratio)) * Math.PI * 2 + angle,
      endAngle: (item.x1 / (width / ratio)) * Math.PI * 2 + angle,
    };
    const path: Path = {
      name: (item.data as TimeDataValueValueChild).name,
      d: arc(angles as DefaultArcObject),
    };
    const textAngle = (angles.startAngle + angles.endAngle) / 2;
    const angleDistance = angles.endAngle - angles.startAngle;
    const [x, y] = arc.centroid(angles as DefaultArcObject);
    const radiusDistance = ((item.y1 - item.y0) * interval) / height;
    const textRadius =
      (innerR +
        (item.y0 * interval) / height +
        innerR +
        (item.y1 * interval) / height) /
      2;
    const text: Text = {
      name: (item.data as TimeDataValueValueChild).name,
      x,
      y,
      angle: textAngle,
      angleDistance,
      radiusDistance,
      radius: textRadius,
    };
    textData.push(text);
    pathData.push(path);
  });
  return {
    path: pathData,
    text: textData,
  };
}

export function getSon(item: ListData, data: ListData[]): string[] {
  if (item.data.son.length === 0) {
    return [];
  }
  return item.data.son.flatMap((sonID) => {
    // flatMap() 方法首先使用映射函数映射每个元素，然后将结果压缩成一个新数组。
    const sonNode = data.find((node) => node.ID === sonID);
    if (!sonNode) return [];
    return [sonID, ...getSon(sonNode, data)];
  });
}

export function getFather(item: ListData, data: ListData[]): string[] {
  if (item.data.level <= 0) return [];
  const fatherNode = data.find((node) => node.data.son?.includes(item.ID));
  if (!fatherNode) return [];
  return [fatherNode.ID, ...getFather(fatherNode, data)];
}
