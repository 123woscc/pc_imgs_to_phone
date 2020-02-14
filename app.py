import os
import sys
from urllib.parse import quote, unquote

from flask import Flask, render_template, send_file


def get_all_path(dirname):
    result = []
    for root, dirs, _ in os.walk(dirname):
        for dir in dirs:
            path = os.path.join(root, dir)
            result.append(path)
    return result


app = Flask(__name__)
# 获取根目录
app.config['DIRPATH'] = sys.argv[1]


# 获取文件夹目录
@app.route('/')
def index():
    dirpath = app.config['DIRPATH']
    paths = get_all_path(dirpath)
    paths = [quote(x, safe='') for x in paths]
    return render_template('index.html', paths=paths)


# 显示图片
@app.route('/view/<path>')
def view(path):
    img_check = ['.jpg', '.png']
    imgs = []
    files = os.listdir(unquote(path))
    for file in files:
        if os.path.splitext(file)[1] in img_check:
            imgs.append(file)
    imgs = sorted(imgs)
    imgs = [os.path.join(path, img) for img in imgs]
    imgs = [quote(x, safe='') for x in imgs]
    return render_template('view.html', imgs=imgs)


# 返回图片的真实地址
@app.route('/show/<path:path>')
def show(path):
    return send_file(unquote(unquote(path)), mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
