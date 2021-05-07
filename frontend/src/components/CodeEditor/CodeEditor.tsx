import React from 'react';
import { Button, notification, Card } from 'antd';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import { sendCode } from '@/services/code';
import { UnControlled as CodeMirror } from 'react-codemirror2';
import 'codemirror/lib/codemirror.css'; // 主题风格

import 'codemirror/theme/solarized.css'; // 代码模式，clike是包含java,c++等模式的
import 'codemirror/theme/seti.css'; // 代码模式，clike是包含java,c++等模式的

import 'codemirror/mode/clike/clike';

export default class CodeEditor extends React.Component {
  state = {
    value: 'test',
  };

  handleChange = (value) => {
    console.log(value)
    this.setState({
      value,
    });
  };

  prompt = async() => {
    const msg = await sendCode(this.state.value);
    notification.open({
      message: '发送指令给后端:',
      description: <span dangerouslySetInnerHTML={{ __html: this.state.value }} />,
    });
  };

  render() {
    return (
      <Card title="代码编辑器">
        {/* <ReactQuill value={this.state.value} onChange={this.handleChange} />
        <Button style={{ marginTop: 16 }} onClick={this.prompt}>
          Prompt
        </Button> */}
            <CodeMirror // value={record.data}
              options={{
                mode: 'groovy',
                theme: 'seti',
                lineNumbers: true,
              }} // 这个必须加上，否则在一些情况下，第二次打开就会有问题
              // onBeforeChange={(editor, data, value) => {
              //   console.log('onBeforeChange fresh');
              //   console.log(JSON.stringify(data));
              //   console.log(JSON.stringify(value));
              // }}
              value={this.state.value} 
              onChange={(editor, data, value) => this.handleChange(value)}
              // onChange={(editor, data, value) => {
              //   console.log(JSON.stringify(data));
              //   console.log(JSON.stringify(value));
              // }}
              /* HERE: pick out only the value. and might as well get name. */
            />
            <Button 
              style={{
                margin: 12,
              }}
              type="primary" onClick={this.prompt}>提交代码</Button>
      </Card>
    );
  }
}