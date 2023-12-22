<template>
  <div class="all">
    <div class="title">Topic Evolution View</div>
    <div id="river"></div>
  </div>
</template>

<script setup lang="ts">
import * as d3 from "d3";
import { onMounted, ref, watch } from "vue";
import { getTopicData, sendRiverKeywords } from "@/api/api";
import type {
  TopicKeys,
  FinalData,
  Topics,
} from "@/types/Overview/ThemeRiver/keys";
import type {
  Keyword,
  RawKeyword,
  RawKeywordValue,
} from "@/types/Overview/ThemeRiver/keyword";
import type { NewData } from "@/types/Overview/ThemeRiver/newData";
import type { GroupedData } from "@/types/Overview/ThemeRiver/groupedData";
import type { Topic } from "@/types/Overview/ThemeRiver/topic";
import type { Pos } from "@/types/Overview/ThemeRiver/popTextPos";
import { storeToRefs } from "pinia";
import { useIdStore } from "@/stores/id";
import type { ScaleLinear } from "d3";
import type { ScaleTime } from "d3";
import { topicColour, topics } from "@/utils/topics";
import { Legend } from "@/utils/River/legendStyle";
import { TimeLine } from "@/utils/River/timeLineStyle";
import { River } from "@/utils/River/riverStyle";

const idStore = useIdStore();
const { idArrMap } = storeToRefs(idStore);
const mapData = ref<TopicKeys[]>([]);
const popTextTopic = ref<string>(""); // 用来存放点击的topic
const popTextPos = ref<Pos[]>([]); // 用来存放点击的topic的位置
const dataSortByTopic = ref<FinalData[]>([]);
const dataSortByTopicTotal = ref<FinalData[]>([]);
const mapDataTotal = ref<Date[]>([]);
const xDomain = ref<Date[]>([]);
const xDomainTotal = ref<Date[]>([]);
let keywordsId = ref<string[]>([]);
let svg: d3.Selection<SVGSVGElement, any, HTMLElement, any>;
let x: ScaleTime<number, number>, y: ScaleLinear<number, number>; // x,y轴的比例尺

async function updateTopicData() {
  const newRawData = (await getTopicData()) as string; // 得到的是字符串
  const newData: NewData = JSON.parse(newRawData); // 变成json对象
  const sortedData = sortData(newData);
  mapData.value = getFinalData(sortedData);
  mapDataTotal.value = JSON.parse(JSON.stringify(mapData.value)); // 深拷贝
  TopicData();
}

watch(idArrMap, () => {
  svg.selectAll(".keyword").remove();
  mapData.value = JSON.parse(JSON.stringify(mapDataTotal.value));
  for (let index in mapData.value) {
    for (let key in mapData.value[index].ids) {
      mapData.value[index].ids[key] = mapData.value[index].ids[key].filter(
        (id: string) => {
          return idArrMap.value?.includes(id);
        }
      );
      let topic = key as keyof Topics;
      mapData.value[index][topic] = mapData.value[index].ids[key].length;
    }
  }
  TopicData();
  dataSortByTime();
  drawMain();
});

const translate = new Map([
  ["社会时事", "Current Events"],
  ["国际", "World News"],
  ["娱乐", "Entertainment"],
  ["军事", "Military"],
  ["科技", "Technology"],
  ["历史文化", "Culture"],
  ["常识", "Common Sense"],
  ["母婴育儿", "Baby Care"],
  ["教育", "Education"],
  ["情感", "Affection"],
]); // 后端得到的是中文，要变成英文

