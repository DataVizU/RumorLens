<template>
  <div>
    <button v-on:click="loadMore">click me</button>
	<ul>
		<li v-for="(item, index) in listArr" :key="index">
			<a href="">{{ index }} 《{{ item.name }}》</a>
		</li>
	</ul>
  </div>
</template>
<script>
import Thumbnail from './Middle'

let mock = require('../mock'); // 模拟请求

export default {
	data: () => ({
		listArr: [],
		page: 1,
	}),
	created() {
		this.loadList();
	},
	methods: {
		loadList(page) {
			const {data, success} = mock.data;
			if (this.page > 1) {
				console.log("page is:", this.page);
				return this.listArr = this.listArr.concat(data);
			}
			this.listArr = data;
		},
		loadMore() {
			this.loadList(this.page++);
		},
    //     // 初始化
    // initializeGraph () {
    //   const option = {}
    //   let dom = document.querySelector('#graph')
    //   const bounding = dom.getBoundingClientRect()
    //   // 画布
    //   this.graph = new Graph(dom, {nodes: [], edges: []}, bounding.width, bounding.height, option)
    //   // 缩略图
    //   this.graph.thumbnail = new Thumbnail(dom, this.graph.body, this.graph.operator)
    // },
    //
    // // 注册事件
    // initializeEvent () {
    //   const canvas = this.graph.body.nodeContainer
    //   d3.select(canvas)
    //     .on('click', () => this.graph.body.emitter.emit('tap', d3.mouse(canvas), d3.event, params => {
    //       console.log('单击')
    //       this.clickEvent(d3.mouse(canvas), d3.event, params)
    //     }))
    //     .on('contextmenu', () => this.graph.body.emitter.emit('tap', d3.mouse(canvas), d3.event, params => {
    //       // 阻止默认右键事件
    //       d3.event.returnValue = false
    //       console.log('右键')
    //     }))
    //     .on('dblclick', () => this.graph.body.emitter.emit('tap', d3.mouse(canvas), d3.event, params => {
    //       console.log('双击')
    //     }))
    //   // 注册窗口resize事件
    //   d3.select(window).on('resize', () => {
    //     this.graph.body.emitter.emit('resize', document.body.clientWidth, document.body.clientHeight)
    //   })
    // },
    // /** 加载数据 */
    // loadData () {
    //   // 延时
    //   setTimeout(() => this.graph.setData(defaultDatas))
    // },
    // /** 点击事件 */
    // clickEvent (coordinates, evt, obj) {
    //   if (obj && obj instanceof Node) {
    //     const oldStatus = obj.status
    //     obj.status = oldStatus === Status.selection ? Status.default : Status.selection
    //     this.graph.body.emitter.emit('click.node', event, obj)
    //   }
    // }
	},
};
</script>

<style>
button {
	display: block;
	margin: 0 auto;
	line-height: 30px;
	border: 1px solid #ddd;
	color: #41b883;
}
a {
	color: #35495e;
	font-size: 16px;
	text-decoration: none;
}
ul {
	margin-bottom: 60px;
	padding: 20px;
}
li {
	line-height: 32px;
	border-bottom: 1px solid #ddd;
	padding: 0 10px;
	text-align: left;
	list-style: none;
}
b {
	font-size: 12px;
	color: #35495e;
}
.loading {
  	text-align: center;
}
</style>
