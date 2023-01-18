<template>
  <div id="all-content">
    <HeaderComponent></HeaderComponent>
    <div class="main">
      <div class="main-container">
        <div class="left">
          <OverviewComponent></OverviewComponent>
          <MiddleComponent></MiddleComponent>
        </div>
        <div class="right">
          <DetailsComponent></DetailsComponent>
        </div>
      </div>
    </div>
    <FootComponent></FootComponent>
  </div>
</template>
<script>
import HeaderComponent from "./components/header.vue";
import FootComponent from "./components/footer.vue";
import OverviewComponent from "./components/Overview/overview.vue";
import MiddleComponent from "./components/Middle/middle.vue";
import DetailsComponent from "./components/Details/details.vue";

export default {
  components: {
    HeaderComponent,
    OverviewComponent,
    MiddleComponent,
    DetailsComponent,
    FootComponent,
  },
};
</script>
<style scoped>
#all-content {
  height: inherit;
}
.main {
  position: absolute;
  top: 50px;
  bottom: 30px;
  padding: 20px;
  display: inline-flex;
  background-color: #e0e4ed;
  overflow: auto;
}
.main-container {
  min-height: 970px;
  display: flex;
  flex-direction: row;
}
.left {
  width: 860px;
  height: 100%;
  display: flex;
  flex-direction: column;
  margin-right: 20px;
}

.right {
  width: 940px;
  height: 100%;
}
</style>
