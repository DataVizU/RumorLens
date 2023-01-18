import axios from 'axios';
// import qs from 'qs';

const devApiUrl = '';

const GET_REQUEST = 'get';
const POST_REQUEST = 'post';

function request(url, params, type, callback) {
    let func;
    if (type === GET_REQUEST) {
        func = axios.get;
    } else if (type === POST_REQUEST) {
        func = axios.post;
    }

    func(url, params).then((response) => {
        if (response.status === 200) {
            callback(response);
        } else {
            console.error(response);
        }
    })
    .catch((error) => {
        console.log(error);
    });
}

function sendOverviewData(data_type,callback){
  const url = `${devApiUrl}/overview/${data_type}`
  const params = { data_type }
  request(url, params, GET_REQUEST, callback)
}

function sendMiddleLevelData(content_id,callback){
  const url = `${devApiUrl}/middle`
  const bodyFormData = new FormData();
  content_id.forEach((item) => {
    bodyFormData.append('content_id[]', item);
  });
  axios.post(url, bodyFormData)
    .then((response) => {callback(response);})
    .catch((error) => {
        console.error(error);
    });
}

function sendRiverKeywords(content_id,callback){
  const url = `${devApiUrl}/overview/theme-river`
  const bodyFormData = new FormData();
  content_id.forEach((item) => {
    bodyFormData.append('content_id[]', item);
  });
  axios.post(url, bodyFormData)
    .then((response) => {callback(response);})
    .catch((error) => {
        console.error(error);
    });
}

function sendCommunicationList(userId,callback){
  const url = `${devApiUrl}/communication/${userId}`;
  const params = { userId }
  request(url,params,GET_REQUEST,callback)
}


function sendTreeMap(userId,callback){
  const url = `${devApiUrl}/treemap/${userId}`;
  const params = { userId }
  request(url,params,GET_REQUEST,callback)
}

export default {
  sendOverviewData,
  sendRiverKeywords,
  sendMiddleLevelData,
  sendCommunicationList,
  sendTreeMap
};

