import React from 'react';
import { useEffect } from 'react';
import { useState } from 'react';
import { extend } from "umi-request";
import  { Table, Button, Card} from "antd"

const dataSource = [
  {
    key: '1',
    name: '胡彦斌',
    age: 32,
    address: '西湖区湖底公园1号',
    gender: '男',
  },
  {
    key: '2',
    name: '胡彦祖',
    age: 42,
    address: '西湖区湖底公园1号',
  },
];

const columns = [
  {
    title: '姓名',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '年龄',
    dataIndex: 'age',
    key: 'age',
  },
  {
    title: '住址',
    dataIndex: 'address',
    key: 'address',
  },
  {
    title: '性别',
    dataIndex: 'gender',
    key: 'gender',
  },
];

const request = extend({
  // timeout: 1000,
  headers: {
    "Content-Type": "application/json"
  },
  // params: {
  //   token: "xxx" // 所有请求默认带上 token 参数
  // },
});

export default () => {
  const [dir, setDir] = useState([])
  const [data, setData] = useState(dataSource)

  useEffect(()=>{
    async function getDir(){
    request.get("http://localhost:8002/path/").then((resp)=>{
    console.log(resp)
    setDir(resp)
})}

    getDir()
  },[])
  return (
    <>
    <Button onClick={()=>{setData([])}}>清空</Button>
      <Table bordered={true} dataSource={data} columns={columns} />
    <div>
      {dir.map((item)=><Card title="card" headStyle={{backgroundColor: 'gray'}}>{item}</Card>)}
    </div>
    </>
  );
};
