def initRuntimeEnvironment(startup_script):
    """初始化运行环境。startup_script: 启动脚本路径"""
    import os
    import sys
    import site

    # 重定向输出流到控制台窗口
    try:
        fd = os.open('CONOUT$', os.O_RDWR | os.O_BINARY)
        fp = os.fdopen(fd, 'w')
        sys.stdout = fp
        sys.stderr = fp
    except Exception as e:
        fp = open(os.devnull, 'w')
        sys.stdout = fp
        sys.stderr = fp

    # 定义一个最简单的消息弹窗
    def MessageBox(msg, info='Message'):
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, str(msg), str(info), 0)
        return 0
    os.MessageBox = MessageBox

    # 初始化工作目录和Python搜索路径
    script = os.path.abspath(startup_script)  # 启动脚本.py的路径
    home = os.path.dirname(script)  # 工作目录
    os.chdir(home)  # 重新设定工作目录（不在最顶层，而在UmiOCR-data文件夹下）
    for n in ['.', '.site-packages']:  # 将模块目录添加到 Python 搜索路径中
        path = os.path.abspath(os.path.join(home, n))
        if os.path.exists(path):
            site.addsitedir(path)

    # 初始化Qt搜索路径，采用相对路径，避免中文路径编码问题
    try:
        from PySide6.QtCore import QCoreApplication
        QCoreApplication.addLibraryPath('./.site-packages/PySide2/plugins')
    except Exception as e:
        print(e)
        os.MessageBox(f'addLibraryPath fail!\n\n{e}')
        os._exit(0)
    print('Init runtime environment complete!')


if __name__ == '__main__':
    initRuntimeEnvironment(__file__)  # 初始化运行环境
    import src.gui
    src.gui.gui()