function sortData(newData: NewData): TopicKeys[] {
  let sortedData = [];
  let key: keyof NewData;
  for (key in newData) {
    let newKeys: TopicKeys = {
      // 数组是引用类型，所以要每次都新建一个对象
      "Current Events": 0,
      "World News": 0,
      Entertainment: 0,
      Military: 0,
      Technology: 0,
      Culture: 0,
      "Common Sense": 0,
      "Baby Care": 0,
      Education: 0,
      Affection: 0,
      date: "",
      ids: {},
    };
    newKeys.date = newData[key].date;
    newData[key].topic.forEach(
      (item: { name: string; num: number; id: string[] }) => {
        let keyName: keyof TopicKeys;
        keyName = translate.get(item.name) as keyof TopicKeys;
        if (keyName === "date") {
          return;
        }
        if (keyName !== "ids") {
          newKeys[keyName] = item.num;
        }
        if (item.id) {
          newKeys["ids"][keyName] = item.id;
        }
      }
    );
    sortedData.push(newKeys);
  }
  sortedData.sort((a: TopicKeys, b: TopicKeys) => {
    if (a.date > b.date) {
      return 1;
    }
    return -1;
  });
  return sortedData;
}
function groupDataByWeek(data: TopicKeys[]): GroupedData {
  const format = d3.timeFormat("%Y-%b-%U");
  let groupedData: GroupedData = {};
  data.forEach((item: TopicKeys) => {
    let week = format(new Date(item.date));
    if (!groupedData[week]) {
      groupedData[week] = [item];
    } else {
      groupedData[week].push(item);
    }
  });
  return groupedData;
}
function calculateTopicKeys(data: TopicKeys[]) {
  let resKeys: Topics = {
    "Current Events": 0,
    "World News": 0,
    Entertainment: 0,
    Military: 0,
    Technology: 0,
    Culture: 0,
    "Common Sense": 0,
    "Baby Care": 0,
    Education: 0,
    Affection: 0,
  };
  data.forEach((item: TopicKeys) => {
    let key: keyof TopicKeys;
    for (key in item) {
      if (key !== "date" && key !== "ids") {
        resKeys[key] += item[key];
      }
    }
  });
  return resKeys;
}

function getIds(data: TopicKeys[]) {
  const ids: {
    [key: string]: string[];
  } = {};
  data.forEach((item: TopicKeys) => {
    for (let key in item.ids) {
      if (!ids[key]) {
        ids[key] = item.ids[key];
      } else {
        ids[key] = ids[key].concat(item.ids[key]);
      }
    }
  });
  return ids;
}
function getFinalData(data: TopicKeys[]) {
  const groupedData = groupDataByWeek(data);
  const res: TopicKeys[] = Object.entries(groupedData).map(([date, item]) => {
    let resKeys = calculateTopicKeys(item);
    let ids = getIds(item);
    return {
      date: date,
      ...resKeys,
      ids: ids,
    };
  });
  return res;
}

onMounted(async () => {
  await updateTopicData();
  svg = d3
    .select("#river")
    .append("svg")
    .attr("width", "100%")
    .attr("height", "100%");
  drawThemeRiver();
});

function popText(topic: string) {
  popTextPos.value = [];
  const datetoweek = d3.timeParse("%Y-%b-%U");
  const target = dataSortByTopic.value.find(
    (item: FinalData) => item.key === topic
  );
  if (!target) {
    return;
  }
  for (let mon = 1; mon <= 12; mon++) {
    let day, formatTime: any;
    if (mon === 8) day = 3;
    else if (mon === 10) day = 7;
    else day = 1;
    formatTime = d3.timeFormat("%Y-%b-%U")(new Date(`2020-${mon}-${day}`));
    let pos = { x: 0, y: 0 };
    pos.x = x(datetoweek(formatTime) as Date);
    let foundItem = target.values.find(
      (item: { date: string; number: number }) => item.date === formatTime
    );
    if (!foundItem) {
      continue;
    }
    pos.y = y(foundItem.number); // 找到对应的y值
    popTextPos.value[mon] = pos; // 把每个月的位置都存起来
  }
}

