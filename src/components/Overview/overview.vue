<template>
   <div id="overview">
     <!-- <div id="reset"><b-button variant="outline-primary" @click="resetAll">RESET</b-button></div> -->
     <chinamap @mapFeedback = "getMapFeedback"></chinamap>
     <!-- <barchart ></barchart> -->
     <themeriver @topicFeedback = "getTopicFeedback"></themeriver>
  </div>
</template>

<script>

import themeriver from './themeriver.vue'
import chinamap from './map.vue'
//import barchart from './barchart.vue'
import PipeService from "../../assets/js/pipe-service";
export default {
  name: "overview",
  components:{
    themeriver,
    chinamap,
    //barchart
  },
  data(){
    return {
      //以下两类是后端返回数据的初始化
      map2time:{},
      time2topic:{},
      map_feedback:[],
      topic_feedback:[],
      //最终反馈给middle_level的微博id字符串数组
      filter_result:[],
    }
  },
  watch:{
    topic_feedback:function (){
      this.setFilterResult()
    },
    map_feedback:function (){
      this.setFilterResult()
    },
    //监测已选择的微博id数组 如有变化 同步Middle_level更新
    filter_result: function (){
      console.log("数组变化")
      console.log(this.filter_result)
      PipeService.$emit('middleGetValue', this.filter_result)
    }
  },
  methods:{
    getTopicFeedback(topicVal){
      this.topic_feedback = topicVal
    },
    getMapFeedback(mapVal){
      this.map_feedback = mapVal
    },
    setMapResult(){
      let arr = []
      if (this.map_feedback.length==0){
          arr = []
      }else {
        for (let i=0; i<this.map_feedback.length; i++) {
          arr.push(this.map_feedback[i][1])
        }
      }
      return arr
    },
    setRiverResult(){
      console.log("river trigger")
      let arr = []
      if (this.topic_feedback.length==0){
          arr = []
      }else {
        for (let i=0; i<this.topic_feedback.length; i++) {
          arr.push(this.topic_feedback[i])
        }
      }
      return arr
    },
    setFilterResult(){
      const mapR = this.setMapResult();
      //console.log(mapR)
      const riverR = this.setRiverResult();
      //console.log(riverR)
      let result = []
      if (mapR.length==0 && riverR.length!=0){
        console.log("river")
        result = [].concat(riverR)
      }else if (mapR.length!=0 && riverR.length==0){
        console.log("map")
        result = [].concat(mapR)
      } else if (mapR.length!=0 && riverR.length!=0){
        console.log("river and map")
        result = [].concat(mapR.filter(v => riverR.includes(v)))
      } else {
        result = ["Ip1kHgsUa", "IpeN6vZYI", "Ipldn1hI7", "Iqb818UDx", "IqQaVEA3n", "IrLBgs95V",
        "IrM9FlPHj", "Is8mMj2Il", "IsnM6cczV", "IsnOjBOZY", "IsWGuh4Fv", "ItS3IbNvl",
        "Ivf0JfbOo", "IvgzDsaiN", "IvIVYvpRF", "IwtsWlsWE", "IwqHFikIJ", "IwQTPo5BZ",
        "IwHbMe89M", "IxOcOlwy6", "IxVw9Ajsj", "IyRDFghPf", "IyLnZlfIi", "Iz1Zpg6V6",
        "Iz46ppXQ8", "IztdxqdxP", "IzxatoAoA", "Izw3vjAp1", "Izwyoo7ls", "IzvPE0IuM",
        "IzwyxgXOk", "IzvqNB02H", "IzJYPBvoc", "IzUKnrkKC", "IzUnNoFVX", "IzOpZxQck",
        "IzP3isqjq", "IzN6piN03", "IzOBKvEsH", "IBzNol37j", "IBDaje4kL", "IBVxIbFsQ",
        "ICwmQueXg", "ICxAT5psP", "IFBdQoU6P", "J0FHjxJqh", "J1obHqN36", "J1Cgfs3XH",
        "J5b375KJz", "J5g7kyxnb", "J6zLN6spL", "J798MftA5", "JahvlhEeJ", "JbjhqrT03",
        "JcxX7kLEG", "JgsTQB6Sw", "Jg4RpryNo", "JbY6RhoaY", "Joe0Y9v9N", "Jp6Q1xugq",
        "JpjF0bnwr", "JpjFldswx", "JrDq8niAc", "Jt7ampG3G", "JtBJV1uXV", "JvbFkBgAt",
        "JuiCajqLI", "Jx41xmU0k", "Jy0dWegFZ", "Jy6rH4cRH"]
      }
      //console.log(result)
      if(result.length == 0)
      {
        result = riverR;
      }
      this.filter_result=[].concat(result);
      //将array数组转换成对象
      //let setObj = new Set(mapR)
      //循环数组array1，并将值通过add插入set对象中,此时重复数据并不会插入其中
		  //for(let i = 0; i < riverR.length; i++) {
			  //setObj.add(riverR[i]);
		  //}
		  //使用Array.from()方法将set对象转换成数组，并使用sort()方法排序
		  //this.filter_result = Array.from(setObj).sort();
		  //console.log("1111")
		  //console.log(this.filter_result)
    },
    resetAll(){
      this.map_feedback = []
      this.topic_feedback = []
    },
  },
  mounted() {
    //PipeService.$emit('middleGetValue', this.filter_result)
  }
}
</script>

<style scoped>
#overview{
  width: 100%;
  height: 65%;
  margin-bottom: 20px;
  border-radius:5px;
  background-color: white;
  display: flex;
  flex-direction: column;
}
</style>
