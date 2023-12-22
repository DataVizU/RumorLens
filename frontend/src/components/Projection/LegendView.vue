<template>
  <div id="legend" ref="legend"></div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import * as d3 from "d3";
import { ref } from "vue";
let svg: any;
const legend = ref();
let height: number, width: number;

onMounted(() => {
  height = legend.value.clientHeight;
  width = legend.value.clientWidth;
  svg = d3
    .select("#legend")
    .append("svg")
    .attr("width", width)
    .attr("height", height);
  init();
});

////画有缺口的圆弧
function drawArc(
  color: string,
  innerR: number,
  outerR: number,
  endAngle: number
) {
  const arc = d3
    .arc()
    .innerRadius(innerR)
    .outerRadius(outerR)
    .startAngle(0 * Math.PI)
    .endAngle(endAngle * Math.PI);

  svg
    .append("path")
    .attr("class", "arc")
    .attr("d", arc)
    .attr("fill", color)
    .attr("stroke-width", "1")
    .attr("transform", "translate(" + 60 + "," + (height * 0.645 - 30) + ")");
}

function addText(text: string, x: number, y: number) {
  svg
    .append("text")
    .attr("x", x)
    .attr("y", y)
    .attr("text-anchor", "left")
    .attr("font-size", "8pt")
    .text(text);
}

function drawCircle(r: number, color: string, x: number, y: number) {
  svg
    .append("circle")
    .attr("r", r)
    .attr("fill", color)
    .attr("stroke-width", "1")
    .attr("opacity", 0.8)
    .attr("transform", "translate(" + x + "," + y + ")");
}

function drawLine(x1: number, y1: number, x2: number, y2: number) {
  svg
    .append("line")
    .attr("x1", x1)
    .attr("y1", y1)
    .attr("x2", x2)
    .attr("y2", y2)
    .attr("stroke", "black")
    .attr("stroke-width", 1);
}

function init() {
  drawArc("#575757", 16, 21, 1.55);
  drawArc("#808080", 21, 26, 1.4);
  drawArc("#bdbdbd", 26, 31, 1.2);
  drawArc("rgba(203,203,203,0.62)", 31, 36, 1.1);
  addText("Size " + " " + " : Influence", 10, 18);
  addText("Color: Topic", 10, 33);
  addText("Integrity of ", 85, 33);
  addText(" user information", 85, 48);
  addText("Fans num", 115, 68);
  addText("Followees num", 98, 100);
  addText("Tweets num", 87, 130);
  addText("Whether there any ", 10, 145);
  addText("pictures or videos", 10, 158);
  drawCircle(16, "#b6d0fc", 60, height * 0.645 - 30);
  drawCircle(2, "black", 60, height * 0.645 - 40); //锚点
  //指向whether there any pictures or videos
  drawLine(60, height * 0.645 - 40, 60, height * 0.645 - 20);
  drawLine(60, height * 0.645 - 20, 15, height * 0.645 - 20);
  drawLine(15, height * 0.645 - 20, 15, height * 0.645 + 20);
  //指向Tweet num
  drawLine(60, height * 0.645 + 3, 60, 126);
  drawLine(60, 126, 87, 126);
  //指向Followees num
  drawLine(95, 97, 83, 97);
  //指向Fans num
  drawLine(110, 65, 80, 70);
  //指向Integrity of user information
  drawLine(70, 65, 85, 35);
  //指向Color: Topic
  drawLine(30, 35, 30, 75);
  drawLine(30, 75, 55, 75);
}
</script>
<style scoped lang="scss">
#legend {
  width: 100%;
  height: 100%;
}
</style>
