# CalDAV ICS

同步 CalDAV 日历（特别是 [飞书](https://www.feishu.cn/) 导出的日历）到可订阅的 ICS 文件。

## 安装

配置如下环境变量：

```bash
PORT=<服务端口号>
CALDAV_SERVER=https://caldav.feishu.cn
CALDAV_USERNAME=<飞书 CalDAV 用户名>
CALDAV_PASSWORD=<飞书 CalDAV 密码>
PASSWORD=<用于保护 ICS 文件的密码>
```

启动服务器：

```bash
uv run caldav_ics
```

然后访问 `http://localhost:<PORT>/calendar/<日历名称>?key=<PASSWORD>` 即可获得 ICS 文件，此链接可以在 Google 日历等应用中订阅。此处的日历名称是在飞书中显示的日历名称。

## 鸣谢

实现参考了 [nemofq/caldav-to-ics](https://github.com/nemofq/caldav-to-ics) 和 [Xuanwo 的博客](https://xuanwo.io/reports/2023-35/)。
