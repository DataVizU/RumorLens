<template>
  <div class="tree" ref="svgObject">
    <div class="hoverWindow">
      <div class="detailsText">
        <div
          class="detail-items"
          v-for="(item, index) in this.hoverList"
          :key="index * 1000"
        >
          <span class="content-title">{{ item.title }}</span>
          <span class="content-text">{{ item.content }}</span>
        </div>
      </div>
    </div>
    <div class="time-container"><svg class="time-barchart"></svg></div>
    <svg class="container-border" ref="treemap" :id="userid">
      <text x="10" y="35" style="font-size: 16pt; font-weight: 800">
        Propagation View
      </text>
      <text x="10" :y="svgHeight - 6" style="font-size: 16pt; font-weight: 800">
        Post Details View
      </text>
      <g>
        <path
          v-for="item in this.listResult"
          class="base"
          :key="item.ID"
          :d="findD(item.ID, pathData)"
          :style="getBaseStyle(item)"
        ></path>
      </g>

      <g>
        <path
          v-for="item in this.listResult"
          class="content"
          @click="click(item)"
          :key="item.ID2"
          :d="findD(item.ID, pathDataContent)"
          :style="getContentStyle(item)"
        ></path>
      </g>
      <g>
        <text
          class="content-text"
          v-for="item in this.listResult"
          :key="item.ID + '0'"
          :style="getTextStyle(item)"
        >
          {{ getKeyword(item) ? getKeyword(item) : "" }}
        </text>
      </g>
      <g>
        <path
          v-for="item in this.listResult"
          @mouseover="mouseover(item, $event)"
          @mousemove="mousemove(item, $event)"
          @mouseout="mouseout(item, $event)"
          @click="click(item)"
          @contextmenu.prevent="rightClick(item)"
          class="cover"
          :key="item.ID"
          :d="findD(item.ID, pathData)"
          :style="getCoverStyle(item)"
        ></path>
      </g>
      <g></g>
    </svg>
    <div class="legend">
      <div class="unit">
        <span class="unitTitle">Key Word of This Retweeting</span>
        <div class="legendBase">
          <div class="legendContent">
            <span class="legendText">Keyword</span>
          </div>
        </div>
      </div>
      <div class="emotion">
        <div class="line">
          <div class="color blue"></div>
          <span class="legendText">Positive</span>
        </div>
        <div class="line">
          <div class="color red"></div>
          <span class="legendText">Negative</span>
        </div>
        <div class="line">
          <div class="color yellow"></div>
          <span class="legendText">Neutral</span>
        </div>
      </div>
      <div class="center">
        <span class="legendText">Size:The Influence of the Origin Tweet</span>
        <div class="circle"></div>
      </div>
    </div>
    <span class="horizontal-line"></span>

    <div class="compare-window">
      <template
        v-if="
          this.detailWindowRight[0] == this.blankWindow ||
          this.detailWindowLeft[0] == this.blankWindow
            ? 0
            : 1
        "
      >
        <div
          class="compare-window-single left"
          v-for="(item, index) in this.detailWindowLeft"
          :key="index + 'cl'"
        >
          <div
            class="detail-items"
            v-for="(detailItem, index) in item.userdetail"
            :key="index + 'cld'"
          >
            <span class="content-text">{{ detailItem.content }}</span>
          </div>
        </div>
        <div
          class="compare-items"
          v-for="(item, index) in this.detailWindowLeft"
          :key="index + 'ci'"
        >
          <div
            class="detail-items"
            v-for="(detailItem, index) in item.userdetail"
            :key="index + 'ci'"
          >
            <span class="content-title">{{
              detailItem.title.slice(0, -2)
            }}</span>
          </div>
        </div>
        <div
          class="compare-window-single right"
          v-for="(item, index) in this.detailWindowRight"
          :key="index + 'cr'"
        >
          <div
            class="detail-items"
            v-for="(detailItem, index) in item.userdetail"
            :key="index + 'crd'"
          >
            <span class="content-text">{{ detailItem.content }}</span>
          </div>
        </div>
      </template>
      <template v-else>
        <div
          class="tree-detail-window-single"
          v-for="(item, index) in this.detailWindowLeft[0] == this.blankWindow
            ? this.detailWindowRight
            : this.detailWindowLeft"
          :key="index"
        >
          <div class="detail-content-single">
            <div class="contentdetails-single">
              <div class="detail-items-single">
                <span class="content-title">Create Time: </span>
                <span class="content-text">{{ item.createTime }}</span>
              </div>
              <div class="detail-items-single">
                <span class="content-title">Full Content: </span>
                <span class="content-text">{{ item.fullContent }}</span>
              </div>
              <div class="detail-items-single">
                <span class="content-title">Key Words: </span>
                <span class="content-text">{{ item.keyword }}</span>
              </div>
            </div>
            <span class="vertical-line"></span>
            <div class="userdetails-single">
              <template
                class="detail-items-single"
                v-for="(detailItem, index) in item.userdetail"
              >
                <div
                  :key="index + 'single-item'"
                  v-if="
                    detailItem.title != 'Create Time: ' &&
                    detailItem.title != 'Keywords: ' &&
                    detailItem.title != 'Full Content: '
                  "
                  class="single-item"
                >
                  <span class="content-title">{{ detailItem.title }}</span>
                  <span class="content-text">{{ detailItem.content }}</span>
                </div>
              </template>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
