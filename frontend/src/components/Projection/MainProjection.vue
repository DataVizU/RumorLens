<template>
  <svg id="projection"></svg>
</template>

<script setup lang="ts">
import { watch } from "vue";
import type { PropType } from "vue";
import { drawProjection } from "@/components/Projection/js/draw";
import * as d3 from "d3";
import type { Data } from "@/types/Projection/data";

const props = defineProps({
  data: {
    type: Array as PropType<Data[] | undefined>, // 传入的数据加上类型检查
    required: true,
    default: () => [], // 默认值,防止为undefined，导致出现warnning
  },
});

watch(props, () => {
  // 不能写props.data，否则无法检测到变化（或者加上deep:true也行）
  if (props.data === undefined) return;
  d3.select("#projection").selectAll("*").remove();
  drawProjection(props.data); // 绘制缩略图
});
</script>

<style scoped lang="scss">
#projection {
  width: 100%;
  height: 100%;
}
</style>
