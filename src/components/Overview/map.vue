<template>

  <div id="map" ref="svgObject">
    <svg id="china_map" >
    </svg>
      <button @click="transpass(data_class[0])" class="btn" > China </button>
      <br>
      <button @click="transpass(data_class[1])" class="btn"> Overseas </button>
  </div>
</template>

<script>
import * as d3 from 'd3'
import {map_draw_data,map_draw_data_southsea} from "../../mock";
import PipeService from "../../assets/js/pipe-service"
export default {
  data(){
    return {
      data_class:["中国", "海外"],
      map_south_sea:{},
      map_draw_data:{},
      map_final_data:[],
      map_final_south_sea:[],
      map_result:[],
    }
  },
  watch:{
    map_result:{
        handler(newVal){
          this.$emit("mapFeedback",newVal)
        },
        deep:true
    }
  },
  methods: {
    //回调函数
    setMap2Time(response) {
      this.map_data = JSON.parse(response.data)
      console.log(this.map_data)
      this.drawsvg()
    },
    //传值给themeriver
    transpass(content){
      if(content === "海外") {
        this.map_result = this.map_data["海外"]
      } else {
        this.map_result = []
        for (let province in this.map_data){
          if(province!=="海外"){
            this.map_result = this.map_result.concat(this.map_data[province])
          }
        }
      }
      console.log(this.map_result)
      let arr = []
      if (this.map_result.length==0){
          arr = []
      }else {
        for (let i=0; i<this.map_result.length; i++) {
          arr.push(this.map_result[i][1])
        }
      }
      PipeService.$emit('passmap',arr)
    },
    cleanData(){
      for (let i = 0; i < this.map_draw_data.features.length; i++) {
        let location = this.map_draw_data.features[i].properties.name
        let obj = {
          type:"Feature",
          geometry:this.map_draw_data.features[i].geometry,
          properties:this.map_draw_data.features[i].properties
        }
        for (let key in this.map_data){
          if (location.indexOf(key)!=-1){
            obj.properties.arr = this.map_data[key]
          }
        }
        this.map_final_data.push(obj)
      }
    },
    setMaxData(){
      const numArr = []
      const result = []
      for (const i in this.map_final_data) {
        numArr.push(this.map_final_data[i].properties.arr.length)
      }
      numArr.sort((a,b)=>{return a-b})
      result.push(numArr[0],numArr[33])
      return result
    },
    drawsvg(){
      this.cleanData()
      const width = this.$refs.svgObject.offsetWidth;
      const height = this.$refs.svgObject.offsetHeight;
      const svg = d3.select("#china_map").attr("width",width).attr("height",height)
        .attr("preserveAspectRatio", "xMidYMid meet")
        .attr("viewBox", [0,0,width,height])
      const min_maxData = this.setMaxData()
      const color = d3.scaleLinear().domain([0, min_maxData[1]])
            .range(['#dce7fe','#1d79ff']);

      const cover_x_trans = 120;
      const cover_y_trans = -10;
      let projection1 = d3.geoMercator()
        .center([80, 26])
        .scale(height+30)
        .translate([width/2, height/2]);
      let path1 = d3.geoPath().projection(projection1)
      let map1 = svg.append("g").attr("id","map_sea")
        .selectAll("path")
        .data(this.map_final_south_sea)
      map1.enter().append('path')
        .attr('d', path1)
        .attr('stroke', "rgba(128,126,126,0.6)")
        .attr('stroke-width', 1)
        .attr('fill',"#f2f2f2")
        .attr('transform',`translate(${cover_x_trans - 5}, ${cover_y_trans})`)



      svg.append('g').append('rect')
        .attr("class","cover")
        .attr('width',width/2)
        .attr('height',200)
        .attr('transform',`translate(${width/2.5 + cover_x_trans}, ${cover_y_trans -35})`)
        .style('fill','white')

      svg.append('g').append('rect')
        .attr("class","cover")
        .attr('width',width/4)
        .attr('height',180)
        .attr('transform',`translate(${width/2.5+21 + cover_x_trans}, ${ cover_y_trans + height/2})`)
        .style('fill','white')

      svg.append('g').append('rect')
        .attr("class","cover")
        .attr('width',width/5-45)
        .attr('height',140)
        .attr("rx",10)
        .attr('stroke', 'gray')
        .attr('stroke-width', 1)
        .attr('transform',`translate(${width/2+145 + cover_x_trans}, ${cover_y_trans + height/2+8})`)
        .style('fill-opacity','0')

      let projection = d3.geoMercator()
        .center([104, 36])
        .scale(height+30)
        .translate([width/2, height/2]);
      let path = d3.geoPath().projection(projection)
      let map = svg.append("g").attr("id","map_path")
        .selectAll("path")
        .data(this.map_final_data)


      map.enter().append('path')
        .attr('class', (d) => 'provinces ' + d.properties.name)
        .merge(map)
        .attr('d', path)
        .attr('stroke', 'white')
        .attr('stroke-width', 1)
        .attr('fill',"black")
        .attr('opacity', (d) => {
          let c = d3.scaleLinear()
                        .domain([0,211])
                        .range([0.05,1]);
          // let curData = d.properties.arr.length
          // return color(curData)
          return c(d.properties.arr.length)
        })

        .on("click",(i,d)=>{
          //console.log(d.properties.arr);
          this.map_result = d.properties.arr
          let arr = []
          if (this.map_result.length==0){
              arr = []
          }else {
            for (let i=0; i<this.map_result.length; i++) {
              arr.push(this.map_result[i][1])
            }
          }
          PipeService.$emit('passmap',arr)
        })
        .on("mouseover",function(d,i){
          d3.select(this)
          .style('fill','rgba(9,103,118,0.92)')
          .style('opacity',(d) => {
          let c = d3.scaleLinear()
                        .domain([0,211])
                        .range([0.05,1]);
          // let curData = d.properties.arr.length
          // return color(curData)
          return c(d.properties.arr.length) * 4
        })
        })
        .on("mouseout",function(i,d){
          d3.select(this)
            .style("fill","black")
            .style("opacity",(d) => {
          let c = d3.scaleLinear()
                        .domain([0,211])
                        .range([0.05,1]);
          // let curData = d.properties.arr.length
          // return color(curData)
          return c(d.properties.arr.length)
        })
      })

      let legenddata = [{"text":"200+", "colour":"#313131"},
                        {"text":"150-200", "colour":"#3d3d3d"},
                        {"text":"100-150", "colour":"#505050"},
                        {"text":"50-100", "colour":"#686868"},
                        {"text":"0-50", "colour":"#8b8b8b"},
                        {"text":"0", "colour":"#d2d2d2"}]
      let legend = svg.selectAll(".legend")
      .data(legenddata)
      .enter()
      .append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(-25," + (i*25+110) + ")"; })

      legend.append("rect")
      .attr("x",width-820)
      .attr("y",function(d,i){return i+20})
      .attr("rx",5)
      .attr("ry",5)
      .attr("width",14)
      .attr("height",14)
      .style("fill", function(d,i){
        return d.colour
      })
      legend.append("text")
      .attr("x", width-800)
      .attr("y", function(d,i){return 32+i*1})
      .style("text-anchor","start")
      .text(function(d){
        return d.text;
      })

      svg.append("text")
      .attr("x", width-845)
      .attr("y", 115)
      .style("font-size", "12pt")
      .style('font-weight', '600')
      .text("Numbers")

      svg.append("text")
      .attr("x", width-850)
      .attr("y", 35)
      .style("font-size", "16pt ")
      .style('font-weight', '800')
      .text("Location Distribution View")

      svg.append("text")
      .attr("x", width-850)
      .attr("y", height-10)
      .style("font-size", "16pt ")
      .style('font-weight', '800')
      .text("Topic Evolution View")

      svg.append("line")
      .style("stroke", "black")
      .style("stroke-width", 0.5)
      .attr("x1", 20)
      .attr("y1",height)
      .attr("x2",width-20)
      .attr("y2",height)
      svg.selectAll("text")
    }
  },
  created() {
    const {type,features} = map_draw_data;
    this.map_draw_data = {type,features}

    const {typess,featuress} =map_draw_data_southsea;
    this.map_south_sea = {typess,featuress}
    for (let i = 0; i < this.map_south_sea.featuress.length; i++) {
        let obj = {
          type:"Feature",
          geometry:this.map_south_sea.featuress[i].geometry,
          properties:this.map_south_sea.featuress[i].properties
        }
        this.map_final_south_sea.push(obj)
      }
  },
  mounted(){
    this.$net.sendOverviewData("map2time",this.setMap2Time)
  }
}
</script>

<style scoped>
#china_map {
  width: 100%;
  height: 100%;
}
/*.button{*/
/*  width: 10%;*/
/*  height: 10%;*/
/*}*/
#map {
  height: 50%;
  width: 100%
}
.btn{
  width:85px ;
  margin-top:-550px;
  margin-left:15px;
  color: #fff;
  background-color: rgba(82, 143, 198, 0.58);
  border-color: rgba(82, 143, 198, 0.58);
  text-shadow: 0 -1px 0 rgba(0,0,0,0.12);
  -webkit-box-shadow: 0 2px 0 rgba(0,0,0,0.045);
  box-shadow: 0 2px 0 rgba(0,0,0,0.045);
  height: 23px;
  position: relative;
      cursor: pointer;
  line-height: 0.499;
}

</style>
