export default [
  {
    path: '/user',
    layout: false,
    routes: [
      {
        path: '/user',
        routes: [
          {
            name: 'login',
            path: '/user/login',
            component: './User/login',
          },
        ],
      },
    ],
  },
  {
    path: '/welcome',
    name: '操作台',
    icon: 'smile',
    component: './Welcome',
  },
  {
    name: 'Bro',
    icon: 'smile',
    path: '/bros',
    component: './bros',
  },
  {
    path: '/jsoneditor',
    name: '编辑器',
    icon: 'smile',
    component: './JsonEditor',
  },
  {
    path: '/admin',
    name: 'admin',
    icon: 'crown',
    access: 'canAdmin',
    component: './Admin',
    routes: [
      {
        path: '/admin/sub-page',
        name: 'sub-page',
        icon: 'smile',
        component: './Welcome',
      },
    ],
  },
  {
    name: '历史任务',
    icon: 'table',
    path: '/list',
    component: './TableList',
  },
  {
    path: '/',
    redirect: '/welcome',
  },
  {
    name: '个人设置',
    icon: 'smile',
    path: '/accountsettings',
    component: './AccountSettings',
  },
  {
    component: './404',
  },
];