function setLegend() {
  const legend = svg
    .selectAll(".legend")
    .data(topicColour)
    .enter()
    .append("g")
    .attr("class", "legend")
    .attr("transform", function (d: Topic, i: number) {
      return (
        "translate(" +
        Legend.xOffsets +
        "," +
        (i * Legend.verticalSpacing + Legend.yOffsets) +
        ")"
      );
    });
  legend
    .append("rect")
    .attr("x", Legend.rectXOffsets)
    .attr("y", function (d: Topic, i: number) {
      return Legend.rectYOffsets + i * Legend.rectVerticalSpacing;
    })
    .attr("rx", Legend.rectR)
    .attr("ry", Legend.rectR)
    .attr("width", Legend.rectLength)
    .attr("height", Legend.rectLength)
    .style("fill", function (d: Topic) {
      return d.colour;
    });
  legend.on("click", (d: any) => {
    popTextTopic.value = d.target.__data__.topic;
    setRiverKeywords(popTextTopic.value as string);
    popText(popTextTopic.value as string);
  });
  legend
    .append("text")
    .attr("x", Legend.textXOffsets)
    .attr("y", function (d: Topic, i: number) {
      return Legend.textYOffsets + i * Legend.textVerticalSpacing;
    })
    .style("text-anchor", "start")
    .style("font", Legend.textSize)
    .text(function (d: Topic) {
      return d.topic;
    });
  svg
    .append("line")
    .attr("x1", Legend.lineXOffsets)
    .attr("y1", Legend.lineY1)
    .attr("x2", Legend.lineXOffsets)
    .attr("y2", Legend.lineY2)
    .attr("stroke", Legend.lineColor)
    .attr("stroke-width", Legend.lineStrokeWidth)
    .attr("opacity", Legend.lineOpacity);
}

async function setRiverKeywords(topic: string) {
  keywordsId.value = [];
  const target = dataSortByTopicTotal.value.find(
    (item: FinalData) => item.key === topic
  );
  if (!target) {
    return;
  }
  target.values.forEach((item: { date: string; number: number; ids: any }) => {
    if (item.ids !== undefined) {
      item.ids.forEach((id: string) => {
        keywordsId.value.push(id);
      });
    }
  });
  // idStore.setIdArr(keywordsId.value);
  const rawKeyword = (await sendRiverKeywords(keywordsId.value)) as RawKeyword; // 后端处理后返回的是关键词，才能实现点击后出现关键词的功能
  let keyword: Keyword[] = [];
  let key, value: RawKeywordValue;
  for ([key, value] of Object.entries(rawKeyword)) {
    const topic = Object.keys(value)[0];
    let month: number = Number(key); // key是字符串，要转换成数字
    if (topic) {
      keyword.push({
        month: month,
        word: value[topic][0],
      });
    }
  }
  addKeyword(keyword);
}

function addKeyword(keyword: Keyword[]) {
  svg.selectAll(".keyword").remove();
  let kwSiftedByTime = keyword.filter((item: Keyword) => {
    return popTextPos.value[item.month] !== undefined;
  }); // 把没有位置的关键词去掉
  const kw = svg
    .selectAll(".keyword")
    .data(kwSiftedByTime)
    .enter()
    .append("g")
    .attr("class", "keyword");
  let text = kw
    .append("text")
    .attr("x", function (d) {
      return popTextPos.value[d.month].x + River.xOffSet;
    })
    .attr("y", function (d) {
      return popTextPos.value[d.month].y + River.yOffSet;
    })
    .text(function (d) {
      return d.word;
    })
    .style("fill", "white")
    .style("text-anchor", "middle");
  svg
    .selectAll(".keyword")
    .selectAll("text")
    .each(function (d: any) {
      let text = this as SVGTextElement;
      d.bbox = text.getBBox(); // 得到能装下text的最小矩形
    });
  kw.append("rect")
    .attr("x", function (d) {
      return d.bbox ? d.bbox.x - 3 : 0;
    })
    .attr("y", (d) => (d.bbox ? d.bbox.y - 1 : 0))
    .attr("rx", 5)
    .attr("ry", 5)
    .attr("width", (d) => (d.bbox ? d.bbox.width + 5 : 0))
    .attr("height", (d) => (d.bbox ? d.bbox.height + 1 : 0))
    .style("fill", "#717d8e")
    .style("opacity", 1);
  text.raise(); // 把text放在最上面
}

function getXDomain() {
  const parse = d3.timeParse("%Y-%b-%U");
  const startWeek = parse(mapData.value[0].date);
  const endWeek = parse(mapData.value[mapData.value.length - 1].date);
  if (!startWeek || !endWeek) {
    return [null, null];
  }
  return [startWeek, endWeek];
}

