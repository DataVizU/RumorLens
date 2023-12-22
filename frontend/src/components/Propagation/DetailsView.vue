<template>
  <div class="all">
    <div class="title">Post Details View</div>
    <hr />
    <div class="main">
      <div class="left">
        <div class="time">
          <b>Create Time:</b>
          {{ detailData["Create Time"] }}
        </div>
        <div class="content">
          <b>Full Content</b>
          <br /><br />
          {{ detailData["Full Content"] }}
        </div>
      </div>
      <div class="right">
        <div v-for="item in userDetail" :key="item[0]" class="useDetail">
          <b>{{ item[0] }}: </b>
          {{ item[1] === "nan" || item[1] === "" ? "no data" : item[1] }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDetailStore } from "@/stores/detail";
import { storeToRefs } from "pinia";
import { ref, watch } from "vue";

const detailStore = useDetailStore();
const { detailData } = storeToRefs(detailStore);
const userDetail = ref<[string, string | number][]>();

watch(detailData, () => {
  if (!detailData.value.userDetail) userDetail.value = [];
  else userDetail.value = Object.entries(detailData.value.userDetail);
});
</script>

<style scoped lang="scss">
.all {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  .title {
    font-size: 20px;
    font-weight: bold;
    width: 100%;
    padding: 10px;
  }
  > hr {
    width: 100%;
    margin: 0;
  }
  > .main {
    width: 100%;
    height: 90%;
    display: flex;
    > .left {
      width: 65%;
      height: 94%;
      padding: 10px;
      border-right: rgba(0, 0, 0, 0.3) 2px solid;
      > .content {
        margin-top: 40px;
      }
    }
    > .right {
      width: 35%;
      height: 100%;
      box-sizing: border-box;
      padding: 10px;
      > .useDetail {
        margin-top: 20px;
      }
    }
  }
}
</style>
