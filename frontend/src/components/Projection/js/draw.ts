import * as d3 from "d3";
import {
  HEIGHT,
  RADIUSRANGE,
  RADIUSWIDTH,
  WIDTH,
} from "@/components/Projection/js/public_def";
import { colours, topicsChinese } from "@/utils/topics";
import type { Data, User } from "@/types/Projection/data";
import { useIdStore } from "@/stores/id";

const xArr: number[] = [];
const yArr: number[] = [];
const influenceArr: number[] = [];
const fanArr: number[] = [];
const followArr: number[] = [];
const tweetsArr: number[] = [];
const xScale = d3.scaleLinear();
const yScale = d3.scaleLinear();
const sizeScale = d3.scaleSqrt(); // circle size
const colorScale = d3.scaleOrdinal();
const fansScale = d3.scaleLinear();
const followsScale = d3.scaleLinear();
const tweetsScale = d3.scaleLinear();
let projection: d3.Selection<
  SVGGElement,
  unknown,
  HTMLElement,
  undefined
> | null = null;

export function getArr(rawData: Data[]) {
  rawData.forEach((data: Data) => {
    xArr.push(Math.round(+data.coordinate[0]));
    yArr.push(Math.round(+data.coordinate[1]));
    influenceArr.push(data.influence);
    fanArr.push(data.user.fans_num);
    followArr.push(data.user.follows_num);
    tweetsArr.push(data.user.tweets_num);
  });
}

export function calScale() {
  xScale.domain(d3.extent(xArr) as number[]).range([20, WIDTH]);
  yScale.domain(d3.extent(yArr) as number[]).range([20, HEIGHT]);
  sizeScale.domain([0, d3.max(influenceArr) as number]).range(RADIUSRANGE);
  colorScale.domain(topicsChinese).range(colours);
  fansScale.domain(d3.extent(fanArr) as number[]).range([0, 2]);
  followsScale.domain(d3.extent(followArr) as number[]).range([0, 2]);
  tweetsScale.domain(d3.extent(tweetsArr) as number[]).range([0, 2]);
}

export function drawThumbNail(rawData: Data[]) {
  const svg = d3.select("#thumbNail");
  svg
    .selectAll("circle")
    .data(rawData)
    .enter()
    .append("circle")
    .attr("cx", function (d: Data) {
      return xScale(d.coordinate[0]);
    })
    .attr("cy", function (d: Data) {
      return yScale(d.coordinate[1]);
    })
    .attr("r", function (d: Data) {
      if (sizeScale(d.influence) < 0) return 0;
      return sizeScale(d.influence);
    })
    .attr("fill", function (d: Data) {
      return colorScale(d.topic.topic) as string;
    })
    .attr("opacity", 0.8)
    .attr("transform", "scale(0.3)");
}

export function drawProjection(rawData: Data[]) {
  projection = d3.select("#projection").append("g");
  projection
    .selectAll("circle")
    .data(rawData)
    .enter()
    .append("circle")
    .attr("id", (d: Data) => d.content_id)
    .attr("cx", function (d: Data) {
      return xScale(d.coordinate[0]);
    })
    .attr("cy", function (d: Data) {
      return yScale(d.coordinate[1]);
    })
    .attr("r", function (d: Data) {
      if (sizeScale(d.influence) < 0) return 0;
      return sizeScale(d.influence);
    })
    .attr("fill", function (d: Data) {
      return colorScale(d.topic.topic) as string;
    })
    .attr("opacity", 0.8)
    .on("mouseover", function () {
      d3.select(this).raise().attr("opacity", 2);
      d3.select(".dot" + this.id).raise();
      d3.selectAll(".arc" + this.id).raise();
    })
    .on("mouseout", function () {
      d3.select(this).lower().attr("opacity", 0.8);
      d3.select(".dot" + this.id).lower();
      d3.selectAll(".arc" + this.id).lower();
    })
    .on("click", function (d, i: Data) {
      const idStore = useIdStore();
      idStore.setIdTree(i.content_id);
    });
  // 画锚点
  projection
    .selectAll("dot")
    .data(rawData)
    .enter()
    .append("circle")
    .attr("class", (d: Data) => "dot" + d.content_id)
    .attr("cx", function (d: Data) {
      return xScale(d.coordinate[0]);
    })
    .attr("cy", function (d: Data) {
      return yScale(d.coordinate[1]) - 0.5 * sizeScale(d.influence);
    })
    .attr("r", (d: Data) => {
      if (d.pics) return 1.5;
      else return 0;
    })
    .attr("fill", "black");
  drawArc("#575757", rawData, 0);
  drawArc("#808080", rawData, RADIUSWIDTH);
  drawArc("#bdbdbd", rawData, 2 * RADIUSWIDTH);
  drawArc("rgba(203,203,203,0.62)", rawData, 3 * RADIUSWIDTH);
  // 缩放功能
  d3.select("#projection").call(
    d3
      .zoom()
      .extent([
        [0, 0],
        [WIDTH, HEIGHT],
      ])
      .scaleExtent([1, 8])
      .on("zoom", zoomed) as any
  );
  function zoomed({ transform }: { transform: any }) {
    projection?.attr("transform", transform);
  }
}
function getIntegrity(user: User) {
  const nonNaN = Object.values(user).filter((value) => value !== "nan").length;
  const sum = Object.keys(user).length;
  return nonNaN / sum;
}

function drawArc(color: string, rawData: Data[], startR: number) {
  const arcClass = "arc" + startR;
  projection
    ?.selectAll(`.${arcClass}`)
    .data(rawData)
    .enter()
    .append("path")
    .attr("d", function (d: Data) {
      let endAngle: number = 0;
      switch (startR) {
        case 0:
          endAngle = getIntegrity(d.user) * Math.PI;
          break;
        case RADIUSWIDTH:
          endAngle = fansScale(d.user.fans_num) * Math.PI;
          break;
        case 2 * RADIUSWIDTH:
          endAngle = followsScale(d.user.follows_num) * Math.PI;
          break;
        case 3 * RADIUSWIDTH:
          endAngle = tweetsScale(d.user.tweets_num) * Math.PI;
          break;
      }
      const arcGenerator = d3
        .arc()
        .innerRadius(sizeScale(d.influence) + startR)
        .outerRadius(sizeScale(d.influence) + startR + RADIUSWIDTH)
        .startAngle(0)
        .endAngle(endAngle);
      return arcGenerator(d as any);
    })
    .attr("fill", color)
    .attr("stroke-width", "1")
    .attr("class", function (d: Data) {
      return "arc" + d.content_id;
    })
    .on("mouseover", function () {
      const id = this.className.baseVal.slice(3);
      d3.selectAll(".arc" + id).raise();
      d3.select("#" + id)
        .raise()
        .attr("opacity", 2);
      d3.select(".dot" + id).raise();
    })
    .on("mouseout", function () {
      const id = this.className.baseVal.slice(3);
      d3.selectAll(".arc" + id).lower();
      d3.select("#" + id)
        .lower()
        .attr("opacity", 2);
      d3.select(".dot" + id).lower();
      d3.select(this).attr("opacity", 0.8);
    })
    .attr("transform", function (d: Data) {
      return (
        "translate(" +
        xScale(d.coordinate[0]) +
        "," +
        yScale(d.coordinate[1]) +
        ")"
      );
    });
}
