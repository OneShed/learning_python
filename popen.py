import subprocess

out, err = None, None

def _run(cmd):
    global out, err
    p = subprocess.Popen(cmd.split(' '), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()

    if p.returncode == 0:
        out = stdout.splitlines()
        return True
    else:
        err  = stderr.splitlines()
        return False

if _run('ls'):
    print('OK')
    print("out: %s" % out)
else:
    print('NOK')
    print("err : %s" % err)