<script>
import * as d3 from "d3";
export default {
  props: {
    userid: String,
  },
  data() {
    return {
      svgHeight: "",
      svgWidth: "",
      listResult: [],
      detailWindowLeft: [],
      detailWindowRight: [],
      windowId: [],
      rawData: {},
      originTweetData: {},
      pathData: [],
      pathDataContent: [],
      pathDataText: [],
      timeDivide: [],
      textList: [],
      son: [],
      father: [],
      childScale: [],
      chosenID: "",
      fullContent: "",
      detailList: [],
      hoverList: [],
      borderTimes: 0.4,
      timedata: [],
      timeChosen: [],
      blankWindow: {
        fullContent: "",
        userdetail: [
          // { title: "Nickname: " },
          { title: "Authentication: " },
          { title: "Gender: " },
          // { title: "Birthday: " },
          // { title: "Province and City: " },
          { title: "Fans Number: " },
          { title: "Follows Number: " },
          { title: "Tweets Number: " },
          { title: "VIP Level: " },
          { title: "Create Time: " },
          { title: "Keywords: " },
          { title: "Full Content: " },
          // { title: "Lables: " },
          // { title: "Brief Introduction: " },
        ],
      },
    };
  },
  watch: {
    userid: function () {
      this.$net.sendTreeMap(this.userid, this.setTreemap);
    },
  },
  methods: {
    setTreemap(rep) {
      this.rawData = rep.data;
      if (this.rawData != null) {
        this.chosenID = "";
        this.pathData = [];
        this.pathDataContent = [];
        this.pathDataText = [];
        this.timeDivide = [];
        this.timedata = [];
        this.listResult = this.setListData(this.rawData);
        this.getOriginInfo(this.listResult);
        this.infoInit(this.originTweetData);
        this.getAllD();
        this.getTextList();
        this.setTimeBarchart();
      }
    },

    setTimeBarchart() {
      let chart = d3.select(".time-barchart");
      let width = 300,
        height = 200;
      let margin = { top: 30, right: 0, bottom: 30, left: 40 };
      // let backcolor = "#dddddd";
      let contentcolor = "rgb(219, 230, 254)";
      let data = this.timedata;
      console.log(this.timedata);
      chart.attr("viewBox", [0, 0, width, height]);
      chart.selectAll(".time-barchart > *").remove();
      let x = d3
        .scaleBand()
        .domain(d3.range(data.length))
        .range([margin.left, width - margin.right])
        .padding(0.5);
      let y = d3
        .scaleLinear()
        .domain([0, d3.max(data, (d) => d.value.length)])
        .nice()
        .range([height - margin.bottom, margin.top]);
      let xAxis = (g) =>
        g.attr("transform", `translate(0,${height - margin.bottom})`).call(
          d3
            .axisBottom(x)
            .tickFormat((i) => {
              if (i == 0) return "unknown";
              else return `day${i}`;
            })
            .tickSizeOuter(0)
        );
      let yAxis = (g) =>
        g
          .attr("transform", `translate(${margin.left},0)`)
          .call(d3.axisLeft(y).ticks(5))
          .call((g) => g.select(".domain").remove())
          .call((g) =>
            g
              .append("text")
              .attr("x", -margin.left)
              .attr("y", 10)
              .attr("fill", "currentColor")
              .attr("text-anchor", "start")
              .text("Number of Tweets")
          );

      chart
        .append("g")
        .selectAll("rect")
        .data(data)
        .join("rect")
        .attr("x", (d, i) => x(i))
        .attr("y", (d) => y(d.value.length))
        .attr("class", (d) => `rect-${d.name}`)
        .attr("fill", contentcolor)
        .attr("height", (d) => y(0) - y(d.value.length))
        .attr("width", x.bandwidth());
      chart.append("g").call(xAxis);
      chart.append("g").call(yAxis);

      for (let i in data) {
        let rect = document.querySelector(`.rect-${data[i].name}`);
        rect.addEventListener("click", () => {
          let allRects = document.querySelectorAll(".time-barchart rect");
          for (let i in allRects) {
            if (typeof allRects[i] == "object") {
              allRects[i].style.fill = "rgb(219, 230, 254)";
            }
          }
          if (this.timeChosen.length != data[i].value.length) {
            this.timeChosen = data[i].value;
            rect.style.fill = "rgb(119, 130, 154)";
          } else {
            this.timeChosen = [];
          }
        });
      }
    },

    getOriginInfo(listResult) {
      for (let i in listResult) {
        if (listResult[i].data.level == 0)
          this.originTweetData = listResult[i].data;
      }
    },
    setListData(rawData) {
      let dataArr = [];
      for (let i in rawData) {
        if (i != "comments") {
          let temp = new Object();
          temp.ID = i;
          temp.ID2 = i + "0";
          temp.ID3 = i + "#";
          temp.data = rawData[i];
          dataArr.push(temp);
        }
      }
      return dataArr;
    },
    infoInit(originTweetData) {
      let init = new Object();
      init.ID = originTweetData.content_id;
      init.userdetail = this.dataManage(originTweetData, "detail");
      init.fullContent = originTweetData.full_content;
      init.keyword = "no data";
      init.createTime = originTweetData.created_at;
      this.detailWindowLeft = [init];
      this.detailWindowRight = [this.blankWindow];
    },

    mouseover(item, event) {
      let window = document.querySelector(".hoverWindow");
      let father = document.querySelector(".tree");
      this.dataManage(item.data, "hover");
      window.style.display = "block";
      if (event.offsetX + 20 > 0.7 * father.offsetWidth) {
        window.style.top = event.offsetY + 60 + "px";
        window.style.left =
          event.offsetX - 20 - parseInt(window.style.width) + 900 + "px";
      } else {
        window.style.top = event.offsetY + 60 + "px";
        window.style.left = event.offsetX + 20 + 900 + "px";
      }
      if (this.hoverList[0].content == "No User Data")
        window.style.width = "130px";
      else window.style.width = "300px";
    },
    getKeyword(item) {
      if (this.textList.indexOf(item.ID) > -1) {
        if (item.hasOwnProperty("data"))
          if (item.data.hasOwnProperty("key_words"))
            if (item.data.key_words.length > 1) return item.data.key_words[0];
      } else return "";
    },

    dataManage(dataObj, prop) {
      // console.log("this is in func dataManage:", dataObj);
      let createTime = {
        title: "Create Time: ",
        content: `${dataObj.created_at}
`,
      };
      let fansNum = {
        title: "Fans Number: ",
        content:
          dataObj.user == ""
            ? ""
            : `${dataObj.user.fans_num}
`,
      };
      let followsNum = {
        title: "Follows Number: ",
        content:
          dataObj.user == ""
            ? ""
            : `${dataObj.user.follows_num}
`,
      };
      let authentication = {
        title: "Authentication: ",
        content:
          dataObj.user == ""
            ? ""
            : `${dataObj.user.authentication}
`,
      };
      let vipLevel = {
        title: "VIP Level: ",
        content:
          dataObj.user == ""
            ? ""
            : dataObj.user.vip_level
            ? `${dataObj.user.vip_level.slice(1)}
`
            : `${dataObj.user.vip_level}
`,
      };
      let location = {
        title: "Province and City: ",
        content:
          dataObj.user == ""
            ? ""
            : `${dataObj.user.province} ${
                dataObj.user.city ? dataObj.user.city : ""
              }
`,
      };
      let tweetsNum = {
        title: "Tweets Number: ",
        content:
          dataObj.user == ""
            ? ""
            : `${dataObj.user.tweets_num}
`,
      };
      let birthday = {
        title: "Birthday: ",
        content:
          dataObj.user == ""
            ? ""
            : `${dataObj.user.birthday}
`,
      };
      let briefIntroduction = {
        title: "Brief Introduction: ",
        content:
          dataObj.user == ""
            ? ""
            : `${dataObj.user.brief_introduction}
`,
      };
      let gender = {
        title: "Gender: ",
        content:
          dataObj.user == ""
            ? ""
            : `${dataObj.user.gender}
`,
      };
      let lables = {
        title: "Lables: ",
        content:
          dataObj.user == ""
            ? ""
            : `${dataObj.user.lables}
`,
      };
//       let nickName = {
//         title: "Nickname: ",
//         content:
//           dataObj.user == ""
//             ? ""
//             : `${dataObj.user.nick_name}
// `,
//       };
      let emotion = { title: "Emotion: ", content: "\n" };
      let keywords = {
        title: "Keywords: ",
        content: dataObj.hasOwnProperty("key_words")
          ? dataObj.key_words[0]
          : `
`,
      };
      let fullContent = {
        title: "Full Content: ",
        content: dataObj.full_content,
      };
      if (prop == "hover") {
        this.hoverList = [];
        if (dataObj.user == "")
          this.hoverList = [{ title: "", content: "No User Data" }];
        else
          this.hoverList.push(
            createTime,
            fansNum,
            followsNum,
            authentication,
            vipLevel,
            location,
            tweetsNum
          );
        return this.blankWindow.userdetail;
      } else if (prop == "detail") {
        let detailList = [];
        detailList.push(
          // nickName,
          authentication,
          gender,
          // birthday,
          // location,
          fansNum,
          followsNum,
          tweetsNum,
          vipLevel,
          createTime,
          keywords,
          fullContent
          // lables
          // briefIntroduction
        );
        return detailList;
      }
    },
    mousemove(item, event) {
      let window = document.querySelector(".hoverWindow");
      if (event.offsetX + 20 > 700) {
        window.style.top = event.offsetY + 60 + "px";
        window.style.left =
          event.offsetX - 20 - parseInt(window.style.width) + 900 + "px";
      } else {
        window.style.top = event.offsetY + 60 + "px";
        window.style.left = event.offsetX + 20 + 900 + "px";
      }
    },
    mouseout(item, event) {
      document.querySelector(".hoverWindow").style.display = "none";
    },
    click(item) {
      // console.log(item.data);
      console.log("this is in func click: ", item);
      this.son = [];
      this.father = [];
      this.timeChosen = [];
      if (this.chosenID != item.ID) {
        this.getSon(item);
        this.getFather(item);
        let clickItem = {};
        clickItem.fullContent = item.data.hasOwnProperty("content")
          ? item.data.content
          : item.data.full_content;
        clickItem.userdetail = this.dataManage(item.data, "detail");
        clickItem.createTime = item.data.created_at
          ? item.data.created_at
          : "no data";
        clickItem.keyword = this.getKeyword(item)
          ? this.getKeyword(item)
          : "no data";
        this.chosenID = item.ID;
        // console.log(this.detailWindowLeft);
        if (this.detailWindowLeft.length) this.detailWindowLeft[0] = clickItem;
        else this.detailWindowLeft.unshift(clickItem);
      } else {
        this.son = [];
        this.father = [];
        this.chosenID = "";
        if (this.detailWindowLeft.length > 1) this.detailWindowLeft.shift();
        else this.detailWindowLeft[0] = this.blankWindow;
      }
    },
    rightClick(item) {
      let temp = new Object();
      temp.fullContent = item.data.full_content;
      temp.userdetail = this.dataManage(item.data, "detail");
      temp.createTime = item.data.created_at ? item.data.created_at : "no data";
      temp.keyword = this.getKeyword(item) ? this.getKeyword(item) : "no data";
      temp.ID = item.ID;
      if (this.detailWindowRight.length) {
        if (this.detailWindowRight[0].ID === item.ID) {
          this.detailWindowRight = [this.blankWindow];
          this.windowId = [];
        } else {
          this.detailWindowRight = [temp];
          this.windowId = [item.ID];
        }
      } else {
        this.detailWindowRight = [temp];
        this.windowId = [item.ID];
      }
    },
    getSon(item) {
      let searchBuffer = [];
      if (item.data.son.length == 0) return 0;
      else {
        for (let i in item.data.son) {
          let ID = item.data.son[i];
          searchBuffer.push(ID);
        }
        for (let i in this.listResult) {
          if (searchBuffer.indexOf(this.listResult[i].ID) > -1) {
            this.son.push(this.listResult[i].ID);
            this.getSon(this.listResult[i]);
          }
        }
      }
    },
    getFather(item) {
      if (item.data.level > 0) {
        for (let i in this.listResult) {
          if (this.listResult[i].data.son.indexOf(item.ID) > -1) {
            this.father.push(item.ID);
            this.getFather(this.listResult[i]);
          }
        }
      } else return 0;
    },
    findD(ID, list) {
      for (let i in list) {
        if (list[i].name === ID) return list[i].d;
      }
    },
    getBaseStyle(item) {
      let childArr = this.childScale;
      let fill = (function getfill(itemdata, childScale) {
        let opacity;
        opacity = 0;
        // if (itemdata.son.length > 250) opacity = 1;
        // else opacity = itemdata.son.length / 250;
        return "fill:rgba(0,0,0," + opacity + ");";
      })(item.data, childArr);

      let border = (function getBorder() {
        return "stroke:black;stroke-width:0.4;stroke-opacity:0.7;";
      })();

      let transform =
        "transform:translate(" +
        this.svgWidth / 2 +
        "px," +
        this.svgHeight / 2 +
        "px);";
      return transform + fill + border;
    },

    getContentStyle(item) {
      let fill = (function getfill(itemdata) {
        let color;
        if (itemdata.emotion > 0) color = "#b0f4a6";
        else if (itemdata.emotion == 0) color = "#ffedc0";
        else if (itemdata.emotion < 0) color = "#ff9792";
        // color = "#ffffff";
        return "fill:" + color + ";";
      })(item.data);

      let transform =
        "transform:translate(" +
        this.svgWidth / 2 +
        "px," +
        this.svgHeight / 2 +
        "px);";
      return transform + fill;
    },

    getCoverStyle(item) {
      let transform =
        "transform:translate(" +
        this.svgWidth / 2 +
        "px," +
        this.svgHeight / 2 +
        "px);";
      let fill = "";
      if (this.chosenID != "") {
        if (this.son.indexOf(item.ID) > -1) fill = "opacity: 0;";
        else if (this.father.indexOf(item.ID) > -1) fill = "opacity: 0;";
        else if (this.windowId.indexOf(item.ID) > -1)
          fill = "fill:rgba(0,0,0,0.25);";
        else fill = "fill:rgba(0,0,0,0.6);";
        return transform + fill;
      } else if (this.timeChosen != "") {
        if (this.timeChosen.indexOf(item.ID) > -1) fill = "opacity:0;";
        else fill = "fill:rgba(0,0,0,0.6);";
        return transform + fill;
      } else {
        if (this.windowId.indexOf(item.ID) > -1) {
          fill = "fill:rgba(0,0,0,0.4);";
          return transform + fill;
        } else return transform + "opacity: 0;";
      }
    },

    getTextStyle(item) {
      let position = this.findD(item.ID, this.pathDataText);
      if (position) {
        let offsetX = this.svgWidth / 2 - 10,
          offsetY = this.svgHeight / 2 + 3;
        let wordLength = this.getKeyword(item);
        if (wordLength) wordLength = wordLength.length;
        let width = position.angleInterval * position.radius;
        let height = position.height;
        if (width < wordLength * 9 || height < 10) return "display: none";
        let x = offsetX + position.x - (wordLength - 2) * 4;
        let y = offsetY - position.y;
        let translate = "translate(" + x + "px," + y + "px) ";
        let angle =
          position.angle > Math.PI / 2 && position.angle < 1.5 * Math.PI
            ? -Math.PI + position.angle
            : position.angle;
        let spiral = "rotate(" + angle + "rad)";
        let transform = "transform:" + translate + spiral + ";";
        let origin2 = "transform-origin:0.8% -0.3%;";
        let origin3 = "transform-origin:1.2% -0.3%;";
        let origin4 = "transform-origin:1.6% -0.3%;";
        let origin;
        if (wordLength == 2) origin = origin2;
        else if (wordLength == 3) origin = origin3;
        else if (wordLength == 4) origin = origin4;
        return `${
          origin + transform + origin
        }font-weight: thin;font-size:9px;text-aligh:center`;
      }
    },
    getWindowStyle() {
      return "height:100%;" + "width:" + (49 % +";") + "float:left;";
    },

    getSingleD(partition, data, innerRadius, angleOffset, radiusInterval) {
      const root = d3.hierarchy(data, (d) => d.children).sum((d) => d.size); //对已经格式化的json数据处理得到根结点，对每个节点获得size属性用于计算总和
      let gramwidth = 100 * (radiusInterval / 2 + innerRadius) * 3.14,
        gramheight = 100 * radiusInterval;
      const treemap = d3.treemap().size([gramwidth, gramheight]); //规定整张图的大小
      let centerRadius = this.originTweetData.influence / 2;
      const tree = treemap(root); //构建树状图对象
      let leaves = tree.leaves();
      for (let i in leaves) {
        let arc = d3
          .arc()
          .innerRadius(
            innerRadius +
              centerRadius +
              (leaves[i].y0 * radiusInterval) / gramheight
          )
          .outerRadius(
            innerRadius +
              centerRadius +
              (leaves[i].y1 * radiusInterval) / gramheight
          );
        let angles = {
          startAngle:
            (leaves[i].x0 / (gramwidth / partition)) * Math.PI * 2 +
            angleOffset,
          endAngle:
            (leaves[i].x1 / (gramwidth / partition)) * Math.PI * 2 +
            angleOffset,
        };
        let temp = new Object();
        temp.name = leaves[i].data.name;
        temp.d = arc(angles);
        this.pathData.push(temp);
      }
    },
    getSingleDContent(
      partition,
      data,
      innerRadius,
      angleOffset,
      radiusInterval
    ) {
      const root = d3.hierarchy(data, (d) => d.children).sum((d) => d.size); //对已经格式化的json数据处理得到根结点，对每个节点获得size属性用于计算总和
      let gramwidth = 100 * (radiusInterval / 2 + innerRadius) * 3.14,
        gramheight = 100 * radiusInterval;
      const treemap = d3.treemap().size([gramwidth, gramheight]); //规定整张图的大小
      let centerRadius = this.originTweetData.influence / 2;
      const tree = treemap(root); //构建树状图对象
      let leaves = tree.leaves();
      let width = 4;
      let times = this.borderTimes;
      for (let i in leaves) {
        let arc = d3
          .arc()
          .innerRadius(
            innerRadius +
              centerRadius +
              (leaves[i].y0 * radiusInterval) / gramheight +
              width / 4
          )
          .outerRadius(
            innerRadius +
              centerRadius +
              (leaves[i].y1 * radiusInterval) / gramheight -
              width / 4
          );
        let angles = {
          startAngle:
            (leaves[i].x0 / (gramwidth / partition)) * Math.PI * 2 +
            angleOffset +
            width * 0.002,
          endAngle:
            (leaves[i].x1 / (gramwidth / partition)) * Math.PI * 2 +
            angleOffset -
            width * 0.002,
        };
        let temp = new Object();
        temp.name = leaves[i].data.name;
        temp.d = arc(angles);
        this.pathDataContent.push(temp);
      }
    },
    getsingleDText(partition, data, innerRadius, angleOffset, radiusInterval) {
      const root = d3.hierarchy(data, (d) => d.children).sum((d) => d.size); //对已经格式化的json数据处理得到根结点，对每个节点获得size属性用于计算总和
      let gramwidth = 100 * (radiusInterval / 2 + innerRadius) * 3.14,
        gramheight = 100 * radiusInterval;
      const treemap = d3.treemap().size([gramwidth, gramheight]); //规定整张图的大小
      let centerRadius = this.originTweetData.influence / 2;
      const tree = treemap(root); //构建树状图对象
      let leaves = tree.leaves();
      for (let i in leaves) {
        let radius =
          innerRadius +
          centerRadius +
          (((leaves[i].y1 + leaves[i].y0) / 2) * radiusInterval) / gramheight;
        let angles =
          ((leaves[i].x0 / (gramwidth / partition)) * Math.PI * 2 +
            angleOffset +
            ((leaves[i].x1 / (gramwidth / partition)) * Math.PI * 2 +
              angleOffset)) /
          2;
        let temp = new Object();
        temp.name = leaves[i].data.name;
        temp.d = {};
        temp.d.x = radius * Math.sin(angles);
        temp.d.y = radius * Math.cos(angles);
        temp.d.angle = angles;
        temp.d.angleInterval =
          ((leaves[i].x1 - leaves[i].x0) / (gramwidth / partition)) *
          Math.PI *
          2;
        temp.d.radius = radius;
        temp.d.height =
          ((leaves[i].y1 - leaves[i].y0) * radiusInterval) / gramheight;
        this.pathDataText.push(temp);
      }
    },
    getX(ID, list) {
      let position = this.findD(ID, list);
      if (position) return position.x;
      else return 0;
    },

    getY(ID, list) {
      let position = this.findD(ID, list);
      if (position) return -position.y;
      else return 0;
    },

    getTextList() {
      for (let i in this.pathDataText) {
        // console.log(this.pathDataText[i].name);
        this.textList.push(this.pathDataText[i].name);
      }
    },

    getAllD() {
      let childNum = [];
      let levels = new Object();
      let actuallRadius =
        this.svgWidth > this.svgHeight ? this.svgHeight / 2 : this.svgWidth / 2;
      let levelNum = -1;

      (function (data) {
        levels = new Object();
        let resData = data;
        for (let j in resData) {
          if (!levels[resData[j].level])
            levels[resData[j].level] = new Object();
          (function (item) {
            if (item.created_at) {
              let timeString = item.created_at;
              item.createTime = parseInt(
                timeString.slice(0, 10).split("-").join("")
              );
            } else item.createTime = 0;
          })(resData[j]);
          levels[resData[j].level][j] = resData[j];
        }
      })(this.rawData);

      let datas = {};
      datas = {};
      for (let i in levels) {
        if (i != "undefined") {
          datas["level" + i] = {};
          (function (level) {
            for (let i in level) {
              if (level[i].hasOwnProperty("son")) {
                if (
                  !datas["level" + level[i].level].hasOwnProperty([
                    level[i].createTime,
                  ])
                ) {
                  datas["level" + level[i].level][level[i].createTime] = {};
                  datas["level" + level[i].level][level[i].createTime].name =
                    "root";
                  datas["level" + level[i].level][
                    level[i].createTime
                  ].children = [];
                  datas["level" + level[i].level][level[i].createTime].sum = 0;
                }

                let temp = {};
                let copy = {};
                Object.assign(copy, level[i]);
                temp.name = i;
                temp.size = copy.words_num;
                temp.son = copy.son;
                temp.level = copy.level;
                childNum.push(temp.son.length);

                datas["level" + level[i].level][level[i].createTime].sum +=
                  temp.size;

                datas["level" + level[i].level][
                  level[i].createTime
                ].children.push(temp);
              }
            }
          })(levels[i]);
          levelNum += 1;
        }
      }
      childNum.sort((a, b) => a - b);
      this.childScale = childNum;

      datas.sum = 0;
      for (let i in datas) {
        if (i != "level0" && i != "sum") {
          datas[i].sum = 0;
          for (let j in datas[i]) {
            if (datas[i][j].hasOwnProperty("sum"))
              datas[i].sum += datas[i][j].sum;
          }
          datas.sum += datas[i].sum;
        }
      }
      let scale = (actuallRadius / (actuallRadius + 15 * levelNum)) * 0.8;
      let innerR = 0;
      let timeline = {};
      for (let i in datas) {
        let angle = 0;
        if (i != "level0") {
          let interval =
            (Math.sqrt(
              actuallRadius * actuallRadius * (datas[i].sum / datas.sum) +
                innerR * innerR
            ) -
              innerR) *
            scale;

          for (let j in datas[i]) {
            if (j != "sum") {
              let partition = datas[i][j].sum / datas[i].sum;
              this.getSingleD(partition, datas[i][j], innerR, angle, interval);
              this.getSingleDContent(
                partition,
                datas[i][j],
                innerR,
                angle,
                interval
              );
              this.getsingleDText(
                partition,
                datas[i][j],
                innerR,
                angle,
                interval
              );
              // this.getTimeDivide(partition, innerR, angle, interval);
              angle += 2 * Math.PI * partition;
              if (timeline.hasOwnProperty(j)) {
                // timeline[j] += datas[i][j].children.length;
                for (let index in datas[i][j].children) {
                  timeline[j].push(datas[i][j].children[index].name);
                }
              } else {
                timeline[j] = [];
                for (let index in datas[i][j].children) {
                  timeline[j].push(datas[i][j].children[index].name);
                }
              }
            }
          }
          innerR += interval + 10 * scale;
        } else if (i == "level0") {
          let arc = d3
            .arc()
            .innerRadius(0)
            .outerRadius(this.originTweetData.influence / 2 - 10 * scale);
          let angles = { startAngle: 0, endAngle: Math.PI * 2 };
          let temp = new Object();
          temp.name = this.originTweetData.content_id;
          temp.d = arc(angles);
          this.pathDataContent.push(temp);
        }
      }
      let count = 0;
      for (let i in timeline) {
        if (count <= 5) {
          let temp = {};
          temp.name = i == "0" ? "unkonw" : i;
          temp.value = timeline[i];
          this.timedata.push(temp);
          count++;
        }
      }
      // console.log(this.timedata);
    },
  },
  mounted() {
    this.$net.sendTreeMap(this.userid, this.setTreemap);
    this.svgHeight = this.$refs.svgObject.offsetHeight * 0.7;
    this.svgWidth = this.$refs.svgObject.offsetWidth * 1.2;
  },
};
</script>
<style scoped>
.tree {
  height: 100%;
  width: 100%;
  border-radius: 5px;
  border-radius: 5px;
  background-color: white;
}
.container-border {
  width: 100%;
  height: 70%;
}

