<script setup lang="ts">
import Overview from "./components/Overview/OverView.vue";
import DetailsView from "@/components/Propagation/DetailsView.vue";
import Projection from "@/components/Projection/ProjectionView.vue";
import PropagationView from "@/components/Propagation/PropagationView.vue";
</script>

<template>
  <div id="body">
    <div class="left">
      <div class="top content">
        <Overview />
      </div>
      <div class="bottom content">
        <Projection />
      </div>
    </div>
    <div class="right content">
      <div class="top">
        <PropagationView />
      </div>
      <div class="bottom">
        <DetailsView />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
#body {
  display: flex;
  flex-direction: row;
  height: 100%;
  width: 100%;
  .left {
    display: flex;
    flex-direction: column;
    width: 50%;
    height: 100%;
    margin-right: 20px;
    .top {
      width: 100%;
      height: 65%;
      margin-bottom: 20px;
    }
    .bottom {
      width: 100%;
      height: 35%;
    }
  }
  .right {
    width: 50%;
    height: 100%;
    > .top {
      height: 65%;
    }
    > .bottom {
      height: 35%;
    }
  }
}

.content {
  background-color: white;
}
</style>