function getYDomain() {
  const yRawDomain: number[] = [];
  mapData.value.forEach((item: TopicKeys) => {
    let key: keyof TopicKeys;
    for (key in item) {
      if (key !== "date" && key !== "ids") {
        yRawDomain.push(item[key]);
      }
    }
  });
  return [d3.max(yRawDomain) || 0, d3.min(yRawDomain) || 0];
}

function TopicData() {
  dataSortByTopic.value = topics.map((key) => {
    const perTopic = {
      key: key,
      values: mapData.value.map((element: TopicKeys) => {
        const { date, ...rest } = element;
        let topicKey = key as keyof Topics;
        let ids = element.ids[topicKey];
        let num = rest[topicKey];
        const perValues = {
          date,
          number: num || 0,
          ids: ids || [],
        };
        return perValues;
      }),
    };
    return perTopic;
  });
  dataSortByTopicTotal.value = JSON.parse(
    JSON.stringify(dataSortByTopic.value)
  );
}

function dataSortByTime() {
  const timeParse = d3.timeParse("%Y-%b-%U");
  dataSortByTopic.value = dataSortByTopicTotal.value.map((item: FinalData) => {
    let values = item.values.filter(
      (value: { date: string; number: number; ids: string }) => {
        let date = timeParse(value.date);
        if (!date) {
          return false;
        }
        if (date >= xDomain.value[0] && date <= xDomain.value[1]) {
          return true;
        }
        return false;
      }
    );
    return {
      key: item.key,
      values: values,
    };
  });
  const idArr: string[] = [];
  dataSortByTopic.value.forEach((item: FinalData) => {
    item.values.forEach(
      (value: { date: string; number: number; ids: string }) => {
        idArr.push(...value.ids);
      }
    );
  });
  idStore.setIdArrRiver(idArr);
}

function findTime(date: Date, index: number) {
  const dataParse = d3.timeParse("%Y-%b-%U");
  let finded;
  dataSortByTopicTotal.value.find((item: FinalData) => {
    // reverse会改变原数组，用拓展运算符解决
    let data = index === 1 ? item.values : [...item.values].reverse();

    data.find((value: { date: string; number: number; ids: any }) => {
      let valueDate = dataParse(value.date);
      if (!valueDate) {
        return false;
      }
      if (index === 1) {
        if (valueDate >= date) {
          finded = valueDate;
          return true;
        }
        return false;
      } else {
        if (valueDate <= date) {
          finded = valueDate;
          return true;
        }
        return false;
      }
    });
  });
  return finded;
}

function setTimeLine() {
  xDomain.value = getXDomain() as Date[];
  xDomainTotal.value = getXDomain() as Date[];
  xDomain.value = [new Date(xDomain.value[0]), new Date(xDomain.value[1])];
  if (!xDomain.value[0] || !xDomain.value[1]) {
    return;
  }
  const year: string = xDomain.value[1]?.getFullYear().toString();
  const formatTime = d3.timeFormat("%b-%U");
  const formatTick = (domainValue: any) => formatTime(domainValue);
  let selectedNum = 0;
  let selectedDate: Date[] = [];
  let x = d3.scaleTime().domain(xDomain.value).range(TimeLine.range);
  svg
    .append("g")
    .attr(
      "transform",
      "translate(" + TimeLine.xOffSet + "," + TimeLine.timeYOffSet + ")"
    )
    .attr("class", "pointer")
    .style("font", TimeLine.timeFont)
    .call(
      d3.axisBottom(x).ticks(d3.timeMonth).tickFormat(formatTick).tickSize(0)
    )
    .call((g: any) => g.select(".domain").remove())
    .on("click", (param) => {
      svg.select(".keyword").remove();
      if (selectedNum >= 2) {
        svg.selectAll("text[fill='#17a2b88f']").attr("fill", "black");
        selectedNum = 0;
        selectedDate = [];
        xDomain.value = xDomainTotal.value;
      }
      d3.select(param.target).attr("fill", "#17a2b88f");
      selectedNum++;
      if (selectedNum === 1) {
        let time = findTime(param.target.__data__, 1);
        time && selectedDate.push(time);
        xDomain.value = [selectedDate[0], xDomain.value[1]];
      }
      if (selectedNum === 2) {
        let time = findTime(param.target.__data__, 2);
        time && selectedDate.push(time);
        if (selectedDate[0] > selectedDate[1]) {
          selectedDate.reverse();
        }
        xDomain.value = selectedDate;
      }
      dataSortByTime();
      drawMain();
    });
  svg
    .append("line")
    .attr("x1", TimeLine.range[0])
    .attr("y1", 0)
    .attr("x2", TimeLine.range[1])
    .attr("y2", 0)
    .attr("stroke", TimeLine.lineColor)
    .attr("opacity", TimeLine.lineOpacity)
    .attr("stroke-width", TimeLine.timeStrokeWidth);
  svg
    .append("text")
    .attr("x", TimeLine.textXOffSet)
    .attr("y", TimeLine.textYOffSet)
    .style("text-anchor", "start")
    .attr("font-size", TimeLine.textFont)
    .attr("font-weight", TimeLine.textWeight)
    .text(year);
}