.time-container {
  position: absolute;
  margin-left: 20px;
  margin-top: 7%;
  width: 200px;
  height: 150px;
}
.tree_details {
  display: flex;
  flex-flow: nowrap;
  height: 10%;
  width: 100%;
  margin: auto;
}
.tree-detail-window {
  height: 100%;
  width: 50%;
  float: left;
}
.horizontal-line {
  display: block;
  background: black;
  height: 1px;
  line-height: 1px;
  transform: scaleY(0.5);
  width: 100%;
}
.vertical-line {
  display: block;
  background: black;
  width: 1px;
  height: 100%;
  transform: scaleX(0.5);
}
.line-between {
  display: block;
  background: gray;
  height: 1px;
  line-height: 1px;
  transform: scaleY(0.5);
  width: 100%;
}
.compare-window {
  display: flex;
  flex-flow: nowrap;
  height: 30%;
  width: 100%;
  overflow: auto;
}
.compare-window-single {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  width: 40%;
}
.compare-items {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  width: 20%;
}
.left {
  text-align: right;
}
.right {
  text-align: left;
}
.compare-items {
  text-align: center;
}
.divide {
  display: block;
  background: black;
  width: 1px;
  height: 100%;
  margin: 0 15px;
  transform: scaleX(1.5);
}
.detail-items {
  height: 7%;
}
.detail-items:last-child {
  height: 27%;
  overflow: auto;
}
.compare-items .detail-items:last-child .content-title {
  margin-top: 13.5%;
  transform: translateY(-4.5px);
}
.detail-content {
  width: 100%;
  height: 100%;
  display: flex;
}
.contentdetails {
  width: 100%;
  margin: 5px;
  overflow: auto;
}

