// import { request } from 'umi';
import { extend } from "umi-request";

const request = extend({
  // timeout: 1000,
  headers: {
    "Content-Type": "application/json"
  },
  // params: {
  //   token: "xxx" // 所有请求默认带上 token 参数
  // },
  errorHandler: function(error) {
    /* 异常处理 */
  }
});
export async function sendCode(code: object) {
  request
    .post("http://localhost:8002/iop/", {
      data: code
    })
    .then(function(response) {
      console.log(response);
      return response
    })
    .catch(function(error) {
      console.log(error);
    });
  }

  export async function sendTask(code: object) {
    request
      .post("http://localhost:8002/question_iop/", {
        data: code
      })
      .then(function(response) {
        console.log(response);
        return response
      })
      .catch(function(error) {
        console.log(error);
      });
    }

  export async function getTask(id: string) {
    request
      .get(`http://localhost:8002/question_iop/${id}`)
      .then(function(response) {
        console.log(response);
        return response
      })
      .catch(function(error) {
        console.log(error);
      });
    }