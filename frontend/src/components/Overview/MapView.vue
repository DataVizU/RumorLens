<template>
  <div class="all">
    <div class="title">Location Distribution View</div>
    <div id="map"></div>
    <el-button
      type="info"
      id="china"
      @click="getIdArrayByLocation(location[0])"
    >
      China
    </el-button>
    <el-button
      type="info"
      id="overseas"
      @click="getIdArrayByLocation(location[1])"
    >
      Overseas</el-button
    >
  </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from "vue";
import * as echarts from "echarts";
import chinaJson from "../../utils/China.json";
import { getMapData } from "../../api/api";
import { useIdStore } from "../../stores/id";
import type { GeoJSON } from "echarts/types/src/coord/geo/geoTypes";
import { rangeColor, selectedColor } from "../../utils/mapStyle";

const idStore = useIdStore();
const newData = ref();
let chinaMap: any;
const location = ["中国", "海外"];

function getIdArrayByLocation(location: string) {
  let newArr: string[] = [];
  if (location === "海外") {
    newArr = newData.value["海外"].map((item: any) => item[1]);
  } else if (location === "中国") {
    for (const prop in newData.value) {
      if (prop !== "海外") {
        newArr = newArr.concat(
          ...newData.value[prop].map((item: any) => item[1])
        );
      }
    }
  } else if (location === "南海诸岛") {
    newArr = [];
  } else if (location !== "nan") {
    newArr = newData.value[location].map((item: any) => item[1]);
  }
  idStore.setIdArrMap(newArr);
}

async function updateMapData() {
  const newRawData = (await getMapData()) as string; // 得到的是字符串
  newData.value = JSON.parse(newRawData); // 变成json对象
  for (let i = 0; i < chinaJson.features.length; i++) {
    let location: string = chinaJson.features[i].properties.name;
    if (newData.value[location]) {
      (chinaJson.features[i].properties as any).value =
        newData.value[location].length;
    }
  }
}

onMounted(async () => {
  chinaMap = echarts.init(document.getElementById("map") as HTMLDivElement);
  await updateMapData(); // 必须加await，否则会出现异步问题，导致不能根据设置的图例显示颜色
  init();
});

function init() {
  echarts.registerMap("china", chinaJson as GeoJSON);
  const option = {
    visualMap: {
      // 左下角的图例
      min: 0,
      max: 200,
      left: "left", // 图例位置
      top: "bottom", // 图例位置
      text: ["Numbers"],
      dimension: "value", // 指定取哪个维度的数据来决定颜色
      inRange: {
        color: rangeColor,
      },
      show: true,
      itemWidth: 15, // 图例的宽度
      showLabel: true,
      pieces: [
        // 分段式的图例
        { min: 200 },
        { min: 150, max: 200 },
        { min: 100, max: 150 },
        { min: 50, max: 100 },
        { min: 0, max: 50 },
        { value: 0 },
      ],
    },
    series: [
      {
        type: "map",
        map: "china", // 和注册时的名字对应
        top: "28%",
        zoom: 1.7, // 当前视角的缩放比例
        select: {
          // 选中的区域样式
          itemStyle: {
            areaColor: selectedColor,
            label: {
              show: false,
            },
          },
        },
        emphasis: {
          // 是图形在高亮状态下的样式
          itemStyle: {
            areaColor: selectedColor,
          },
        },
        data: chinaJson.features.map((item: any) => {
          return {
            name: item.properties.name,
            value: item.properties.value,
          };
        }),
      },
    ],
  };
  chinaMap.setOption(option);
  chinaMap.on("click", (param: any) => {
    getIdArrayByLocation(param.name);
  });
}
</script>

<style scoped lang="scss">
.all {
  width: 100%;
  height: 46%;
  position: relative;
  padding: 20px;
  box-sizing: border-box;
  > .title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  #map {
    box-sizing: border-box;
    width: 100%;
    height: 91%;
  }
  #china {
    position: absolute;
    top: 47px;
    left: 24px;
    width: 100px;
  }
  #overseas {
    width: 100px;
    position: absolute;
    top: 83px;
    left: 12px;
  }
}
</style>
