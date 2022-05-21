# script2http

以http方式执行脚本

访问
`http://ip:port/scriptname?input=xx&args=xxx&timeout=120`
调用scripts/scriptname脚本文件，input传入脚本的stdin，args作为脚本参数(,隔开)，timeout超时时间

```shell
docker build -t script2http .
docker run -d --name script2http --restart=unless-stopped -p 9000:5000 -v $PWD/scripts:/app/scripts script2http
```
