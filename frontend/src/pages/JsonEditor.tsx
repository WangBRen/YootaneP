import React from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import Editor from '@/pages/CodeEditor/JsonEditor';
import 'jsoneditor-react/es/editor.min.css';
import 'codemirror/lib/codemirror.css'; // 主题风格

import 'codemirror/theme/solarized.css'; // 代码模式，clike是包含java,c++等模式的

import 'codemirror/mode/clike/clike';

import 'jsoneditor-react/es/editor.min.css';

export default (): React.ReactNode => {
  return (
    <PageContainer>
        <Editor
        />
    </PageContainer>
  );
};
