# script2http
> 以http方式执行脚本文件

### 执行当前项目脚本

1. 新建scripts文件夹，放入脚本文件somescy.sh，支持'','.sh','.py','.js'结尾

2. 启动服务`export FLASK_APP=main FLASK_ENV=development && flask run --host=0.0.0.0`

3. 访问
`http://localhost:5000/somescy?input=xx&args=xxx&timeout=120`
调用scripts/somescy.sh脚本文件，input传入脚本的stdin，args作为脚本参数(,隔开)，timeout超时时间

### docker方式

注意：当前仅为python3环境，可以通过Dockerfile FROM更改
```shell
docker build -t script2http .
docker run -d --name script2http --restart=unless-stopped -p 9000:5000 -v $PWD/scripts:/app/scripts script2http
```
