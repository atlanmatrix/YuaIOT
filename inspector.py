

def inspect_file(f_name):
    try:
        fd = open(f_name, 'r')
        data = fd.read()
        for i in data.split('\n'):
            print(i)
    except:
        print('Open file failed')

