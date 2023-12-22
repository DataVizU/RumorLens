<template>
  <svg id="treemap" ref="treemap" @mousemove="updateTooltipPos($event)">
    // 要加$符号
    <g>
      <path
        v-for="item in listData"
        :key="`path${item.ID}`"
        :d="findD(item.ID, pathData)"
        :style="`fill:${getColor(item, father, son, selected, rightSelected)}`"
        @mouseover="showTooltip(item)"
        @mouseleave="hideTooltip()"
        @click="handleClick(item, listData)"
        @contextmenu.prevent="handleRightClick(item)"
      >
        // 处理右键点击事件，阻止浏览器默认行为
      </path>
      <text
        v-for="item in listData"
        :key="`text${item.ID}`"
        :style="getTextStyle(item, textData)"
        @contextmenu.prevent="handleRightClick(item)"
      >
        {{ getKeyword(item) }}
      </text>
    </g>
  </svg>
  <el-card
    class="tooltip"
    v-if="isShowTooltip"
    :style="{ left: `${mousePosition.x}px`, top: `${mousePosition.y}px` }"
  >
    <div>
      <div v-for="item in tooltipKeys" :key="item">
        <div
          v-if="tooltipData && tooltipData[item as keyof Tooltip] && tooltipData[item as keyof Tooltip]!==`nan`"
        >
          {{ item }}: {{ tooltipData[item as keyof Tooltip] || "no data" }}
        </div>
      </div>
    </div>
  </el-card>
</template>

<script lang="ts" setup>
import type {
  DetailData,
  ListData,
  RawData,
  TimeData,
} from "@/types/Propagation/data";
import { onMounted, ref, watch } from "vue";
import type { Path, Text } from "@/types/Propagation/path";
import {
  getFather,
  getListData,
  getPathData,
  getSon,
} from "@/components/Propagation/js/setPathData";
import { findD, getColor } from "@/components/Propagation/js/pathAttr";
import { getKeyword, getTextStyle } from "@/components/Propagation/js/textAttr";
import type { Tooltip } from "@/types/Propagation/tooltip";
import { useDetailStore } from "@/stores/detail";

const props = defineProps<{
  data: TimeData;
  sumArr: number[];
  rawData: RawData;
}>();
const listData = ref<ListData[]>([]);
const pathData = ref<Path[]>([]);
const textData = ref<Text[]>([]);
const treemap = ref<HTMLElement>();
const width = ref<number>();
const height = ref<number>();
let actualRadius: number;
const isShowTooltip = ref(false);
const tooltipData = ref<Tooltip>();
const tooltipKeys = ref<string[]>([]);
const mousePosition = ref({ x: 0, y: 0 });
const son = ref<string[]>([]);
const father = ref<string[]>([]);
const selected = ref<string>();
const rightSelected = ref<string>();
const detailStore = useDetailStore();

watch(props, () => {
  listData.value = getListData(props.rawData);
  const { path, text } = getPathData(props.data, props.sumArr, actualRadius);
  pathData.value = path;
  textData.value = text;
});

onMounted(() => {
  width.value = treemap.value?.clientWidth as number;
  height.value = treemap.value?.clientHeight as number;
  actualRadius = Math.max(width.value, height.value) / 2;
});

function updateTooltipPos(event: any) {
  const wrapper = treemap.value?.getBoundingClientRect(); // 获取svg在页面中的位置
  if (!wrapper) return;
  mousePosition.value = {
    x: event.clientX - wrapper.left, // 鼠标在svg中的位置
    y: event.clientY - wrapper.top,
  };
}

function showTooltip(data: ListData) {
  isShowTooltip.value = true;
  const { data: userData } = data;
  tooltipData.value = {
    "Create Time": userData["createTime"],
    "Fans Number": userData.user["fans_num"],
    "Followers Number": userData.user["follows_num"],
    Authenticated: userData.user["authentication"],
    "VIP Level": userData.user["vip_level"],
    "Tweets Number": userData.user["tweets_num"],
    "Province and City":
      userData.user["province"] + userData.user["city"] !== "nan"
        ? userData.user["city"]
        : "",
  };
  tooltipKeys.value = Object.keys(tooltipData.value);
}
function hideTooltip() {
  isShowTooltip.value = false;
}

function handleClick(item: ListData, data: ListData[]) {
  if (selected.value === item.ID) {
    // 点击两次相同的节点，取消选中
    selected.value = "";
    son.value = [];
    father.value = [];
  } else {
    son.value = getSon(item, data);
    father.value = getFather(item, data);
    selected.value = item.ID;
  }
}

function handleRightClick(item: ListData) {
  if (rightSelected.value === item.ID) {
    // 点击两次相同的节点，取消选中
    rightSelected.value = "";
    detailStore.setDetailData({} as DetailData);
  } else {
    rightSelected.value = item.ID;
    detailStore.setDetailData({
      "Full Content": item.data.full_content,
      "Create Time": item.data.created_at || "no data",
      userDetail: {
        id: item.data.user.id,
        Authentication: item.data.user.authentication,
        Gender: item.data.user.gender,
        "Fans Number": item.data.user.fans_num,
        "Follows Number": item.data.user.follows_num,
        "Tweets Number": item.data.user.tweets_num,
        "VIP Level": item.data.user.vip_level,
      },
    });
  }
}
</script>

<style scoped lang="scss">
#treemap {
  width: 100%;
  height: 100%;
  g {
    transform: translate(50%, 50%); // 将坐标原点移动到中心
    path {
      stroke: black;
      stroke-width: 0.4;
      stroke-opacity: 0.7;
    }
    text {
      font-size: 9px;
      alignment-baseline: middle; // 文字垂直居中
      text-anchor: middle; // 文字水平居中
      user-select: none;
    }
  }
}

.tooltip {
  position: absolute;
  z-index: 100;
  width: 260px;
}
</style>
