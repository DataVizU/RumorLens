<template>
  <div id="barchart" ref="svgObject" >
    <svg id="barchart_map"></svg>
  </div>
</template>

<script>
import * as d3 from 'd3'
import PipeService from "../../assets/js/pipe-service"
export default {
  data()
  {
    return{
      river_data:{},
      topic:['军事','历史文化','国际','娱乐','常识','情感','教育','母婴育儿','社会时事','科技'],
      newDataset:[],
      newMonDataset:[],
      topic_result:[],
      final_id:[]
    }
  },
  watch:{
    topic_result:{
      handler:function(val, oldval){
        console.log('修改后',val,'修改前',oldval);
        this.$emit("topicFeedback",val)
      },
      deep:true
    }
  },
  methods: {
    setTime2Map(response) {
      this.river_data = JSON.parse(response.data)
      //以月份为划分的数据
      this.newMonDataset = this.setMonthDataset();
      //以日期为划分的数据
      this.newDataset = this.setNewDataset(this.river_data);
      //堆叠柱状图
      this.barSvg(this.newMonDataset)

    },
    setMonthDataset() {
      const dataset = this.river_data;
      let map = {}
      for (let key in dataset){
        let singelObj = dataset[key]
        let dateYear = new Date(singelObj.date).getFullYear()
        let dateMonth = new Date(singelObj.date).getMonth()+1
        let newYM = `${dateYear.toString()}-${dateMonth.toString()}`
        if (!map[newYM]) {
            map[newYM] = [singelObj]
        } else {
            map[newYM].push(singelObj)
        }
      }
      //console.log(map)

      let res = []
      Object.keys(map).forEach(key => {
        res.push({
            date: key,
            result: this.setNewDataset(map[key]),

        })
      })
      //console.log(res)

      for (const resKey in res) {
        let month_result = res[resKey].result //arr
        let month_result_length = month_result.length
        let topic_keys = {'社会时事':0, '国际':0, '娱乐':0, '军事':0,
          '科技':0, '历史文化':0, '常识':0, '母婴育儿':0,
          '教育':0, '情感':0}
        for (let i = 0; i < month_result_length; i++) {
          let every_obj = month_result[i]
           for (const everyObjKey in every_obj) {
             if (everyObjKey != 'date' && everyObjKey != 'ids'){
               topic_keys[everyObjKey] = topic_keys[everyObjKey]+every_obj[everyObjKey]
             }
           }
        }
        for (let topicKeysKey in topic_keys) {
          res[resKey][topicKeysKey] = topic_keys[topicKeysKey]
        }
      }
      res.splice(1, 1);
      let temp = res[2];
        res[2] = res[3];
        res[3] = temp;
      //console.log(res)
      return res

    },
    barSvg(dataset){
      let series = d3.stack()
        .keys(this.topic) //set key to topics 
        (dataset).map(d => (d.forEach(v => v.key = d.key), d))
      //console.log(series)

      const width = this.$refs.svgObject.offsetWidth;
      const height = this.$refs.svgObject.offsetHeight;
      const margin = ({top: 10, right: 10, bottom: 20, left: 20})

      let x = d3.scaleBand()
              .domain(dataset.map(d => d.date))
              .range([margin.left, width - margin.right])
              .padding(0.1)

      let y = d3.scaleLinear().domain([0, d3.max(series,this.stackMax)])
              .rangeRound([height - margin.bottom, margin.top])

      let color = d3.scaleOrdinal().domain(series.map(d => d.key))
              .range(d3.schemeSpectral[series.length])
              .unknown("#ccc")

      const svg = d3.select("#barchart_map")
          .attr("width", width)
          .attr("height", height)
          .attr("viewBox", [0, 0, width, height])
          .style("padding","0.5em")
          .append("g")
          
          
      svg.selectAll("g")
        .data(series)
        .join("g")
        .attr("fill", d => color(d.key))
        .selectAll("rect")
          .data(d => d)
        .join("rect")
          .attr("x", (d) => x(d.data.date))
          .attr("y", d => y(d[1]))
          .attr("height", d => y(d[0]) - y(d[1]))
          .attr("width", x.bandwidth())
        .on("mouseover",function(d,i){
          d3.select(this)
          .style("stroke-width",3)
          .style("stroke","black")
          .style("stroke-opacity",0.7)
        })
        .on("mouseout",function(d,i){
          d3.select(this)
           .style("stroke-width",1)
           .style("stroke","black")
           .style("stroke-opacity",0.5);
          //console.log(this);
        })
        .on("click",(i,d)=>{
          
          //console.log(d.data.date)
          let final_id = []
          console.log(this.newMonDataset)
          for(let i = 0; i< this.newMonDataset.length;i++)
          {
            if(d.data.date == this.newMonDataset[i].date)
            {
              var topic = d.key;
              
              //console.log(topic)
              var keys = Object.keys(this.newMonDataset[i].result)
              //console.log(this.newMonDataset[i].result)
              this.newMonDataset[i].result.forEach(key=>{
                if(typeof key.ids[topic] != "undefined")
                {
                  for(let j = 0; j<key.ids[topic].length; j++)
                  {
                    final_id.push(key.ids[topic][j])
                  }
                }
              })
              //console.log(final_id)
              
              //this.topic_result= this.newMonDataset[i]
            }
          }
          this.topic_result = final_id;
          //topic_result = 
        })

      svg.append("g")
          .attr("transform", `translate(0,${height - margin.bottom})`)
          .call(d3.axisBottom(x).tickSizeOuter(0))
          .call(g => g.selectAll(".domain").remove())

      svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).ticks(null, "s"))
        .call(g => g.selectAll(".domain").remove())

    },
    timeSort(property, bol) { //property是你需要排序传入的key,bol为true时是升序，false为降序
	    return function(a, b) {
		    let value1 = a[property];
		    let value2 = b[property];
		    if (bol) {
			    // 升序
			    return Date.parse(value1) - Date.parse(value2);
		    } else {
			    // 降序
			    return Date.parse(value2) - Date.parse(value1)
		    }
	    }
    },
    setNewDataset(dataset){
      let newDS = [];
      for (let key in dataset) {
        let keys = {
          '社会时事':0, '国际':0, '娱乐':0, '军事':0,
          '科技':0, '历史文化':0, '常识':0, '母婴育儿':0,
          '教育':0, '情感':0, 'date':'','ids':{}
        }
        keys["date"] = dataset[key].date
        for (let i=0; i<dataset[key].topic.length; i++ ){
          let topic_name = dataset[key].topic[i].name
          keys[topic_name] = dataset[key].topic[i].num
          if (dataset[key].topic[i].id.length!=null){
            keys['ids'][topic_name] = dataset[key].topic[i].id
          }
        }
        newDS.push(keys)
      }
      //按照时间排序数组
      newDS.sort(this.timeSort("date", true))
      return newDS
    },
    stackMin(data){
      return d3.min(data,(d) => d[0])
    },
    stackMax(data){
      return d3.max(data,(d) => d[1]);
    },
  },
  mounted(){
    this.$net.sendOverviewData("time2topic",this.setTime2Map)
    // PipeService.$on("middleGetValue",(val)=>{
    //   //拿到map数据
    //   console.log(val)
    // })
  }

}


</script>

<style scoped>
svg{
  width: 100%;
  height: 100%;
}
/*#themeriver{
  background-color: cornflowerblue;
}*/
</style>
