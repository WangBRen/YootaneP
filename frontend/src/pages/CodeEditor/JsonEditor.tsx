import React from 'react';
import { Upload, message, Button, notification, Card } from 'antd';
import 'react-quill/dist/quill.snow.css';
import { sendCode } from '@/services/code';

import { JsonEditor as Editor } from 'jsoneditor-react';
import 'jsoneditor-react/es/editor.min.css';
import { UploadOutlined } from '@ant-design/icons';
import { values } from 'lodash';
import shortcut from "./shortcut.png"

export default class JsonEditor extends React.PureComponent {
  state = {
    value: {
      key1: 123,
      key2: "string"
    },
  };

  getFilds = () =>{
    const filedom = document.getElementById('file');
    filedom.click()
  }

  fileinputChange = (event) =>{
    const _this = this
    const fileData = event.target.files[0];
    console.log(fileData)               //其实是可以扩展到多文件上传的，不过我们就选第一个，也就是下标0
    if (!!fileData) {                              //!!是一个js的语法，表示后面的变量不是null/undefined/空串，实用写法。
      const reader = new FileReader();         //实例化一个FileReader对象
      reader.readAsText(fileData, "gbk");          //借助 FileReader 的方法，按照文本格式读入文件，第二个参数是编码方式（可空）
      reader.onload = function() {
        var tmp1 = this.result;    
        console.log(tmp1)
        const JsonValue = JSON.parse(tmp1);
        console.log(JsonValue)
          _this.setState({
            value: JsonValue
        }, ()=>{console.log(JsonValue)});
      }
  }
  }

  handleChange = (value) => {
    console.log(value)
    this.setState({
      value,
    });
  };

  prompt = async() => {
    // const msg = await sendCode(this.state.value);
    console.log(this.state.value)
    notification.open({
      message: '提交了代码:',
      description: <span dangerouslySetInnerHTML={{ __html: this.state.value }} />,
    });
  };

  clean = () => {
    // const msg = await sendCode(this.state.value);
    this.setState({
      value: {}
    })
  };

  render() {
    return (
      <Card title="编辑器">
        <Editor 
            key={Date.now()}
            value={this.state.value}
            onChange={this.handleChange}
        />
        <input id="file" type="file" accept=".json"
         	style={{ display:"none", }}
         	onChange={this.fileinputChange}
        />
        <Button style={{
                margin: 12,
              }} type="primary" onClick={this.getFilds}>读取文件</Button>
          <Button
              style={{
                margin: 12,
              }}
              type="primary" onClick={this.prompt}>保存文件</Button>
              <Button
              style={{
                margin: 12,
              }}
              type="primary" onClick={this.clean}>清空</Button>
              <img style={{
                margin: 12,
                width: 800
              }} src={shortcut}/>
       </Card>
    );
  }
}