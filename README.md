# calibre-chinese-dirs
calibre 中文目录名读写问题解决
现有版本支持calibre 3.48 windows 7 版本的目录修改

# 操作流程

- 到官方下载源码,到[官方网站](https://calibre-ebook.com/zh_CN/download_windows) 找到[3.48 版本](https://download.calibre-ebook.com/3.48.0/)
- 下载source code
- 找到源码文件**calibre-3.48.0/src/calibre/db/backend.py**
- 注释掉代码
- 在源文件中找到 construct_path_name 方法，注释掉以下两行
  ```python
     author = ascii_filename(author)[:l]
     title  = ascii_filename(title.lstrip())[:l].rstrip()
  
  ```
  继续寻找 construct_file_name 方法，注释掉以下两行:
  ```python
    author = ascii_filename(author)[:l]
    title  = ascii_filename(title.lstrip())[:l].rstrip()
  ```

- 使用python2.7 编译该文件，最好在windows 环境下
  ```python
  c:\Python27\python.exe -O -m py_compile src\calibre\db\backend.py
  
  ```

- 到安装calibre 的目录下，备份pylib.zip 目录，默认情况下在 C:\Program Files\Calibre2\app\pylib.zip 

- 将这个pylib.zip 放到这个代码所在目录里面
- 运行 extra.py
  ```python
  c:\Python27\python.exe extra.py
  
  ```
- 这个时候，就会将这个pylib.zip 解压缩，并且创建一个目录
- 这个时候，将编译好的新的backend.pyo 文件，拷贝带pylib\calibre\db\, 替换掉原来的backend.pyo
- 执行zipc.py 用来重新打包,生成的文件是pylib2.zip
```python

  c:\Python27\python.exe zipc.py
  
```
- 将新的pylib2.zip 拷贝到原来zip 所在目录,改名pylib.zip 替换掉原来的zip 文件
- 启动calibre 就好了
