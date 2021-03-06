import sublime, sublime_plugin
import os, re, subprocess

DOCKER_NOT_INSTALLED_LINUX_MSG='''Docker is not installed. 

Install it to use SublimeDocker: open a Terminal and run
    'curl -sSL https://get.docker.com/ | sh'
'''

DOCKER_NOT_INSTALLED_OSX_MSG='''Docker is not installed. 

Install it to use SublimeDocker. Visit the following URL for installation instructions:

    https://docs.docker.com/en/latest/installation/
'''

DOCKER_NOT_RUNNING_LINUX_MSG='''Docker engine is not running. 

Start it to use SublimeDocker: open a Terminal and run 'sudo /etc/init.d/docker start'
'''
DOCKER_NOT_RUNNING_OSX_MSG='''Docker engine is not running. 

Start it to use SublimeDocker: open a Terminal and run 'boot2docker up'
'''

def isDockerInstalled():
    platform = sublime.platform()
    if platform == 'linux':
        return isDockerInstalledOnLinux()
    if platform == 'osx':
        return isDockerInstalledOnOSX()

def isDockerRunning():
    platform = sublime.platform()
    if platform == 'linux':
        return isDockerRunningOnLinux()
    if platform == 'osx':
        return isDockerRunningOnOSX()

def isDockerRunningOnLinux():
    """ Check is Docker daemon is running:
          We assume that the path to the daemon which appears in full ps output
          is of the form */bin/docker
    """
    if len(os.popen("ps -aef | grep '/bin/docker ' | grep -v grep").read().strip()) < 1:
        return False
    return True

def isDockerRunningOnOSX():
    if len(os.popen("ps -aef | grep 'boot2docker' | grep -v grep").read().strip()) < 1:
        return False
    try:
        os.environ["DOCKER_HOST"]
        os.environ["DOCKER_CERT_PATH"]
        os.environ["DOCKER_TLS_VERIFY"]
    except KeyError:
        boot2docker_init_cmd = subprocess.check_output(["/usr/local/bin/boot2docker", "shellinit"], stderr=None).strip()
        env = dict(re.findall(r'(\S+)=(".*?"|\S+)', boot2docker_init_cmd.decode()))
        for key,value in env.items():
            os.environ[key]=value
    return True

def isDockerInstalledOnLinux():
    if shutil.which('docker') != None :
        return True
    return False

def isDockerInsalledOnOSX():
    if shutil.which('docker') != None and shutil.which('boot2docker') != None :
        return True
    return False

def isNotRunningMessage():
    platform = sublime.platform()
    if platform == 'linux':
        isNotRunningMessageLinux()
    if platform == 'osx':
        isNotRunningMessageOSX()

def isNotInstalledMessageLinux():
    sublime.error_message(DOCKER_NOT_INSTALLED_LINUX_MSG)

def isNotInstalledMessageOSX():
    sublime.error_message(DOCKER_NOT_INSTALLED_OSX_MSG)

def isNotRunningMessageLinux():
    sublime.error_message(DOCKER_NOT_RUNNING_LINUX_MSG)        

def isNotRunningMessageOSX():
    sublime.error_message(DOCKER_NOT_RUNNING_OSX_MSG)

def isUnsupportedFileType(file_name):
    return False

def getFileFullPath():
    win = sublime.active_window()
    if win:
        view = win.active_view()
        if view and view.file_name():
            return view.file_name()
    return ""

def getFileDir():
    filefullpath = getFileFullPath()
    dirname = os.path.dirname(filefullpath)
    if os.path.exists(dirname):
        return dirname
    else:
        return ""

def getFileName():
    filefullpath = getFileFullPath()
    return os.path.basename(filefullpath)

def getView():
    win = sublime.active_window()
    return win.active_view()

def getCommand():
    platform = sublime.platform()
    if platform == 'linux':
        return "docker"
    if platform == 'osx':
        return "/usr/local/bin/docker"