function drawThemeRiver() {
  setTimeLine();
  setLegend(); // 添加图例
  drawMain();
}
let xAxis: any, yAxis: any, river: any;
function drawMain() {
  xAxis && xAxis.remove();
  yAxis && yAxis.remove();
  river && river.remove();
  const yDomain = getYDomain();
  const formatTime = d3.timeFormat("%b-%U");
  const formatTick = (domainValue: any) => formatTime(domainValue);
  x = d3.scaleTime().domain(xDomain.value).range(River.xRange);
  xAxis = svg
    .append("g")
    .attr(
      "transform",
      "translate(" +
        River.xOffSet +
        "," +
        (River.yOffSet + River.yRange[1]) +
        ")"
    )
    // 要打括号，否则就是字符串相加而不是数字相加
    .call(
      d3
        .axisBottom(x)
        .ticks(d3.timeMonth) // 计算有几个月，设置刻度数量
        .tickFormat(formatTick)
        .tickSize(0)
    ); // tickSize(0)表示刻度的长度为0
  y = d3.scaleLinear().domain(yDomain).rangeRound(River.yRange);
  yAxis = svg
    .append("g")
    .attr("transform", "translate(" + River.xOffSet + "," + River.yOffSet + ")")
    .call(d3.axisLeft(y).tickSize(-River.xRange[1]).ticks(10))
    .call((g: any) => g.select(".domain").remove()); // 删除y轴的竖线
  svg.selectAll(".tick line").attr("opacity", River.tickOpacity); // 设置刻度线的颜色
  // 画曲线
  const parse = d3.timeParse("%Y-%b-%U");
  river = svg
    .append("g")
    .attr("transform", "translate(" + River.xOffSet + "," + River.yOffSet + ")")
    .selectAll(".line")
    .data(dataSortByTopic.value)
    .enter()
    .append("path")
    .attr("stroke", function (d: any): string {
      let topic = topicColour.find((item: Topic) => item.topic === d.key);
      if (topic === undefined) {
        return "black";
      }
      let colour: string = topic?.colour;
      return colour;
    })
    .attr("stroke-width", River.lineStrokeWidth)
    .attr("fill", "none")
    .attr("d", function (d: any) {
      return d3
        .line<{ date: string; number: number }>()
        .curve(d3.curveMonotoneX)
        .x(function (d: { date: string; number: number }) {
          if (d.date !== null) {
            return x(parse(d.date) as Date);
          }
          return 0;
        })
        .y(function (d: { date: string; number: number }) {
          return y(d.number);
        })(d.values);
    });
}
</script>

<style scoped lang="scss">
.all {
  height: 54%;
  width: 100%;
  padding: 15px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  > .title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
  }

  #river {
    width: 100%;
    flex-grow: 1; // 填充剩余空间
  }
}

:deep(.legend) {
  stroke-width: 1;
  stroke: black;
  stroke-opacity: 0;
  cursor: pointer;
  &:hover {
    stroke-opacity: 0.7;
    stroke-width: 2;
  }
}

:deep(.pointer) {
  cursor: pointer;
}
</style>
