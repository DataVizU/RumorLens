<template>
  <div id="middle" ref="middleDiv">
<!--  <div class="row align-items-center">-->
<!--    <div class="col-sm-2"><p id="value-range"></p></div>-->
<!--    <div class="col-sm"><div id="slider-range"></div></div>-->
<!--  </div>-->
    <svg id="mainsvg"></svg>

    <!--测试组件间传值用-->
    <div id="getOverview" style="display: none">{{content_id}}</div>
    <!--测试组件间传值结束-->
  </div>
</template>
<!--<script src="https://unpkg.com/d3-simple-slider"></script>-->

<!--<link-->
<!--  rel="stylesheet"-->
<!--  href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"-->
<!--  integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO"-->
<!--  crossorigin="anonymous"-->
<!--/>-->
<script>
import * as d3 from 'd3'
import PipeService from "../../assets/js/pipe-service"
export default {
  name: "middle",
  data () {
      return {
        //content_id是bubble_chart对应需求的content_id 来自overview选择后的反馈数据 初始为上海地区
        content_id: [
          "InzJsiQ1k", "InFnuqpW4", "IocdREafF", "Io7AU2ycs", "ImK6c8cSz", "Io3ARb8iR", "IncktfXmK", "IonB45Xs2", "IofEGwaKE", "IofwIrUtu", "IopyFzr9w",
          "IozmFec6C", "Ip8QP05TS", "Ip8M16JxL", "Ip8XldyDf", "Ip8eWFbSj", "IoXtuwooZ", "Ip1kHgsUa", "Ip8Gk34G6", "Ip2evaZFw", "Iptu3rj0W", "Ipty8lciL",
          "IprjQF3gE", "IprrUBsgq", "Ipj5V6uqD", "Iplqi8XO1", "IpcPa66iA", "IptoezsNI", "IoSEzfDzd", "IpinJ1dGL", "IpjnxwwAp", "IoSGc3Klt", "Ip1vwjTrU",
          "Ipoyw1TRS", "IpeN6vZYI", "IpgKsBIdc", "IoYJAbJJL", "IphrHBzpO", "Ipldn1hI7", "IprnBwp0m", "IpBU17ofX", "IpsOrtDNK", "IpsVZvMNi", "IptAchAbS",
          "IpEcmyHqX", "IpLIVbfWb", "Iq2e10ns5", "Iqb818UDx", "Iq4kyeCRU", "IqNk34Ppx", "IpMREzpOH", "IqNpk8Kit", "IqNnEpRY0", "IqPXXCzEH", "IqQFfxCEH",
          "IqV15ahlk", "Ir6Hn4oOJ", "Ir66eyaps", "Ir6fNmSMd", "Ir6u5gIxd", "Ir1HoeMCG", "Ir2e318dG", "Ir55P6Da5", "Ir1YOBx1s", "Ir1Mk6AFC", "Ir6gCaKE7",
          "Ir1IqFAkF", "Ir1ZntSVo", "Ir1z0tApl", "Ir1vvBx1A", "Ir219mDha", "Ir81xkCMw", "Ir25OnH6T", "Ir778sKuy", "Ir6yWjZ3S", "Ir7C3lbFt", "Ir5chfB0Q",
          "IqHmSy5e7", "Irhj441G7", "Irh0MiBEf", "IqQaVEA3n", "IrfJKoNma", "IrnSL61Lr", "IrqGM69O6", "IqM32E8p5", "Ir1ufhd0W", "IrLBgs95V", "Irz7cqtdq",
          "IrLqSBrak", "IrLzlFrNB", "IrMIRznEW", "IrJiN3PjW", "IrM9FlPHj", "IrQU5ETxj", "IrMqcEx6H", "IrSHmwvB6", "IrQSjaRGh", "IrRZMwz5s", "IrRFBF44i",
          "IrMe3dWip", "IrQXboZw9", "IrQanzyNq", "IrQi3DiOs", "IrWxbwi8l", "IrLE6AiZV", "IrzoSpGLE", "Is8mMj2Il", "Is4tAifaC", "IsrffjJ6t", "Istwpdnfr",
          "ICdWpg0IX", "IsnR8dYvF", "IsoWvliqT", "IsrQuf0ba", "IsshW0qe6", "Is2oc2EjE", "IsnM6cczV", "IsnOjBOZY", "Iss4XFyUr", "Iss69eBIk", "Isvxgv5zu",
          "IsB3JDMV2", "IsvRpxVil", "IsCuul10e", "IsDXRrcIM", "IsImv7WqK", "IsDEiaTkR", "IsCeF0gmr", "IsDrC9Ff6", "IsEAAkGIS", "IsEoesr4Q", "IsCS5jDsz",
          "IsDTe0KoJ", "IsEAv39Jm", "IsF6u4JOE", "IsDS2Eef9", "IsEyB7oD3", "IsFIj88qO", "IsFXo44xw", "IsHpmkE51", "IsPNjAOe5", "IsPsJoISU", "IsQ5zDawh",
          "IsObsvmC5", "IsMlnB2RX", "IsPobfrRV", "IsRuG67sY", "IsN1B4FUy", "IsUXlDx2E", "IsWGuh4Fv", "IsXvm61SV", "IsZPNhHLP", "It4BWfpfq", "It4xXeTYQ",
          "It7bruyva", "IsPojbXqS", "It56P254O", "It8EufXmN", "ItfahfwiH", "IsFyVg476", "IsOhT5voh", "ItiRG9IPc", "Ito2j6fm4", "IsIHQ40OZ", "IsXtL5RkV",
          "IsaTPBRoV", "ItzIArnqd", "ItQzsCINP", "ItS3IbNvl", "ItRt0ifs2", "ItSii4Hrr", "ItVfbyUL3", "Ite86sHD7", "Iuw5YnvnL", "IuzrdzMoq", "IuCIJ5t4w",
          "IuE3JmTLn", "IuvMxobEP", "Iuw7fA7E4", "IuOH43EOQ", "Iv1zZEvmV", "Iv2FZ9vJP", "Iv3TIeurL", "IuZ0rtfQ1", "Iv6GBualh", "Ivf0JfbOo", "Iv6ywnoUA",
          "IvgKQc5ZQ", "IuV9MrHIu", "IvgzDsaiN", "Ivrbo5d6r", "IvHZ2aKfQ", "IvIfKd3Dm", "IvxcauP2T", "Ivu3kfsdQ", "IvIiJsbWl", "IvIluwxDH", "IvOA9dNTp",
          "IvMM8zuPA", "IvDu7780O", "IvCKb93cy", "IvHq82cRT", "IvIVYvpRF", "IvZlMlkYa", "Ivvn7rjZo", "Iw1V5qQVk", "IwqT2lIyz", "Iw1BhEBNC", "Iwqcd17LF",
          "Iw7BiiT17", "IwquXwcbc", "Iw1D6ABIN", "Iw6UAqbnZ", "IwrbmeCt0", "IwtsWlsWE", "Iw1Ra1oFX", "IwK0ltkKb", "IwqHFikIJ", "IwzPSDkEK", "IwIu1opfC",
          "IwFJ6dsuQ", "IwQPFpifN", "IwQTPo5BZ", "IwDO0oeOm", "IvhdX2yXw", "IwSih1mRV", "IwUL5lQ7Y", "IvkWla46R", "IvqA7yB5t", "IvvHMpjMa", "IvvRb7JUp",
          "IvDdteU5s", "Ivw9zqfkm", "IvwFRobHt", "IvwtlqTTT", "IwDOzhj1E", "IwF8Llkmx", "IwHbMe89M", "IwzXGDrtP", "IuWen3hMQ", "IwL3HiYOE", "IwLtnFPNj",
          "IwMVhvKOf", "IuOScAMS4", "IuOiTjY9a", "IuQ1qtbCF", "IuWQmo7jz", "IuTKn5h3x", "IuTO24JFg", "IuUpkhvaj", "IuUsp9inD", "IuVH4sWWU", "IuVxfrhJm",
          "IuVy5bh7i", "IwVj0CpvA", "IpC1SCQAk", "IpD21gkN3", "IpIN9qc8a", "It0GFc4Wz", "IxPxuyNUc", "IxQkudVv8", "IxkP9EgF5", "IxPaLo8wu", "IxOnXxzNQ",
          "IxPPU2nxi", "IxPl2a2eG", "IxQpX9dIb", "IxNyjg6nt", "IxOcOlwy6", "IxQmOohbl", "IxQw8FtbG", "IxP6keKj1", "IxFlBlu8Q", "IxQ5G8ird", "IxTRjpgcZ",
          "IxReD7IVL", "IxVaY5L2h", "IxXSFywll", "Iy5badryg", "IxDGFA7JG", "IxHkJmyvq", "IxS1mdLqy", "IxVw9Ajsj", "IqlqYhW16", "IxQZR69d5", "IxVV2iAP9",
          "IxVxjoS2O", "IqfAXADVD", "IxOtWCPmZ", "IxQNdry8P", "IybidxQdL", "IyfGZc80p", "IyfHSqTPn", "IygTXyus4", "Iygj7orDf", "IyidsaZ3T", "Iyaa9ec57",
          "IyiwXjbhj", "IykFrnrVC", "IxZbRzROv", "Iyh2SrmDY", "IymSla2Lb", "Iypzx0fDm", "IyIadte7f", "IyL3xpmjL", "IynIerirI", "IytQFcFmm", "IyJt1AelP",
          "IyLAErjLB", "IyLH9xs50", "IyLNDFwuV", "IyLOky7BZ", "IyPIP94ky", "IySaAwmqa", "IySnlgROR", "IyQEh2A5K", "IyR5Hi1UF", "IyRDFghPf", "IyS7zufpY",
          "IyLYMe6To", "IyRLwd5jh", "IyRKPDrHJ", "Iz02W5Tpd", "IyUGaiZi8", "IyQPk0jAN", "IyipqpLSg", "Iz3u1Aq5T", "IyLnZlfIi", "Iz0U07rVI", "Iz1Zpg6V6",
          "Iz5u17SQK", "IyUMAiy7f", "IxMS4CUf5", "Iz46ppXQ8", "IyVTrwCoU", "IztdxqdxP", "IzuCjubDz", "IzuoblfF4", "IzvkH56Xi", "IzuMHBInA", "IzuVJAhlN",
          "Izu9VeBEP", "IzxatoAoA", "IzvUAb9yT", "Izw3vjAp1", "IzwAdzwZV", "Izwyoo7ls", "IztH91Qbj", "IzwJE3LkV", "IzwVWo1Ya", "IzwVo9XjU", "IzBxo1BDR",
          "IzvPE0IuM", "IzwyxgXOk", "IzxNQ7rAR", "IzAj4iREj", "IzCnduS2d", "Izvb6xbN9", "IzvqNB02H", "IzB3Bv6Jt", "IzBx8ntA9", "IzEUrbjtF", "IzCfY2fXp",
          "IzA34Ayh4", "IzJkchIeR", "IzMqL18zI", "IzLr8BOAl", "IzJYPBvoc", "IzDheq4Cc", "IzKmSosSY", "IzKuxcQXg", "IzPMyugqb", "IzBiHAeLy", "IzUKnrkKC",





        ],
        bubble_chart_data:{},
        dimension_reduction_data:{}
      }
    },
  methods: {
    //设置绘制气泡图数据的回调函数
    setBubbleData(response){
      this.bubble_chart_data = response.data
      console.log(this.bubble_chart_data)
      //此处应写生成d3气泡图的方法！！
      const legend_width = 100;//图例宽
      const width = this.$refs.middleDiv.offsetWidth;
      const height = this.$refs.middleDiv.offsetHeight;

      const svg = d3.select('#mainsvg').attr("width",width).attr("height",height);

      const margin = {top: 50, right: 80, bottom: 20, left: 30};//内框边距
      const innerWidth = width - margin.left - margin.right;//内框宽
      const innerHeight = height - margin.top - margin.bottom;//内框高

      //更新前清空svg画布
      svg.selectAll("*").remove();

      //处理数据
      const dataset = this.bubble_chart_data
      const data_length = dataset.length
      const xValue = function(d){return d.coordinate[0]};
      const yValue = function(d){return d.coordinate[1]};
      const yValue2 = d=>d.topic.topic;
      const zValue = d=>d.influence;
      const colorValue = d =>d.topic.topic;
      const fans=d=>d.user.fans_num;
      const follows=d=>d.user.follows_num;
      const pics=d=>d.pics
      let y_trans = -105
      let x_trans = 0
      let scale_rate = 0.3


      const radius = [-15,20];
      //
      dataset.sort(function(b,a){
        return a.influence-b.influence
        })
      const time_arr = [ ];
      const emo_arr = [ ];
      const emo_neg_arr = [ ];
      const ifl_arr = [ ];
      const tpc_arr = [ ];
      const len_arr = [ ];
      const fans_arr = [ ];
      const follows_arr = [ ];
      const tweets_arr = [ ];
      const user_info=[];
      var userInfo=0;

      const colors = ['#b871c9','#BE3636','#528fc6','#95e0f4','#ffedc0','#47a875','#ddc0ff','#f45540','#ff9792','#b0f4a6'];
      const topics = ['社会时事','母婴育儿','国际','娱乐','教育','常识','科技','军事','历史文化','情感'];
      const topics2 = ['社会时事','母婴育儿','国际','娱乐','教育','常识','科技','军事','历史文化','情感'];
      const x_arr=[];
      const y_arr=[];
      const nodes_data=[];

      //将传入的数据format成数组
      for(let i = 0; i <= data_length - 1 ;i++){
        dataset[i].time = new Date(dataset[i].time)
        time_arr.push(dataset[i].time)
        emo_arr.push(dataset[i].emotion.positive_prob)
        emo_neg_arr.push(dataset[i].emotion.negative_prob)
        fans_arr.push(dataset[i].user.fans_num)
        follows_arr.push(dataset[i].user.follows_num)
        tweets_arr.push(dataset[i].user.tweets_num)
        ifl_arr.push(dataset[i].influence)
        tpc_arr.push(dataset[i].topic)
        len_arr.push(dataset[i].length)
        x = Math.round(+dataset[i].coordinate[0])
        y = Math.round(+dataset[i].coordinate[1])
        x_arr.push(x)
        y_arr.push(y)
        user_info.push([])
        nodes_data.push([])
          if(dataset[i].user.authentication != null){
            userInfo += 1
          }
          if(dataset[i].user.birthday != null){
            userInfo += 1
          }
          if(dataset[i].user.brief_introduction != null){
          userInfo += 1
          }
          if(dataset[i].user.city != null){
            userInfo += 1
          }
          if(dataset[i].user.gender != null){
            userInfo += 1
          }
          if(dataset[i].user.labels != null){
            userInfo += 1
          }
          if(dataset[i].user.nick_name != null){
            userInfo += 1
          }
          if(dataset[i].user.province != null){
            userInfo += 1
          }

          user_info[i].push([userInfo/8])
          userInfo = 0

      };

      //定义Scale
      //x轴
      const xScale = d3.scaleLinear()
        .domain([d3.min(x_arr),d3.max(x_arr)])
        .range([50-width, 0-margin.right-legend_width - 90]);
      //y轴
      const yScale = d3.scaleLinear()
        .domain([d3.min(y_arr),d3.max(y_arr)])
        .range([radius[1]+margin.top + 10, height-radius[1]-margin.bottom - 10 ]);
      //大小
      const zScale = d3.scaleSqrt()//circle size
        .domain([0, d3.max(dataset, d=>d.influence)])
        .range(radius);
      //粉丝数
      const fansScale = d3.scaleLinear()
        .domain(d3.extent(fans_arr))
        .range([0,2]);
      //关注数
      const followsScale = d3.scaleLinear()
        .domain([d3.min(follows_arr),d3.max(follows_arr)])
        .range([0,2]);
      //发博数
      const tweetsScale = d3.scaleLinear()
        .domain(d3.extent(tweets_arr))
        .range([0,2]);

      const colorScale = d3.scaleOrdinal()
        .domain(topics)
        .range(colors);
      const legendYScale = d3.scaleBand()
        .domain(topics)
        .range([0,innerHeight])
      legendYScale
        .bandwidth(20)
      // console.log(legendYScale(topics))

      const g = svg.append("g")
        .attr('width',innerWidth)
        .attr('height',innerHeight)
        .attr("transform", `translate(${margin.left+legend_width},${margin.top})`);

      //legend背景白色方块
      svg
        .append('rect')
        .attr('x',0)
        .attr('y',205 + y_trans )
        .attr('width',170)
        .attr('height',`${height - 150}`)
        .attr("transform", `translate(${margin.left-20},-${margin.top})`)
        .attr('fill','white')
        .attr('stroke','gray')
        .attr('opacity',0.85)
        .attr('rx',"5")

      const thumb =
        svg
          // .selectAll('rect').data(dataset).enter()
          .append('rect')
          .attr('x', 0)
          .attr('y', 277)
          .attr('width',195)
          .attr('height',`${height - 235}`)
          .attr("transform", `translate(${margin.left-20},-${margin.top})`)
          .attr('fill','none')
          .attr('stroke','gray')
          .attr('opacity',0.85)
          .attr('rx',"5")




      const legend = svg.append('g')
        .attr('class','legend')
        .attr('width',legend_width)
        .attr('height',innerHeight)
        .attr("transform", `translate(${margin.left},${margin.top})`)

      const thumbnail = svg.append('g')
        .attr('class','thumbnail')
        .attr('width',170)
        .attr('height',`${height - 240}`)
        .attr("transform", "translate(-50,215)")


      //绘制图例
      svg.append('text')
        .attr('y',35)
        .attr('x',margin.left-15)
        .attr('font-size','16pt')
        .attr("text-anchor","left")
        .text('Features Projection View')
        .attr("font-weight", "800")


      //创建图形

      var x = function(d){return -xScale( d.coordinate[0])}
      var y = function(d){return yScale( d.coordinate[1])}
      // console.log(x)
      // 缩放
      const delaunay = d3.Delaunay.from(dataset, d => xScale(xValue(d)), d => yScale(yValue(d)));

      //thumbnail背景白色方块
      // const thumb_select =
      //   thumbnail
      //     .selectAll('rect').data(dataset).enter()
      //     .append('rect')
      //     .attr('x', function(d){return (60 * xScale(xValue(d))/ xScale(xValue(d)))})
      //     .attr('y', function(d){return (7 * yScale(yValue(d))/ yScale(yValue(d)))})
      //     .attr('width',195)
      //     .attr('height',`${height - 245}`)
      //     .attr("transform", `translate(${margin.left-20},-${margin.top})`)
      //     .attr('fill','none')
      //     .attr('stroke','steelblue')
      //     .attr('stroke-width',0.1)
      //     .attr('opacity',0.5)
      //     .attr('rx',"5")

      //主体图形
      const points =g.selectAll('circle').data(dataset)
        .enter().append('circle')
        .attr('cy',y)
        .attr('cx', x)
        .attr('r',d=> zScale(zValue(d)))
        .attr('opacity',0.8)
        .attr('fill', d=>colorScale(colorValue(d)))
        .on("mouseover",function(d,i){
          d3.select(this)
            .attr("fill","blue")
            .attr('opacity',0.6)
            ;
        })
        .on("mouseout",function(d,i){
          d3.select(this)
            .attr('fill', d=>colorScale(colorValue(d)))
            .transition()
            .attr('opacity',0.8)
            .duration(300);
        })
        .on("click",function (d,i){
          //平行传递两个点击的气泡userId给detail组件
          PipeService.$emit('middleByValue', i.content_id)
        })


      const g0 = g.append('g');
      // .attr('transform', 'translate(' + 0 + ',' + -5 + ')')
      const points1 =g0.selectAll('circle').data(dataset)
        .enter().append('circle')
        .attr('cy',y)
        .attr('cx', x)
        // .attr('r',function(d){return pics(d)*2})
        .attr('opacity',0.8)
        .attr('fill','black')
        .on("mouseover",function(d,i){
          d3.select(this)
            .attr("fill","blue")
            .attr('opacity',0.6)
            ;
        })
        .on("mouseout",function(d,i){
          d3.select(this)
            .attr('fill', d=>colorScale(colorValue(d)))
            .transition()
            .attr('opacity',0.8)
            .duration(300);
        })
        .on("click",function (d,i){
          //平行传递两个点击的气泡userId给detail组件
          PipeService.$emit('middleByValue', i.content_id)
        })

      //缩略图
      const thumbnail_view =thumbnail.selectAll('circle').data(dataset)
        .enter().append('circle')
        .attr('cy',y)
        .attr('cx', x)
        .attr('r',d=> zScale(zValue(d)))
        .attr('opacity',0.8)
        .attr('fill', d=>colorScale(colorValue(d)))
        .attr("transform","scale(0.3)")

      thumbnail.append('text')
        .attr('x',95)
        .attr('y',129)
        .attr("text-anchor","left")
        .attr('font-size',fontSize)
        .text('Thumbnail View')
        .attr("transform","scale(0.7)")

        //颜色
        const arc1_color = "#575757"
        const arc2_color = "#808080"
        const arc3_color = "#bdbdbd"
        const arc4_color = "rgba(203,203,203,0.62)"
        //第1个圆环
        for(let i = 0; i <= data_length - 1 ;i++){
          var arc1 = d3.arc()
            .innerRadius(function(d) { return zScale(zValue(d)) *0.5})
            .outerRadius(function(d) { return zScale(zValue(d)) *0.5 +1.5})
            .startAngle(0 * Math.PI)
            .endAngle(user_info[i] * Math.PI);
        }

        //第2个圆环fans

        var arc2 = d3.arc()
          .innerRadius(function(d) { return zScale(zValue(d)) *0.5+1.5})
          .outerRadius(function(d) { return zScale(zValue(d)) *0.5+3})
          .startAngle(0 * Math.PI)
          .endAngle(d=> fansScale(d.user.fans_num) * Math.PI);

        //第3个圆环follows
        var arc3 = d3.arc()
          .innerRadius(function(d) { return zScale(zValue(d)) *0.5+3})
          .outerRadius(function(d) { return zScale(zValue(d)) *0.5+4.5})
          .startAngle(0 * Math.PI)
          .endAngle(d=> followsScale(d.user.follows_num) * Math.PI);

        //第4个圆环tweets

        var arc4 = d3.arc()
          .innerRadius(function(d) { return zScale(zValue(d)) *0.5+4.5})
          .outerRadius(function(d) { return zScale(zValue(d)) *0.5+6})
          .startAngle(0 * Math.PI)
          .endAngle(d=> tweetsScale(d.user.tweets_num) * Math.PI);

        var g1=g.append('g')
        const arc_1 = g1.selectAll('path')
          .data(dataset).enter()
          .append("path")
          .attr("class", "arc")
          .attr("d", arc1)
          .attr("fill",arc1_color)
          .attr('stroke-width','1')
          .attr('opacity',0.8)
          .attr("transform",function(d) { return "translate(" + xScale(xValue(d)) + "," + yScale(yValue(d)) + ")"; })

        var g2=g.append('g')
        const arc_2 = g2.selectAll('path')
          .data(dataset).enter()
          .append("path")
          .attr("class", "arc")
          .attr("d", arc2)
          .attr("fill",arc2_color)
          .attr('stroke-width','1')
          .attr('opacity',0.8)
          .attr("transform",function(d) { return "translate(" + xScale(xValue(d)) + "," + yScale(yValue(d)) + ")"; })

        var g3=g.append('g')
        const arc_3 = g3.selectAll('path')
          .data(dataset).enter()
          .append("path")
          .attr("class", "arc")
          .attr("d", arc3)
          .attr("fill",arc3_color)
          .attr('stroke-width','1')
          .attr('opacity',0.8)
          .attr("transform",function(d) { return "translate(" + xScale(xValue(d)) + "," + yScale(yValue(d)) + ")"; })

        var g4=g.append('g')
        const arc_4 = g4.selectAll('path')
          .data(dataset).enter()
          .append("path")
          .attr("class", "arc")
          .attr("d", arc4)
          .attr("fill",arc4_color)
          .attr('stroke-width','1')
          .attr('opacity',0.8)
          .attr("transform",function(d) { return "translate(" + xScale(xValue(d)) + "," + yScale(yValue(d)) + ")"; })




        const top = 0
        const bandwidth = 65
        const bandwidth2= 30
        const fontSize="9pt"

        const innerRadius1 = 19
        const outerRadius1 = 24

        const innerRadius2 = 24
        const outerRadius2 = 29

        const innerRadius3 = 29
        const outerRadius3 = 34

        const innerRadius4 = 34
        const outerRadius4 = 39

        const left=50

        const adjustCoe = -0.025

        // const yTransCoe1=height*(0.08 + adjustCoe)
        // const yTransCoe2=height*(0.14 + adjustCoe)
        // const yTransCoe3=height*(0.17 + adjustCoe)

        // const yTransCoe4=height*(0.24 + adjustCoe)
        // const yTransCoe5=height*(0.31 + adjustCoe)

        // const yTransCoe6=height*(0.38 + adjustCoe)
        // const yTransCoe7=height*(0.45 + adjustCoe)

        // const yTransCoe8=height*(0.53 + adjustCoe)
        // const yTransCoe9=height*(0.61 + adjustCoe)

        const yTransCoe10=height*(0.67 + adjustCoe)+45 +y_trans
        // const yTransCoe11=height*(0.74 + adjustCoe)
        // const yTransCoe12=height*(0.77 + adjustCoe)

        // const yTransCoe13=height*(0.81 + adjustCoe)
        // const yTransCoe14=height*(0.85 + adjustCoe)
        // const yTransCoe15=height*(0.88 + adjustCoe)



        var arc_legend1 = d3.arc()
          .innerRadius(innerRadius1)
          .outerRadius(outerRadius1)
          .startAngle(0 * Math.PI)
          .endAngle(1.55 * Math.PI);

        var arc_legend2 = d3.arc()
          .innerRadius(innerRadius2)
          .outerRadius(outerRadius2)
          .startAngle(0 * Math.PI)
          .endAngle(1.4 * Math.PI);

        var arc_legend3 = d3.arc()
          .innerRadius(innerRadius3)
          .outerRadius(outerRadius3)
          .startAngle(0 * Math.PI)
          .endAngle(1.2 * Math.PI);

        var arc_legend4 = d3.arc()
          .innerRadius(innerRadius4)
          .outerRadius(outerRadius4)
          .startAngle(0 * Math.PI)
          .endAngle(1.1 * Math.PI);



        legend
          .append("path")
          .attr("class", "arc")
          .attr("d", arc_legend1)
          .attr("fill",arc1_color)
          .attr('stroke-width','1')
          .attr('opacity',0.8)
          .attr("transform","translate(" + left + "," + yTransCoe10 + ")")

        legend
          .append('text')
          .attr('x',67)
          .attr('y',197+y_trans)
          .attr("text-anchor","left")
          .attr('font-size',fontSize)
          .text('Integrity of ')

        legend
          .append('text')
          .attr('x',67)
          .attr('y',210+y_trans)
          .attr('font-size',fontSize)
          .attr("text-anchor","left")
          .text(' user information')

        legend
          .append("path")
          .attr("class", "arc")
          .attr("d", arc_legend2)
          .attr("fill",arc2_color)
          .attr('stroke-width','1')
          .attr('opacity',0.8)
          .attr("transform","translate(" + left + "," + yTransCoe10  + ")")

        legend
          .append('text')
          .attr('x',92)
          .attr('y',233+y_trans)
          .attr('font-size',fontSize)
          .attr("text-anchor","left")
          .text('Fans num')

        legend
          .append("path")
          .attr("class", "arc")
          .attr("d", arc_legend3)
          .attr("fill",arc3_color)
          .attr('stroke-width','1')
          .attr('opacity',0.8)
          .attr("transform","translate(" + left + "," + yTransCoe10 + ")")

        legend
          .append('text')
          .attr('x',97)
          .attr('y',268+y_trans)
          .attr('font-size',fontSize)
          .attr("text-anchor","left")
          .text('Followees num')

        legend
          .append("path")
          .attr("class", "arc")
          .attr("d", arc_legend4)
          .attr("fill",arc4_color)
          .attr('stroke-width','1')
          .attr('opacity',0.8)
          .attr("transform","translate(" + left + "," + yTransCoe10 + ")")

        legend
          .append('text')
          .attr('x',77)
          .attr('y',298+y_trans)
          .attr('font-size',fontSize)
          .attr("text-anchor","left")
          .text('Tweets num')

        legend
          .append("circle")
          .attr('r',innerRadius1)
          .attr("fill","#b6d0fc")
          .attr('stroke-width','1')
          .attr('opacity',0.8)
          .attr("transform","translate(" + left + "," + yTransCoe10 + ")")

        legend
          .append('text')
          .attr('x',10)
          .attr('y',160+y_trans)
          .attr("text-anchor","left")
          .attr('font-size',fontSize)
          .text('Size ' + " " + ' : Influence')

        legend
          .append('text')
          .attr('x',10)
          .attr('y',173+y_trans)
          .attr("text-anchor","left")
          .attr('font-size',fontSize)
          .text('Color : Topic')

        legend
          .append("circle")
          .attr('r',2)
          .attr("fill","black")
          .attr('stroke-width','1')
          .attr('opacity',0.8)
          .attr("transform","translate(" + left + "," + (yTransCoe10-13) + ")")

        legend
          .append('text')
          .attr('x',12)
          .attr('y',320+y_trans)
          .attr('font-size',fontSize)
          .text('Whether there any ')
        legend
          .append('text')
          .attr('x',12)
          .attr('y',333+y_trans)
          .attr('font-size',fontSize)
          .text('pictures or videos')

        var lineData1=[
          {"x":52,   "y":231+y_trans},
          // {"x":52,  "y":200},
          {"x":65,  "y":200+y_trans},
        ];

        var lineData2=[
          {"x":72,   "y":239+y_trans},
          // {"x":72,  "y":215},
          {"x":90,  "y":230+y_trans},
        ];

        var lineData3=[
          {"x":77,   "y":265+y_trans},
          // {"x":72,  "y":215},
          {"x":95,  "y":265+y_trans},
        ];

        var lineData4=[
          {"x":50,   "y":288+y_trans},
          {"x":50,  "y":295+y_trans},
          {"x":75,  "y":295+y_trans},
        ];

         var lineData5=[
          {"x":50,   "y":239+y_trans},
          {"x":50,  "y":265+y_trans},
          {"x":10,  "y":265+y_trans},
          {"x":10,  "y":310+y_trans},
        ];

         var lineData6=[
          {"x":40,   "y":245+y_trans},
          {"x":10,  "y":245+y_trans},
          {"x":10,  "y":175+y_trans},
        ];

        //线生成器
        var lineFunction = d3.line()
            .x(function(d){return d.x;})
            .y(function(d){return d.y;})
                        //  .interpolate("linear");


        //把path扔到容器中-- lineData和lineFunction，并给d赋属性
        legend.append("path")
            .attr("d",lineFunction(lineData1))
            .attr("stroke","black")
            .attr("stroke-width",1.3)
            .attr("fill","none");
        legend.append("path")
            .attr("d",lineFunction(lineData2))
            .attr("stroke","black")
            .attr("stroke-width",1.3)
            .attr("fill","none");
        legend.append("path")
            .attr("d",lineFunction(lineData3))
            .attr("stroke","black")
            .attr("stroke-width",1.3)
            .attr("fill","none");
        legend.append("path")
            .attr("d",lineFunction(lineData4))
            .attr("stroke","black")
            .attr("stroke-width",1.3)
            .attr("fill","none");

        legend.append("path")
            .attr("d",lineFunction(lineData5))
            .attr("stroke","black")
            .attr("stroke-width",1.3)
            .attr("fill","none");

        legend.append("path")
            .attr("d",lineFunction(lineData6))
            .attr("stroke","black")
            .attr("stroke-width",1.3)
            .attr("fill","none");

        legend
          .attr("transform","translate(20 ,20)scale(0.85)")

        let transform;
        // const circle_r = 13;
        // const arc_scale=1.5;
        const arc_scale=2;
        const zoom = d3.zoom().on("zoom", e => {
          g.attr("transform", (transform = e.transform));
          g.style("stroke-width", 3 / Math.sqrt(transform.k));
          points.attr("r", function(d) { return zScale(zValue(d)) / (Math.sqrt(transform.k))**1.8});
          points1.attr("r",  d=> pics(d)*2/ (Math.sqrt(transform.k))**1.8);
          points1
          .attr('cy',function(d){return yScale(yValue(d)) - (zScale(zValue(d))-5)/ (Math.sqrt(transform.k))**1.8})
          // .attr('cx',function(d){return xScale(xValue(d)) +5/ (Math.sqrt(transform.k))**1.8})
          // points.attr("r", 13 / (Math.sqrt(transform.k))**2.3);
          arc_1.attr("transform",function(d) { return "translate(" + -xScale(xValue(d)) + "," + yScale(yValue(d)) + ")scale(" +arc_scale / (Math.sqrt(transform.k))**1.8+")"; });
          arc_2.attr("transform",function(d) { return "translate(" + -xScale(xValue(d)) + "," + yScale(yValue(d)) + ")scale(" +arc_scale / (Math.sqrt(transform.k))**1.8+")"; });
          arc_3.attr("transform",function(d) { return "translate(" + -xScale(xValue(d)) + "," + yScale(yValue(d)) + ")scale(" +arc_scale / (Math.sqrt(transform.k))**1.8+")"; });
          arc_4.attr("transform",function(d) { return "translate(" + -xScale(xValue(d)) + "," + yScale(yValue(d)) + ")scale(" +arc_scale / (Math.sqrt(transform.k))**1.8+")"; });
          // thumb_select.attr("transform", "scale(" + 10 / (Math.sqrt(transform.k))**1.8+ ")")
          // thumb_select.attr("transform",function(d) { return "translate(" + ((10 * Math.sqrt(transform.k) * xScale(xValue(d))/ xScale(xValue(d)))) + "," + ((237 * Math.sqrt(transform.k) * yScale(yValue(d))/ yScale(yValue(d)))) + ")scale(" + 1/ (Math.sqrt(transform.k))**2.8+")"; })
          // thumb_select.attr("transform",function(d) { return "translate(" + Math.sqrt(transform.k) + "," + Math.sqrt(transform.k) + ")scale(" + 1/ (Math.sqrt(transform.k))**2.8+")"; })


        });

        // Range
  // var sliderRange = sliderBottom()
  //   .min(1)
  //   .max(10)
  //   .width(300)
  //   .tickFormat(d3.format('.2%'))
  //   .ticks(5)
  //   .default([0.015, 0.02])
  //   .fill('#2196f3')
  //   .on('onchange', val => {
  //     d3.select('p#value-range').text(val.map(d3.format('.2%')).join('-'));
  //   });
  //
  // var gRange = select('div#slider-range')
  //   .append('svg')
  //   .attr('width', 500)
  //   .attr('height', 100)
  //   .append('g')
  //   .attr('transform', 'translate(30,30)');
  //
  // gRange.call(sliderRange);
  //
  // d3.select('p#value-range').text(
  //   sliderRange
  //     .value()
  //     .map(d3.format('.2%'))
  //     .join('-')
  // );


        class Thumbnail {
  constructor (parentContainer, body, operator, width) {
    this.body = body
    this.operator = operator
    this.width = width | 160 // 缩略图canvas的大小
    this.parentContainer = parentContainer // 父级容器
    this.container = svg
    this.viewportCvs = document.createElement('canvas') // 节点canvas
    this.handleCvs = document.createElement('canvas') // 操作canvas
    this.scale = {// 缩放因子
      k: 1, x: 0, y: 0
    }
    this.thumbScale = 5 // 缩略图对应主屏幕移动的比例
    this.drag = false // 是否拖拽的标记
    this.startPoint = void 0 // 开始拖拽的点
    this.range = void 0 // 节点和屏幕边界并集[minX, minY, maxX, maxY]
    this.nodeRange = void 0 // 节点边界[minX, minY, maxX, maxY]
    this.screenRange = void 0 // 屏幕边界[minX, minY, maxX, maxY]
    this.viewCenter = void 0 // 屏幕中心点[缩略图]
    this.isDragged = false // 是否移动鼠标位置:用以防止mousemove后触发click
    this.init()
  }
  init () {
    this.container.className = 'thumbnail'
    this.container.style.cssText = `
        position: absolute;
        left: 5px;
        bottom: 5px;
        padding: 3px;
        border: 1px solid #ddd;
        background-color: #fff;`
    this.container.style.width = this.container.style.height = `${this.width + 8}px`
    const temp = document.createElement('div')
    temp.style.cssText = `
        position: relative;
        width: 100%;
        height: 100%;
        user-select: none;
        -webkit-user-drag: none;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);`
    const canvasStyle = `
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        width: 100%;
        height: 100%`
    this.viewportCvs.style.cssText = this.handleCvs.style.cssText = canvasStyle
    this.parentContainer.appendChild(this.container)
    this.container.appendChild(temp)
    temp.appendChild(this.viewportCvs)
    temp.appendChild(this.handleCvs)
    // 容器大小
    this.viewportCvs.width = this.handleCvs.width = this.viewportCvs.height = this.handleCvs.height = this.width
    // 注册拖拽事件
    d3.select(this.handleCvs)
      .on('click', () => this.click())
      .on('mousedown', () => this.mousedown())
      // 改变d3注册为body注册, 这样保证移出屏幕仍然可以拖拽
    document.body.addEventListener('mousemove', evt => this.mousemove(evt))
    document.body.addEventListener('mouseup', evt => this.mouseup())
    // 绘制
    this.redraw()
  }

  /**
   * 只绘制节点
   */
  redraw () {
    if (this.body.data === undefined) {
      return
    }
    // 清空缩略图主画布
    this.operator.clearGraph(this.viewportCvs)
    // 清空缩略图矩形区域
    this.operator.clearGraph(this.handleCvs)
    // 遍历渲染节点和连线
    const nodes = this.body.transformData.nodes
    if (nodes.length > 0) {
      const ctx = this.viewportCvs.getContext('2d')
      // 获取节点边界
      const range = this.nodeRange = this.operator.getRange()
      // 获取屏幕边界
      const cBBox = this.body.nodeContainer.getBoundingClientRect()
      const screenRange = this.screenRange = {
        minX: this.operator.transformX(0),
        minY: this.operator.transformY(0),
        maxX: this.operator.transformX(cBBox.width),
        maxY: this.operator.transformY(cBBox.height)
      }
      let ax, ay, ix, iy
      // 如果节点全部显示在屏幕内
      if (this.body.transformData.nodes.length === this.body.transformData.viewNodes.length) {
        ax = range.maxX
        ay = range.maxY
        ix = range.minX
        iy = range.minY
      } else { // 存在节点不在屏幕内
        ax = Math.max(range.maxX, screenRange.maxX)
        ay = Math.max(range.maxY, screenRange.maxY)
        ix = Math.min(range.minX, screenRange.minX)
        iy = Math.min(range.minY, screenRange.minY)
      }
      // 记录整个范围的边界
      this.range = {
        minX: ix, maxX: ax, minY: iy, maxY: ay
      }
      const width = ax - ix
      const height = ay - iy
      const refer = Math.max(width, height)
      const scale = this.scale
      scale.k = this.width / refer
      ctx.save()
      // 缩放
      ctx.scale(scale.k, scale.k)
      if (width === height) {
        scale.x = -ix
        scale.y = -iy
      } else if (width > height) {
        scale.x = -ix
        scale.y = -iy + (width - height) / 2
      } else {
        scale.x = -ix + (height - width) / 2
        scale.y = -iy
      }
      ctx.translate(scale.x, scale.y)
      // 遍历绘制节点
      for (const node of nodes) {
        if (!isNaN(node.x) && !isNaN(node.y)) {
          node.drawThumbnail(ctx)
        }
      }
      // 存在部分节点不在屏幕中则绘制对应矩形
      if (this.body.transformData.nodes.length > 0 && this.body.transformData.nodes.length > this.body.transformData.viewNodes.length) {
        this.drawThumbnailViewRect(width, height)
      }
      this.viewCenter = {
        x: (this.screenRange.maxX + this.screenRange.minX) / 2, y: (this.screenRange.maxY + this.screenRange.minY) / 2
      }
      ctx.restore()
    }
  }

  /**
   * 绘制缩略图的矩形
   * @param {Number} width 宽度
   * @param {Number} height 高度
   */
  drawThumbnailViewRect (width, height) {
    const ctx = this.handleCvs.getContext('2d')
    const scale = this.scale
    // 获取矩形位置
    const x = this.screenRange.minX
    const y = this.screenRange.minY
    const w = this.screenRange.maxX - this.screenRange.minX
    const h = this.screenRange.maxY - this.screenRange.minY
    // 绘制矩形区域
    ctx.save()
    ctx.beginPath()
    ctx.scale(scale.k, scale.k)
    ctx.translate(scale.x, scale.y)
    ctx.lineWidth = 1 / scale.k
    ctx.strokeStyle = '#409EFF'
    ctx.rect(x, y, w, h)
    ctx.stroke()
    ctx.restore()
  }

  /**
   * 点击事件
   */
  click () {
    if (this.isDragged) {
      this.isDragged = false
      return
    }
    const [x, y] = d3.mouse(this.handleCvs)
    let tx, ty
    if (this.body.transformData.nodes.length > this.body.transformData.viewNodes.length) { // 可视屏幕中心
      const { minX, maxX, minY, maxY } = this.range
      const rangeCenter = {
        x: (minX + maxX) / 2,
        y: (minY + maxY) / 2
      }
      tx = (this.viewCenter.x - rangeCenter.x) * this.scale.k + this.width / 2
      ty = (this.viewCenter.y - rangeCenter.y) * this.scale.k + this.width / 2
    } else { // 缩略图中心
      tx = ty = this.width / 2
    }
    // 向量偏移量
    const vector = {
      x: x - tx,
      y: y - ty
    }
    // 赋值偏移量并重绘主画布
    const bs = this.body.scale
    bs.x -= this.thumbScale * vector.x
    bs.y -= this.thumbScale * vector.y
    this.body.emitter.emit('redraw')
    this.startPoint = {
      x, y
    }
  }

  /**
   * 鼠标按下:记录初始位置
   */
  mousedown () {
    this.drag = true
    const [x, y] = d3.mouse(this.handleCvs)
    this.startPoint = {
      x, y
    }
  }

  /**
   * 鼠标移动:根据相对偏移计算主画布的偏移量, 触发主画布的绘制
   */
  mousemove (evt) {
    if (this.drag) {
      const bounding = this.handleCvs.getBoundingClientRect()
      // const [x, y] = d3.mouse(this.handleCvs)
      const [x, y] = [evt.pageX - bounding.left, evt.pageY - bounding.top]
      // 计算偏移量
      const vector = {
        x: x - this.startPoint.x,
        y: y - this.startPoint.y
      }
      // 重绘
      const bs = this.body.scale
      bs.x -= this.thumbScale * vector.x
      bs.y -= this.thumbScale * vector.y
      this.body.emitter.emit('redraw')
      // 重新记录拖拽初始位置
      this.startPoint = {
        x, y
      }
      this.isDragged = true
    }
  }

  /**
   * 鼠标抬起
   */
  mouseup () {
    this.drag = false
    this.startPoint = void 0
  }

  /**
   * 打开缩略图
   */
  open () {
    this.container.style.display = 'block'
  }

  /**
   * 关闭缩略图
   */
  close () {
    this.container.style.display = 'none'
  }
}


        return svg
          .call(zoom)
          .call(zoom.transform, d3.zoomIdentity)
          .on("pointermove", event => {
            const p = transform.invert(d3.pointer(event));
            const i = delaunay.find(...p);
            points.classed("highlighted", (_, j) => i === j);
            d3.select(points.nodes()[i]).raise();
          })
          .node();

    },

    setDimensionReduction(response){
      // console.log(response.data)
    }
  },
  mounted() {
    //设置气泡图数据的通信方法 net-service.js可看详情
    this.$net.sendMiddleLevelData(this.content_id,this.setBubbleData)
    //同步Overview微博id数据更新到content_id
    PipeService.$on("middleGetValue",(val)=>{
      this.content_id = val
    })
  },
  watch:{
    //如果content_id有更新 则重新渲染气泡图
    content_id: function (){
      this.$net.sendMiddleLevelData(this.content_id,this.setBubbleData)
      if (this.content_id.length<2&&this.content_id.length>0){
        PipeService.$emit('middleByValue', this.content_id[0])
      } else {
        PipeService.$emit('middleByValue', this.content_id[0])
        PipeService.$emit('middleByValue', this.content_id[1])
      }
    }
  }


}


</script>

<style scoped>
#middle{
  border-radius:5px;
  background-color: white;
  height: 33%;
  width: 100%;
}
svg{
  height: 100%;
  width: 100%;
}
</style>
