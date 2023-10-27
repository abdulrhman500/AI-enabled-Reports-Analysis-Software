import axios from 'axios';
import Cookies from 'js-cookie';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;
const getCookie = () => Cookies.get('csrftoken')
export const http = axios.create({
    baseURL: "http://localhost:8000",
    headers: {'X-CSRFToken': getCookie}
  });

export const api = ({ method, headers, data, url }) => {
  let cookie = Cookies.get('csrftoken')
  if(method =='get') return http.request({method,url,headers:{'X-CSRFToken': cookie,...headers}})
  return http.request({method,url,data,headers:{'X-CSRFToken': Cookies.get('csrftoken'),...headers}})
}