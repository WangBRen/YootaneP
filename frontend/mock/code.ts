import { Request, Response } from 'express';

const waitTime = (time: number = 100) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(true);
      }, time);
    });
  };

export default{
    'POST /question': async (req: Request, res: Response) => {
        const { code } = req.body;
        await waitTime(2000);
        if (code === '') {
          res.send({
            status: 'error'
          });
          return;
        }
    
        res.send({
          status: 'success',
        });
      },
}