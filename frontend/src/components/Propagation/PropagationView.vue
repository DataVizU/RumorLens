<template>
  <div class="all">
    <div class="title">Propagation View</div>
    <div class="main">
      <div class="left">
        <div class="histogram">
          <HistogramView :data="timeLineData" />
        </div>
        <div class="legend">
          <h5 class="title">Keyword of This Retweeting</h5>
          <button>Keyword</button>
          <div class="legend-item">
            <div class="color positive"></div>
            <div class="text">Positive</div>
          </div>
          <div class="legend-item">
            <div class="color negative"></div>
            <div class="text">Negative</div>
          </div>
          <div class="legend-item">
            <div class="color neutral"></div>
            <div class="text">Neutral</div>
          </div>
          <div class="legendText">Size:The Influence of the Origin Tweet</div>
          <div class="circle"></div>
        </div>
      </div>
      <div class="right">
        <TreeMap :rawData="rawData" :data="timeData" :sumArr="sumByLevel" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { setTreeMap } from "@/api/api";
import { onMounted, ref, watch } from "vue";
import HistogramView from "@/components/Propagation/HistogramView.vue";
import TreeMap from "@/components/Propagation/TreeMap.vue";
import type {
  LevelData,
  RawData,
  TimeData,
  RawTimeLineData,
  TimeLineData,
} from "@/types/Propagation/data";
import { useIdStore } from "@/stores/id";
import { storeToRefs } from "pinia";

const timeLineData = ref<TimeLineData>({});
const timeData = ref<TimeData>({});
const sumByLevel = ref<number[]>([]);
const idStore = useIdStore();
const { idTree } = storeToRefs(idStore);
const rawData = ref<RawData>({});

onMounted(async () => {
  const id = "J4Iyg1sPT";
  init(id);
});

watch(idTree, async () => {
  const id = idTree.value || "J4Iyg1sPT";
  init(id);
});

async function init(id: string) {
  rawData.value = (await setTreeMap(id)) as RawData;
  const levelData = setDataByLevel(rawData.value);
  timeData.value = setDataByTime(levelData);
  timeLineData.value = setTimeLineData(timeData.value);
}

function setDataByLevel(data: RawData) {
  const levelData = Object.entries(data).reduce(
    (acc: LevelData, [index, item]) => {
      if (!acc[item.level]) {
        acc[item.level] = {};
      }
      if (item.created_at) {
        const time = parseInt(item.created_at.slice(0, 10).split("-").join(""));
        item.createTime = time;
      } else item.createTime = 0;
      acc[item.level][index] = item;
      return acc;
    },
    {}
  );
  return levelData;
}

function setDataByTime(data: LevelData) {
  let resData: TimeData = {};
  Object.entries(data).forEach(([key, level]) => {
    // key是层数，level是层数对应的数据
    if (key !== "undefined") {
      sumByLevel.value[Number(key)] = 0;
      Object.entries(level).forEach(([index, item]) => {
        // index是id
        if ("son" in item) {
          // 判断son是否是item的属性
          if (!resData[`level${item.level}`]) {
            resData[`level${item.level}`] = {};
          }
          const { level: itemLevel, createTime, words_num, son } = item;
          if (!resData[`level${itemLevel}`][createTime]) {
            resData[`level${itemLevel}`][createTime] = {
              name: "root",
              children: [],
              sum: 0,
            };
          }
          const temp = {
            name: index,
            size: words_num,
            son,
            level: itemLevel,
          };
          resData[`level${itemLevel}`][createTime].sum += temp.size;
          resData[`level${itemLevel}`][createTime].children.push(temp);
          sumByLevel.value[itemLevel] += temp.size;
        }
      });
    }
  });
  return resData;
}

function setTimeLineData(data: TimeData) {
  const tmpData = Object.values(data)
    .filter((item, index) => index !== 0) // 第一层不要
    .reduce((acc: RawTimeLineData, item) => {
      Object.keys(item).forEach((createTime) => {
        if (!acc[createTime]) {
          acc[createTime] = [];
        }
        acc[createTime].push(
          ...item[createTime].children.map((child) => child.name)
        );
      });
      return acc;
    }, {});
  const firstFiveKeys = Object.keys(tmpData).slice(0, 6);
  const resData: TimeLineData = Object.fromEntries(
    firstFiveKeys.map((key, index) => [
      key === "0" ? "unknown" : "day" + index,
      tmpData[key].length,
    ])
  ); // 只要前五天的数据
  return resData;
}
</script>

<style scoped lang="scss">
.all {
  width: 100%;
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
  position: relative;
  > .title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  > .main {
    width: 100%;
    height: 100%;
    display: flex;
    > .left {
      width: 30%;
      height: 100%;
      .histogram {
        width: 100%;
        height: 50%;
        padding: 50px 0;
        box-sizing: border-box;
      }
      .legend {
        width: 100%;
        height: 50%;
        > button {
          width: 103px;
          height: 41px;
          border-radius: 3px;
          border: solid 5px rgba(205, 205, 205);
          background-color: rgba(255, 140, 135);
          margin-bottom: 20px;
        }
        .legend-item {
          width: 100%;
          display: flex;
          align-items: center;
          margin-bottom: 15px;
          > .color {
            width: 14px;
            height: 14px;
            margin-right: 10px;
          }
          > .positive {
            background-color: #b0f4a6;
          }
          > .negative {
            background-color: #ff9792;
          }
          > .neutral {
            background-color: #ffedc0;
          }
          > .text {
            font-size: 9px;
          }
        }
        .legendText {
          font-size: 9px;
          margin-bottom: 10px;
        }
        > .circle {
          width: 30px;
          height: 30px;
          border-radius: 50%;
          border: solid 1px rgba(0, 0, 0, 0.3);
          margin-bottom: 10px;
        }
      }
    }
    > .right {
      width: 70%;
    }
  }
}
</style>
