import axios from "axios";
import baseUrl from "@/api/baseUrl";
import { ElMessage } from "element-plus";
const service = axios.create({
  baseURL: baseUrl,
  timeout: 5000, // 发送请求后等待服务器响应的最大时间。如果服务器在指定的时间内没有响应，请求将被取消，并触发一个错误
}); // 自定义配置的新的axios
// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 可以加入某个特定的请求头、添加认证信息、或者对请求参数进行一些处理
    // 然后再将处理后的配置返回
    return config;
  },
  (error) => {
    // 对请求错误做些什么
    console.log(error);
    return Promise.reject(error);
  }
);
// 响应拦截器
service.interceptors.response.use(
  (response) => {
    // 对响应数据做点什么
    return response;
  },
  (error) => {
    if (error && error.response) {
      switch (error.response.status) {
        case 400:
          error.message = "请求错误";
          break;
        // case 401:
        //     error.message = "未授权，请登录";
        //     break;
        case 403:
          error.message = "拒绝访问";
          break;
        case 404:
          error.message = "请求地址出错";
          break;
        case 408:
          error.message = "请求超时";
          break;
        case 500:
          error.message = "服务器内部错误";
          break;
        case 501:
          error.message = "服务未实现";
          break;
        case 502:
          error.message = "网关错误";
          break;
        case 503:
          error.message = "服务不可用";
          break;
        case 504:
          error.message = "网关超时";
          break;
        case 505:
          error.message = "HTTP版本不受支持";
          break;
        default:
          break;
      }
      ElMessage({
        message: error.message,
        type: "error",
        duration: 5 * 1000,
      });
      return Promise.reject(error);
    }
  }
);
const get = function (url, options = {}) {
  // options默认值为空对象
  return new Promise((resolve, reject) => {
    service
      .get(url, options)
      .then((response) => {
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
};
const post = function (url, data, options = {}) {
  return new Promise((resolve, reject) => {
    service
      .post(url, data, options)
      .then((response) => {
        resolve(response.data);
      })
      .catch((error) => {
        reject(error);
      });
  });
};
export default {
  get,
  post,
};