.detail-content-single {
  width: 100%;
  height: 100%;
  /* padding: 15px; */
  display: flex;
}
.contentdetails-single {
  width: 70%;
  margin: 5px;
  overflow: auto;
  white-space: pre-wrap;
}

.userdetails-single {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 30%;

  margin: 5px;

  overflow: auto;
  white-space: pre-wrap;
}

.tree-detail-window-single {
  height: 100%;
  width: 100%;
}
.hoverWindow {
  position: absolute;
  width: 320px;
  border-radius: 30px;
  background-color: white;
  display: none;
  z-index: 9;
  white-space: pre-wrap;
}
.detailsText {
  margin: auto;
  height: 90%;
  width: 90%;
}

.content-title {
  display: inline-block;
  font-family: "Poppins";
  font-weight: bold;
}
.content-text {
  display: inline-block;
  font-family: "noto sans";
}
g .content-text {
  font-size: 7pt;
  stroke: white;
  stroke-linejoin: round;
  stroke-width: 2px;
  paint-order: stroke;
}
.legend {
  width: 240px;
  height: 370px;
  margin-top: -300px;
  margin-left: 20px;
  position: absolute;
}
.unit {
  width: 100%;
  height: 85px;
  /* border: 1px solid; */
}
.emotion {
  margin: 9px 0 9px 0;
  width: 100%;
  height: 72px;
  /* border: 1px solid; */
}
.scale {
  width: 100%;
  height: 75px;
}
.center {
  width: 100%;
  height: 120px;
  margin-left: 5px;
  /* border: 1px solid; */
}
.unitTitle {
  display: inline-block;
  margin-left: 5px;
  font-family: "Poppins";
  font-weight: normal;
  font-size: 9px;
}
.legendBase {
  width: 100px;
  height: 40px;
  margin-top: 5px;
  margin-left: 5px;
  background-color: lightgray;
  border-radius: 3px;
}
.legendContent {
  position: absolute;
  width: 88px;
  height: 28px;
  margin: 6px;
  background-color: #ff9792;
  border-radius: 3px;
  text-align: center;
}
.legendText {
  height: 12px;
  line-height: 12px;
  font-family: "Poppins";
  font-weight: normal;
  font-size: 9px;
}
.legendContent .legendText {
  transform: translateX(20px);
}
.line {
  width: 100%;
  height: 24px;
  /* border: 0.1px solid; */
}
.color {
  margin: 5px;
  width: 14px;
  height: 14px;
  border-radius: 3px;
  float: left;
}
.red {
  background-color: #ff9792;
}
.yellow {
  background-color: #ffedc0;
}
.blue {
  background-color: #b0f4a6;
}
.block {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 26px;
  width: 26px;
  float: left;
  margin-top: 5px;
  line-height: 26px;
  text-align: center;
}
.scaleLegend {
  margin-left: 5px;
}
.scale > .legendText {
  margin-left: 5px;
}
.circle {
  height: 60px;
  width: 60px;
  border-radius: 100%;
  margin-top: 10px;
  border: 1px solid;
  transform-origin: left top;
  transform: scale(0.5);
}
</style>
