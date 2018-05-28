import subprocess


reader_names = ['Вася', 'Маша', 'Зина', 'Коля', 'Оля']

writer_names = ['Миша', 'Петя', 'Юля']

for name in reader_names:
    subprocess.Popen(["start", "cmd", "/k", "python client_starter.py -r -n %s" % name], shell=True)

for name in writer_names:
    subprocess.Popen(["start", "cmd", "/k", "python client_starter.py -w -n %s" % name], shell=True)
