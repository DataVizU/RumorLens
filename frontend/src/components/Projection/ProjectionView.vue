<template>
  <div class="all">
    <div class="title">Features Projection View</div>
    <div class="main">
      <div class="left">
        <div class="introduce">
          <Legend />
        </div>
        <div class="thumb">
          <Thumb :data="rawData" />
        </div>
      </div>
      <div class="right">
        <MainProjection :data="rawData" />
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import Legend from "@/components/Projection/LegendView.vue";
import Thumb from "@/components/Projection/ThumbView.vue";
import MainProjection from "@/components/Projection/MainProjection.vue";
import { contentId } from "@/utils/contentId";
import { getMiddleData } from "@/api/api";
import { storeToRefs } from "pinia";
import { onMounted, ref, watch } from "vue";
import { useIdStore } from "@/stores/id";
import type { Data } from "@/types/Projection/data";
const idStore = useIdStore();
const { idArrRiver } = storeToRefs(idStore);

const rawData = ref<Data[] | undefined>();
async function getData() {
  rawData.value = (await getMiddleData(contentId)) as Data[];
}
watch(idArrRiver, async () => {
  try {
    rawData.value = (await getMiddleData(
      idArrRiver.value as string[]
    )) as Data[];
  } catch (e) {
    // console.log(e)
    // TypeError: Cannot read properties of undefined (reading 'data')
    // at http.js?t=1691459167302:87:30
    // 但似乎没啥影响？
  }
  if (idArrRiver.value) {
    if (idArrRiver.value.length === 1) idStore.setIdTree(idArrRiver.value[0]);
    else idStore.setIdTree(idArrRiver.value[1]);
  }
});

onMounted(async () => {
  await getData();
});
</script>

<style scoped lang="scss">
.all {
  height: 100%;
  width: 100%;
  padding: 20px;
  display: flex;
  box-sizing: border-box;
  flex-direction: column;
  .title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  > .main {
    display: flex;
    flex-grow: 1;
    > .left {
      width: 27%;
      height: 100%;
      .introduce {
        width: 176px;
        height: 170px;
        border-radius: 8px;
        border: solid 3px rgba(0, 0, 0, 0.3);
      }
      .thumb {
        width: 209px;
        margin-top: 10px;
        height: 100px;
        border-radius: 8px;
        border: solid 3px rgba(0, 0, 0, 0.3);
        padding: 5px;
        position: relative;
        box-sizing: border-box;
      }
    }
    > .right {
      width: 73%;
      height: 100%;
      overflow: hidden;
    }
  }
}
</style>
