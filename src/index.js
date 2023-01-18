// 项目启动
import Vue from "vue";
import App from "./App";

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import './assets/css/style.css'

//引入公共request方法
import NET from './assets/js/net-service.js';
Vue.prototype.$net=NET;

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

new Vue({
    render: (h) => h(App),
}).$mount("#app"); // 渲染挂载
