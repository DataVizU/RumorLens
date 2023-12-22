<template>
  <svg id="histogram"></svg>
</template>

<script setup lang="ts">
import * as d3 from "d3";
import { watch } from "vue";
import type { PropType } from "vue";
import type { TimeLineData } from "@/types/Propagation/data";
import { HISTOGRAM_COLOR } from "@/components/Propagation/js/public_def";

const props = defineProps({
  data: {
    type: Object as PropType<TimeLineData>,
    required: true,
  },
});

watch(
  () => props.data,
  () => {
    d3.select("#histogram").selectAll("*").remove();
    init();
  }
);

function init() {
  const svg = d3.select("#histogram");
  const xValue = Object.keys(props.data);
  const x = d3.scaleBand().domain(xValue).range([0, 230]).padding(0.5);
  const yValue = Object.values(props.data);
  const y = d3
    .scaleLinear()
    .domain([d3.max(yValue) as number, 0])
    .nice() // 使得y轴的刻度更加合理,将域四舍五入到“不错”的舍入值
    .range([30, 170]);
  svg
    .append("g")
    .attr("class", "x-axis")
    .attr("transform", "translate(30,170)")
    .call(
      d3.axisBottom(x).tickSizeOuter(0) // 去掉边上的刻度
    );
  svg
    .append("g")
    .attr("transform", "translate(30,0)")
    .call(d3.axisLeft(y).ticks(4))
    .call((g: any) => g.select(".domain").remove()) //删除y轴的横线
    .call((g: any) =>
      g
        .append("text")
        .attr("x", -30)
        .attr("y", 10)
        .attr("fill", "currentColor")
        .attr("text-anchor", "start")
        .text("Number of Tweets")
    ); //y轴标题

  svg
    .append("g")
    .selectAll("rect")
    .data(yValue)
    .join("rect")
    .attr("x", (d, i) => x(xValue[i]) as number)
    .attr("y", (d) => y(d))
    .attr("width", x.bandwidth())
    .attr("height", (d) => y(0) - y(d))
    .attr("fill", HISTOGRAM_COLOR)
    .attr("transform", "translate(30,0)");

  svg.select(".x-axis").raise();
}
</script>

<style scoped lang="scss">
#histogram {
  width: 100%;
  height: 100%;
}
</style>
