<template>
  <div id="themeriver" ref="svgObject">
    <svg id="themeriver_map"></svg>
  </div>
</template>

<script>
import * as d3 from "d3";
import * as d3slider from "d3-simple-slider";
import PipeService from "../../assets/js/pipe-service";
import * as d3label from "d3-area-label";

export default {
  data() {
    return {
      river_data: {}, //人文，时事，母婴
      topic: [
        "军事",
        "历史文化",
        "国际",
        "娱乐",
        "常识",
        "情感",
        "教育",
        "母婴育儿",
        "社会时事",
        "科技",
      ],
      newDataset: [],
      newMonDataset: [],
      newWeekDataset: [],
      topic_result: [],
      timerange_result: [],
      map_result: [],
      region_result: [],
      timeSelection_result: [],
      final_result: [],
      timeRange: [],
      keyword: [],
      topicname: {},
      lasttopic: {},
      selector: [
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
      ],
      selectValue: [],
    };
  },
  watch: {
    final_result: {
      handler: function (val, oldval) {
        //console.log('修改后',val,'修改前',oldval);
        this.$emit("topicFeedback", val);
      },
      deep: true,
    },
    map_result: function () {
      //console.log("new map")
      //当map传值后将id转换为对应的河流图数据格式
      // this.region_result = this.idtotopic()
      // if(this.timeRange.length != 0)
      // {
      //   this.linechart(this.cut(this.region_result))
      // }else{

      //   this.linechart(this.region_result)
      // }
      this.region_result = this.idtotopic();
      this.timeSelection_result = [];
      this.timeRange = [];
      this.keyword = [];
      this.selectValue = [];
      this.$emit("topicFeedback", this.map);
      this.linechart(this.region_result);
    },
    selectValue: function () {
      if (this.selectValue) {
        let node = document.getElementById(this.selectValue[0]);
        node.style.color = "red";
      }
    },
    timeSelection_result: function () {
      this.linechart(this.timeSelection_result);
      //this.$net.sendOverviewData("time2topic",this.setTime2Map)
    },
    keyword: function () {
      //console.log(this.keyword)
      if (this.timeSelection_result.length != 0)
        this.linechart(this.timeSelection_result);
      else if (this.timeSelection_result.length != 0 && this.region_result != 0)
        this.linechart(this.cut(this.region_result));
      else if (this.timeSelection_result.length == 0 && this.region_result != 0)
        this.linechart(this.region_result);
      else this.linechart(this.newWeekDataset);
    },
  },
  methods: {
    setTime2Map(response) {
      console.log("show default river");
      this.river_data = JSON.parse(response.data);
      //以月份为划分的数据
      //this.newMonDataset = this.setMonthDataset();
      //以日期为划分的数据
      this.newDataset = this.setNewDataset(this.river_data);
      this.newWeekDataset = this.Week(this.newDataset);
      //this.riverSvg(this.newWeekDataset)//this.newMonDataset)
      this.linechart(this.newWeekDataset);
    },
    setRiverKeywords(res) {
      // console.log("河流图需要的keywords!!!")
      // console.log(res.data)
      this.keyword = res.data;
      return res.data;
      //this.linechart(this.newWeekDataset)
    },
    linechart(dataset) {
      console.log("refresh");
      this.selector = [
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
        { bool: false },
      ];
      //this.timeSelection_result
      let topic_colour = [
        { topic: "Millitary", colour: "#f45540" },
        { topic: "Culture", colour: "#ff9792" },
        { topic: "World News", colour: "#528fc6" },
        { topic: "Entertainment", colour: "#95e0f4" },
        { topic: "Common Sense", colour: "#47a875" },
        { topic: "Affection", colour: "#b0f4a6" },
        { topic: "Education", colour: "#ffedc0" },
        { topic: "Baby Care", colour: "#BE3636" },
        { topic: "Current Events", colour: "#b871c9" }, //#FAA913
        { topic: "Technology", colour: "#ddc0ff" },
      ];
      //console.log(topic_colour[0].colour)
      //画svg必要的宽度 高度信息
      const width = this.$refs.svgObject.offsetWidth;
      const height = this.$refs.svgObject.offsetHeight;
      const margin = { top: 20, right: 10, bottom: 20, left: 10 };
      var datetoweek = d3.timeParse("%Y-%b-%U");
      var date;
      //设置x轴的起始结束时间
      let startWeek;
      let endWeek;

      startWeek = datetoweek(this.newWeekDataset[0].date); //new Date(dataset[0].date)
      endWeek = datetoweek(
        this.newWeekDataset[this.newWeekDataset.length - 1].date
      ); //new Date(dataset[dataset.length-1].date)
      //console.log(startWeek,endWeek)
      let dateRange = [];
      if (this.timeRange.length != 0) {
        dateRange = [
          datetoweek(this.timeRange[0]),
          datetoweek(this.timeRange[1]),
        ];
      } else {
        dateRange = [startWeek, endWeek];
      }
      //console.log(dataset)
      //this.timeSelection_result = dataset
      let data = [];
      data = dataprocess(dataset, this.topic);
      function dataprocess(dataset, topic) {
        var datares = [];
        topic.forEach((element) => {
          var pertopic = { key: element, values: [] };

          dataset.forEach((e) => {
            var key = Object.keys(e);
            key = key.slice(2, key.length);
            let perweek = { date: e.date, result: [], number: 0 };
            perweek["number"] = e[element];
            e.result.forEach((day) => {
              if (typeof day.ids[element] != "undefined") {
                day.ids[element].forEach((id) => {
                  perweek["result"].push(id);
                });
              }
            });
            pertopic["values"].push(perweek);
          });
          datares.push(pertopic);
        });
        return datares;
      }

      var number = [];
      data.forEach((element) => {
        element.values.forEach((week) => {
          number.push(week.number);
        });
      });

      let x = d3
        .scaleTime()
        .domain(dateRange) //[startWeek,endWeek])
        .range([180, width]);
      let y = d3
        .scaleLinear()
        .domain([d3.min(number), d3.max(number)])
        .rangeRound([height - margin.bottom, margin.top + 30]);

      let canvas = d3
        .select("#themeriver_map")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .style("padding", "0.5em");
      canvas.selectAll("*").remove();
      //选择html中的svg 并增加一个group
      let svg = d3
        .select("#themeriver_map")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .style("padding", "0.5em")
        .append("g")
        .attr("width", width)
        .attr("height", height);

      //wait for futher usage
      let textposition = [];
      drawlines(data, d3.min(number), d3.max(number));

      function drawlines(data, max, min) {
        var xp = height - 15;
        svg
          .append("g")
          .style("font", "6pt")
          .attr("transform", "translate(0," + xp + ")")
          .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%b-%U")).tickSize(0))
          .call((g) => g.select(".domain").remove());

        svg
          .append("g")
          .style("font", "6pt")
          .attr("transform", "translate(180,0 )")
          .call(
            d3
              .axisLeft(y)
              .ticks(10)
              .tickSize(-width - 20)
          )
          .call((g) => g.select(".domain").remove());

        svg.selectAll("g.tick").select("line").style("opacity", 0.4);
        svg
          .append("g")
          .selectAll(".line")
          .data(data)
          .enter()
          .append("path")
          .attr("fill", "none")
          .attr("stroke", function (d, i) {
            return topic_colour[i].colour;
          })
          .attr("stroke-width", 3)
          .attr("d", function (d) {
            return d3
              .line()
              .curve(d3.curveMonotoneX)
              .x(function (d) {
                return x(datetoweek(d.date));
              })
              .y(function (d) {
                return y(+d.number);
              })(d.values);
          });
      }
      var legend = svg
        .selectAll(".legend")
        .data(data)
        .enter()
        .append("g")
        .attr("class", "legend")
        .attr("transform", function (d, i) {
          return "translate(-28," + (i * 20 + 35) + ")";
        });

      legend
        .append("rect")
        .attr("x", 20)
        .attr("y", function (d, i) {
          return 20 + i * 5;
        })
        .attr("rx", 5)
        .attr("ry", 5)
        .attr("width", 15)
        .attr("height", 15)
        .style("fill", function (d, i) {
          return topic_colour[i].colour;
        })
        .on("mouseover", function (d, i) {
          d3.select(this)
            .style("stroke-width", 2)
            .style("stroke", "black")
            .style("stroke-opacity", 0.7);
        })
        .on("mouseout", function (d, i) {
          d3.select(this)
            .style("stroke-width", 1)
            .style("stroke", "black")
            .style("stroke-opacity", 0);
        })

        .on("click", (i, d) => {
          this.topic_name = d.key;
          this.lasttopic = d.key;
          this.$emit("topicFeedback", ids(d));
          //console.log(ids(d))
          this.$net.sendRiverKeywords(ids(d), this.setRiverKeywords);
        });

      legend
        .append("text")
        .attr("x", 40)
        .attr("y", function (d, i) {
          return 33 + i * 5;
        })
        .style("text-anchor", "start")
        .style("font", "9pt")
        .text(function (d, i) {
          return topic_colour[i].topic;
        });

      // legend.selectAll('rect')
      //   .attr('opacity',1)
      //   .on("click",
      //     legend.selectAll('rect')
      //       .attr('opacity', 0.3);
      //     d3.select(this)
      //       .attr('opacity',1)
      //   )

      function ids(data) {
        let ids = [];
        //console.log(data)
        data.values.forEach((week) => {
          week.result.forEach((element) => {
            ids.push(element);
          });
        });
        return ids;
      }
      //console.log(x(datetoweek(d3.timeFormat("%Y-%b-%U")(new Date("2020-08")))))
      //console.log(datetoweek(d3.timeFormat("%Y-%b-%U")(new Date("2020-8-10"))))
      let t = d3.timeFormat("%Y-%b-%U")(new Date("2020-8-05"));
      //console.log(x(t))
      let weekno = [];
      let permonth = [];
      data.forEach((element) => {
        let topic = { key: element.key, pos: [] };
        let tp = [];
        let p = [];
        for (var i = 1; i < 13; i++) {
          var t;
          var w;
          if (i == 8) {
            t = d3.timeFormat("%Y-%b-%U")(new Date(`2020-${i}-03`));
            w = d3.timeFormat("%b-%U")(new Date(`2020-${i}-03`));
          } else if (i == 10) {
            t = d3.timeFormat("%Y-%b-%U")(new Date(`2020-${i}-07`));
            w = d3.timeFormat("%b-%U")(new Date(`2020-${i}-07`));
          } else {
            t = d3.timeFormat("%Y-%b-%U")(new Date(`2020-${i}-01`));
            w = d3.timeFormat("%b-%U")(new Date(`2020-${i}-01`));
          }
          //console.log(t)
          tp.push(w);
          p.push(t);
          let pos = {};
          pos["x"] = x(datetoweek(t));
          element.values.forEach((week) => {
            if (week.date == t) {
              //console.log(week.date,t)
              //console.log(week.number)
              pos["y"] = y(week.number);
            }
          });
          topic.pos.push(pos);
        }
        weekno = tp;
        permonth = p;
        textposition.push(topic);
      });

      svg.selectAll(".axis").remove();

      var pointdata = [];
      data.forEach((element) => {
        element.values.forEach((e) => {
          let pos = {};
          pos["x"] = x(datetoweek(e.date));
          pos["y"] = y(e.number);
          pointdata.push(pos);
        });
      });
      var test = [];
      textposition.forEach((element) => {
        element.pos.forEach((p) => {
          let pos = {};
          pos["x"] = p.x;
          pos["y"] = p.y;
          test.push(pos);
        });
      });
      // console.log(test)

      //this.$net.sendRiverKeywords(this.getid(this.newWeekDataset),this.setRiverKeywords)
      if (this.keyword.length != 0) {
        let word = this.keyword;
        let month = Object.keys(word);
        console.log(month);
        let kw = [];
        month.forEach((d, i) => {
          var topic = this.topic_name;
          if (typeof word[d][topic] != "undefined") {
            let w = {};
            w["word"] = word[d][topic][0];
            w["month"] = d;
            console.log(word[d][topic][0], d);
            kw.push(w);
          }
        });

        let tpos;
        textposition.forEach((element) => {
          if (element.key == this.topic_name) {
            tpos = element;
          }
        });
        //console.log(this.lasttopic, this.topic_name)
        console.log(kw);
        var keyword = svg
          .selectAll(".keyword")
          .data(kw)
          .enter()
          .append("g")
          .attr("class", "keyword");

        keyword
          .append("text")
          .attr("x", function (d, i) {
            return tpos.pos[d.month - 1].x;
          })
          .attr("y", function (d, i) {
            return tpos.pos[d.month - 1].y - 80;
          })
          .text(function (d, i) {
            return d.word;
          })
          .style("fill", "#717d8e")
          .style("text-anchor", "middle");

        svg
          .selectAll(".keyword")
          .selectAll("text")
          .each(function (d) {
            d.bbox = this.getBBox();
          });
        keyword.selectAll("text").remove();
        //svg.data(kw)
        keyword
          .append("rect")
          .attr("x", function (d, i) {
            console.log(d);
            return d.bbox.x - 3;
          })
          .attr("y", (d) => d.bbox.y)
          .attr("rx", 5)
          .attr("ry", 5)
          .attr("width", (d) => d.bbox.width + 5)
          .attr("height", (d) => d.bbox.height + 1)
          .style("fill", "#717d8e")
          .style("opacity", 1);

        // keyword.append("path")
        // .attr()

        keyword
          .append("text")
          .attr("x", function (d, i) {
            return tpos.pos[d.month - 1].x;
          })
          .attr("y", function (d, i) {
            return tpos.pos[d.month - 1].y - 80;
          })
          .text(function (d, i) {
            return d.word;
          })
          .style("fill", "white")
          .style("text-anchor", "middle");
      }
      svg
        .append("line")
        .style("stroke", "black")
        .style("stroke-width", 0.5)
        .attr("x1", 145)
        .attr("y1", 40)
        .attr("x2", 145)
        .attr("y2", height - 20);

      svg.selectAll("text");

      var selector = svg
        .selectAll(".selector")
        .data(weekno)
        .enter()
        .append("g")
        .attr("class", "selector")
        .attr("transform", function (d, i) {
          return "translate(" + i * 73 + "," + 20 + ")";
        });
      selector
        .append("rect")
        .attr("id", function (d, i) {
          return `2020-${weekno[i]}`;
        })
        .attr("width", 60)
        .attr("height", 20)
        .attr("rx", 5)
        .attr("ry", 5)
        .style("fill", (d) => {
          if (this.selectValue.length >= 1) {
            const dName = d;
            for (let i = 0; i < this.selectValue.length; i++) {
              const dValue = this.selectValue[i].toString().slice(5);
              if (dValue === dName) {
                return "#1d79ff";
              }
            }
          }
          return "white";
        });

      let selector1 = this.selector;

      selector
        .append("text")
        .attr("y", 15)
        .attr("dx", ".35em")
        .style("font", "9pt")
        .text(function (d, i) {
          return weekno[i];
        });
      console.log(permonth);
      selector
        // .on("mouseover",function(d,i){
        //   d3.select(this).select("rect")
        //   .style("fill", "#1d79ff")
        // })
        .on("click.rect", function () {
          d3.select(this).select("rect").style("fill", "#17a2b88f");
        })
        .on("click", (d, i) => {
          //console.log(this.selectValue)
          let number = d3.timeFormat("%m")(new Date(i));
          console.log(i, number);
          console.log(permonth[number - 1]);
          let c = 0;
          selector1.forEach((e) => {
            if (e.bool) {
              c++;
            }
          });
          if (!this.selector[number - 1].bool && c < 2) {
            this.selector[number - 1].bool = true;

            this.selectValue = [];
            this.selector.forEach((d, i) => {
              if (d.bool) {
                this.selectValue.push(permonth[i]);
              }
            });
            console.log(this.selectValue);
            if (this.selectValue.length == 2) {
              let temp = this.selectValue;
              let time1 = temp[0]; //this.selectorValue[1]//d3.timeFormat("%Y-%b-%U")(datetoweek(this.selectValue[0]))
              let time2 = temp[1]; //this.selectorValue[1]//d3.timeFormat("%Y-%b-%U")(datetoweek(this.selectValue[1]))
              console.log(time1, time2);
              let sIndex = 0;
              let eIndex = this.newWeekDataset.length;
              this.newWeekDataset.forEach(function (d, i) {
                console.log(d.date);
                if (d.date == time1) {
                  sIndex = i;
                }
                if (d.date == time2) {
                  eIndex = i;
                }
              });
              console.log(sIndex, eIndex);
              this.timeRange = [];
              this.timeRange.push(time1);
              this.timeRange.push(time2);
              let timeselect = [];
              if (this.region_result.length != 0) {
                timeselect = this.region_result.slice(sIndex, eIndex);
              } else {
                timeselect = this.newWeekDataset.slice(sIndex, eIndex);
              }
              this.timeSelection_result = timeselect;
            } else {
              return;
            }
          }

          // if(this.selector[number-1].bool) {
          //   this.selector[number-1].bool = false
          // }
        });
      // .on("mouseout",function(d,i){
      //   var number = d3.timeFormat("%m")(new Date(i))
      //   //console.log(se[0].bool)
      //   if(!selector1[number-1].bool) {
      //     d3.select(this).select("rect")
      //     .style("fill", "white")
      //   }
      // })
      this.selector = selector1;

      svg
        .append("text")
        .attr("x", width - 855)
        .attr("y", 15)
        .style("font-size", "11pt ")
        .style("font-weight", "800")
        .text("2020");

      //定义鼠标样式
      svg.selectAll(".selector").attr("cursor", "pointer");
      const legend_rect = svg.selectAll(".legend");
      legend_rect.selectAll("rect").attr("cursor", "pointer");
    },
    cut(map) {
      var sindex = 0;
      var eindex = 0;
      map.forEach((d, i) => {
        if (d.date == this.timeRange[0]) {
          sindex = i;
        }
        if (d.date == this.timeRange[1]) {
          eindex = i;
        }
      });
      return map.slice(sindex, eindex);
    },

    riverSvg(dataset) {
      //console.log("draw river")

      let topic_colour = [
        { topic: "军事", colour: "#FED85C" },
        { topic: "人文", colour: "#88ADA6" },
        { topic: "国际", colour: "#FB964C" },
        { topic: "娱乐", colour: "#EB5051" },
        { topic: "常识", colour: "#40FFEC" },
        { topic: "情感", colour: "#F54889" },
        { topic: "教育", colour: "#7B2929" },
        { topic: "母婴", colour: "#80D1FF" },
        { topic: "时事", colour: "#A06AE9" },
        { topic: "科技", colour: "#9AF984" },
      ];

      //河流图数据处理 生成层叠部分
      let stack = d3.stack().keys(this.topic).order(d3.stackOrderDescending);
      //.offset(d3.stackOffsetSilhouette)

      let series = stack(dataset);
      //stack.data(series)
      //画svg必要的宽度 高度信息
      const width = this.$refs.svgObject.offsetWidth;
      const height = this.$refs.svgObject.offsetHeight;
      const margin = { top: 20, right: 10, bottom: 10, left: 10 };
      var datetoweek = d3.timeParse("%Y-%b-%U");

      //设置x轴的起始结束时间
      let startWeek;
      let endWeek;

      startWeek = datetoweek(this.newWeekDataset[0].date); //new Date(dataset[0].date)
      endWeek = datetoweek(
        this.newWeekDataset[this.newWeekDataset.length - 1].date
      ); //new Date(dataset[dataset.length-1].date)
      //console.log(startMon,endMon)
      let dateRange = [];
      if (this.timeRange.length != 0) {
        dateRange = [
          datetoweek(this.timeRange[0]),
          datetoweek(this.timeRange[1]),
        ];
      } else {
        dateRange = [startWeek, endWeek];
      }
      let x = d3
        .scaleTime()
        .domain(dateRange) //[startWeek,endWeek])
        .range([0, width]);

      //y轴scale
      let y = d3
        .scaleLinear()
        .domain([d3.min(series, this.stackMin), d3.max(series, this.stackMax)])
        .rangeRound([height - margin.bottom, margin.top]);

      //区域
      let area = d3
        .area()
        .x((d) => x(datetoweek(d.data.date)))
        .y0((d) => y(d[0]))
        .y1((d) => y(d[1]))
        .curve(d3.curveNatural);
      //.attr('transform','translate(0,0)')
      let canvas = d3
        .select("#themeriver_map")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .style("padding", "0.5em");
      canvas.selectAll("*").remove();
      //选择html中的svg 并增加一个group
      let svg = d3
        .select("#themeriver_map")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .style("padding", "0.5em")
        .append("g");
      //boxes
      //let topics = Object.keys(topic_keys);
      svg
        .selectAll("g")
        .data(topic_colour)
        .join("g")
        .append("rect")
        .attr("x", -20)
        .attr("y", function (d, i) {
          return i * 20 + 50;
        })
        .attr("width", 30)
        .attr("height", 15)
        .attr("fill", function (d) {
          return d.colour;
        })
        .data(series)
        .on("mouseover", function (d, i) {
          d3.select(this)
            .style("stroke-width", 2)
            .style("stroke", "black")
            .style("stroke-opacity", 0.7);
        })
        .on("mouseout", function (d, i) {
          d3.select(this)
            .style("stroke-width", 1)
            .style("stroke", "black")
            .style("stroke-opacity", 0);
        })
        .on("click", (i, d) => {
          let result = themeClick(d);
          this.topic_result = result;
          console.log(result);
          this.getResult();
        });

      //text
      // svg.selectAll("g")
      //   .data(topic_colour)
      //   .join("g")
      //   .append("text")
      //   .attr("x",50)
      //   .attr("y",function(d,i){
      //     return i*20+62
      //   })
      //   .style("text-anchor","end")
      //   //.attr("dy",".30em")
      //   .text(function(d){
      //     return d.topic
      //   })

      //点击主题监听事件函数 生成函数
      //eg: return ["IoSGc3Klt", "Iw6UAqbnZ", "IB2sYljXF", "IC72WzbH3", "J4Iyg1sPT", "J67Q22COi", "J6MXazRmW", "Jf6OxrsAl", "JkqeegAow", "JlXMCk3LG"]
      let themeClick = function (dataset) {
        let key = dataset.key;
        let topicIds = [];

        for (let i = 0; i < dataset.length; i++) {
          if (dataset[i].data[key] != 0) {
            let monthArr = dataset[i].data.result;
            for (let j = 0; j < monthArr.length; j++) {
              if (monthArr[j].ids[key]) {
                topicIds = topicIds.concat(monthArr[j].ids[key]);
              }
            }
          }
        }
        return topicIds;
      };

      let stream = svg
        .append("g")
        .attr("id", "areas")
        .selectAll("path")
        .data(series);

      //stream.enter().append("text").attr("dy",5).text(function(d,i){return d.key})
      console.log(series);
      //var areaLabel = d3.areaLabel().area(area).padding(.5);
      stream
        .enter()
        .append("path") //.attr("id",function(d){return "path"+d.index})
        .attr("class", "stream")
        .merge(stream)
        .attr("d", area)
        .attr("transform", "translate(50,0)")
        .data(topic_colour)
        .attr("fill", (d, i) => {
          return d.colour;
        });

      const slider = d3slider
        .sliderBottom(x)
        .min(startWeek)
        .max(endWeek)
        .default(dateRange)
        .tickFormat(d3.timeFormat("%Y-%b-%U"))
        .on("end", (val) => {
          let time1 = d3.timeFormat("%Y-%b-%U")(val[0]);
          let time2 = d3.timeFormat("%Y-%b-%U")(val[1]);

          var sIndex = 0;
          var eIndex = this.newWeekDataset.length;
          this.newWeekDataset.forEach(function (d, i) {
            if (d.date == time1) {
              sIndex = i;
            }
            if (d.date == time2) {
              eIndex = i;
            }
          });
          console.log(time1, time2);
          this.timeRange = [];
          this.timeRange.push(time1);
          this.timeRange.push(time2);
          let res = [];
          let timeselect = [];
          if (this.region_result.length != 0) {
            timeselect = this.region_result.slice(sIndex, eIndex);
          } else {
            timeselect = this.newWeekDataset.slice(sIndex, eIndex);
          }
          this.timeSelection_result = timeselect;

          timeselect.forEach((element) => {
            element.result.forEach((e) => {
              Object.keys(e.ids).forEach((key) => {
                e.ids[key].forEach((id) => {
                  res.push(id);
                  //console.log(id)
                });
              });
            });
          });
          //console.log(res)

          this.timerange_result = res;
          this.getResult();
        });
      svg.call(slider);
      const labels = svg.selectAll("text").data(series);
      labels
        .enter()
        .append("text")
        .attr("class", "area-label")
        .merge(labels)
        .text((d) => d.key)
        .style("fill", "black")
        .attr("transform", d3label.areaLabel(area));
    },
    getid(dataset) {
      let res = [];
      dataset.forEach((element) => {
        element.result.forEach((e) => {
          Object.keys(e.ids).forEach((key) => {
            e.ids[key].forEach((id) => {
              res.push(id);
              //console.log(id)
            });
          });
        });
      });
      return res;
    },
    getResult() {
      if (this.topic_result.length != 0 && this.timerange_result.length != 0) {
        console.log("has topic");
        let final_id = this.topic_result.concat(this.timerange_result);
        if (final_id.length != 0) {
          console.log(final_id);
          this.final_result = final_id;
        }
      } else if (
        this.topic_result.length != 0 &&
        this.timerange_result.length == 0
      ) {
        this.final_result = this.topic_result;
      } else if (
        this.topic_result.length == 0 &&
        this.timerange_result.length != 0
      ) {
        this.final_result = this.timerange_result;
      }
    },
    timeSort(property, bol) {
      //property是你需要排序传入的key,bol为true时是升序，false为降序
      return function (a, b) {
        let value1 = a[property];
        let value2 = b[property];
        if (bol) {
          // 升序
          return Date.parse(value1) - Date.parse(value2);
        } else {
          // 降序
          return Date.parse(value2) - Date.parse(value1);
        }
      };
    },
    setNewDataset(dataset) {
      let newDS = [];
      for (let key in dataset) {
        let keys = {
          社会时事: 0,
          国际: 0,
          娱乐: 0,
          军事: 0,
          科技: 0,
          历史文化: 0,
          常识: 0,
          母婴育儿: 0,
          教育: 0,
          情感: 0,
          date: "",
          ids: {},
        };
        keys["date"] = dataset[key].date;
        for (let i = 0; i < dataset[key].topic.length; i++) {
          let topic_name = dataset[key].topic[i].name;
          keys[topic_name] = dataset[key].topic[i].num;
          if (dataset[key].topic[i].id.length != null) {
            keys["ids"][topic_name] = dataset[key].topic[i].id;
          }
        }
        newDS.push(keys);
      }
      //按照时间排序数组
      newDS.sort(this.timeSort("date", true));
      return newDS;
    },
    //Week
    Week(dataset) {
      //console.log(dataset)
      let weibo = dataset; //this.newDataset;
      let map = {};
      var datetoweek = d3.timeFormat("%Y-%b-%U");
      weibo.forEach((element) => {
        //console.log(element.date)
        var weekNo = datetoweek(new Date(element.date));
        //console.log(element)
        if (!map[weekNo]) {
          map[weekNo] = [element];
        } else {
          map[weekNo].push(element);
        }
      });

      let temp = map;

      let res = [];
      var length = Object.keys(map).length;
      var keys = Object.keys(map);
      Object.keys(map).forEach((key) => {
        res.push({
          date: key,
          result: temp[key],
        });
      });

      for (const resKey in res) {
        let month_result = res[resKey].result; //arr
        let month_result_length = month_result.length;
        let topic_keys = {
          社会时事: 0,
          国际: 0,
          娱乐: 0,
          军事: 0,
          科技: 0,
          历史文化: 0,
          常识: 0,
          母婴育儿: 0,
          教育: 0,
          情感: 0,
        };
        for (let i = 0; i < month_result_length; i++) {
          let every_obj = month_result[i];
          for (const everyObjKey in every_obj) {
            if (everyObjKey != "date" && everyObjKey != "ids") {
              topic_keys[everyObjKey] =
                topic_keys[everyObjKey] + every_obj[everyObjKey];
            }
          }
        }
        for (let topicKeysKey in topic_keys) {
          res[resKey][topicKeysKey] = topic_keys[topicKeysKey];
        }
      }

      return res;
    },
    stackMin(data) {
      return d3.min(data, (d) => d[0]);
    },
    stackMax(data) {
      return d3.max(data, (d) => d[1]);
    },
    idtotopic() {
      let region = this.newDataset;
      var a = 0;
      var b = 0;

      let res = [];

      region.forEach((eachday) => {
        let day = {
          军事: 0,
          历史文化: 0,
          国际: 0,
          娱乐: 0,
          常识: 0,
          情感: 0,
          教育: 0,
          母婴育儿: 0,
          社会时事: 0,
          科技: 0,
          date: eachday.date,
          ids: {},
        };
        //console.log(day)
        Object.keys(eachday.ids).forEach((topic) => {
          for (var i = 0; i < eachday.ids[topic].length; i++) {
            this.map_result.forEach((e) => {
              if (e === eachday.ids[topic][i]) {
                if (typeof day.ids[topic] != "undefined") {
                  day.ids[topic].push(e);
                  day[topic]++;
                } else {
                  day.ids[topic] = [];
                  day.ids[topic].push(e);
                  day[topic]++;
                }
                //console.log(day)
                a++;
              }
            });
          }
        });
        //console.log(day)
        res.push(day);
      });

      var c = 0;
      res.forEach((e) => {
        Object.keys(e.ids).forEach((topic) => {
          for (var i = 0; i < e.ids[topic].length; i++) {
            c++;
          }
        });
      });

      return this.Week(res);
    },
  },
  mounted() {
    this.$net.sendOverviewData("time2topic", this.setTime2Map);
    //this.$net.sendRiverKeywords(["InzJsiQ1k", "InFnuqpW4"],this.setRiverKeywords)
    PipeService.$on("passmap", (val) => {
      this.map_result = val;
    });

    //this.$net.sendRiverKeywords(this.getid(this.newWeekDataset),this.setRiverKeywords)
    //this.$net.sendRiverKeywords(["InzJsiQ1k", "InFnuqpW4"],this.setRiverKeywords)
  },
};
</script>

<style scoped>
#themeriver {
  height: 50%;
  width: 100%;
}
svg {
  width: 100%;
  height: 100%;
}
</style>
