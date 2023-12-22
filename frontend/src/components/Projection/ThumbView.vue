<template>
  <div class="title">ThumbNail View</div>
  <svg id="thumbNail"></svg>
</template>

<script setup lang="ts">
import { watch } from "vue";
import type { PropType } from "vue";
import {
  calScale,
  drawThumbNail,
  getArr,
} from "@/components/Projection/js/draw";
import * as d3 from "d3";
import type { Data } from "@/types/Projection/data";

const props = defineProps({
  data: {
    type: Array as PropType<Data[] | undefined>, // 传入的数据加上类型检查
    required: true,
    default: () => [],
  },
});

watch(props, () => {
  if (props.data === undefined) return;
  // 不能写props.data，否则无法检测到变化（或者加上deep:true也行）
  d3.select("#thumbNail").selectAll("*").remove();
  getArr(props.data); // 获取比例尺的domain数组
  calScale(); // 计算比例尺
  drawThumbNail(props.data); // 绘制缩略图
});
</script>

<style scoped lang="scss">
#thumb {
  width: 100%;
  height: 100%;
}
.title {
  font-size: 12px;
  position: absolute;
  bottom: 0px;
}
</style>
