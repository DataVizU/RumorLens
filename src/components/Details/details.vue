<template>
  <div id="details">
    <!--    {{userId}}   :key="(new Date()).getTime()"  :key="(new Date()).getTime()+0.01" -->
    <TreeComponent :userid="userId1"></TreeComponent>
  </div>
</template>

<script>
import TreeComponent from "./tree.vue";
import PipeService from "../../assets/js/pipe-service";
export default {
  components: {
    TreeComponent,
  },
  data() {
    return {
      // userId1: "IztdxqdxP",//美国军舰
      // userId1: "IySaAwmqa", //意大利外交部长
      // userId1: "Ju8fM4ILB",//应付卫星考核
      // userId1: "IwqT2lIyz",//新冠,院士
      // userId1: "IzxNQ7rAR ",//180战地医院
      // userId1: "JbefauR1p", //耶鲁校长
      userId1: "J4Iyg1sPT", //美国警察
    };
  },
  methods: {
    // setTreeMap(res) {},
    // setTreemap(rep) {
    //   this.listResult = rep.data;
    //   if (this.listResult != null) {
    //     console.log(this.listResult);
    //   }
    // },
  },

  mounted() {
    PipeService.$on("middleByValue", (val) => {
      this.userId1 = val;
      // this.$net.sendTreeMap(this.userid, this.setTreemap);
    });
  },
};
</script>

<style scoped>
#details {
  height: 100%;
}
</style>
