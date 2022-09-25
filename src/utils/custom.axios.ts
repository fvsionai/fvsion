// https://blog.clairvoyantsoft.com/intercepting-requests-responses-using-axios-df498b6cab62
import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
// const axios = require('axios');
import { API_library } from "./index";

// Step-1: Create a new Axios instance with a custom config.
// The timeout is set to 10s. If the request takes longer than
// that then the request will be aborted.
const customAxios = axios.create({
  baseURL: API_library.root,
  timeout: 10000,
  //   headers: { "api-key": "eyJz-CI6Ikp-4pWY-lhdCI6" },
});

// // Step-2: Create request, response & error handlers
// const requestHandler = (request: AxiosRequestConfig<any>) => {
//   // Token will be dynamic so we can use any app-specific way to always
//   // fetch the new token before making the call
//   request.headers!.Authorization =
//     "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTIzNDU2Nzg5IiwibmFtZSI6IlNhbXBsZSIsImlhdCI6MTUxNjIzODIzfQ.ZEBwz4pWYGqgFJc6DIi7HdTN0z5Pfs4Lcv4ZNwMr1rs";

//   return request;
// };

// const responseHandler = (response: AxiosResponse<any, any>) => {
//   if (response.status === 401) {
//     // TODO
//     // window.location = '/login';
//   }

//   return response;
// };

// const errorHandler = (error: any) => {
//   return Promise.reject(error);
// };

// // Step-3: Configure/make use of request & response interceptors from Axios
// // Note: You can create one method say configureInterceptors, add below in that,
// // export and call it in an init function of the application/page.
// customAxios.interceptors.request.use(
//   (request) => requestHandler(request),
//   (error) => errorHandler(error)
// );

// customAxios.interceptors.response.use(
//   (response) => responseHandler(response),
//   (error) => errorHandler(error)
// );
// customInterceptor set in JobStatus

// Step-4: Export the newly created Axios instance to be used in different locations.
export default customAxios;
