import { request } from 'umi';

export async function sendCode(code: string) {
    return request('/question', {
        method: 'POST',
        data: {code: code},
      });
  }