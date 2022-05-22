import time
from flask import Flask, Response, stream_with_context, request
import os.path
import subprocess

app = Flask(__name__)
# 目录
script_dirs = './scripts/'


# 获取完整的脚本路径
def get_full_path(path_name):
    # $开头直接执行bash命令
    if path_name.startswith('$'):
        return path_name[1:]
    ext_maps = ['', '.sh', '.py', '.js']
    for ext in ext_maps:
        full_path_name = script_dirs + path_name + ext
        if os.path.exists(full_path_name):
            return full_path_name
    return ''


# 执行脚本
def exec_script(script, args, ipt, timeout):
    # 记录下当前时间戳
    last_time = time.time()
    if args:
        script += ' ' + args.replace(',', ' ')
    sp = subprocess.Popen(script, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
    if ipt:
        sp.stdin.write(ipt)
        sp.stdin.close()
    # sp.communicate(None, timeout)
    while True:
        # 判断是否超时
        if time.time() - last_time > timeout:
            sp.kill()
            break
        line = sp.stdout.readline()
        if line:
            yield line
            yield '<br>'
        elif sp.poll() is not None:
            break
        time.sleep(0.1)


@app.route("/<path:script_path>")
def run_script(script_path):
    full_path = get_full_path(script_path)
    if full_path == '':
        return f'{script_path} is not exist'
    # 命令后的参数，以,分割
    args = request.args.get('args')
    # 交互式输入
    ipt = request.args.get('input')
    # 超时时长
    timeout = request.args.get('timeout') or 120
    # 流式返回
    return Response(stream_with_context(exec_script(full_path, args, ipt, int(timeout))))
