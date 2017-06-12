from subprocess import Popen, PIPE

p = Popen(['python', 'mailing_lists_people.py'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
output = p.stdout.read()
p.stdin.write(raw_input())

p = Popen(['python', 'messages.py'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
output = p.stdout.read()
p.stdin.write(raw_input())


p = Popen(['python', 'people.py'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
output = p.stdout.read()
p.stdin.write(raw_input())


p = Popen(['python', 'messages_people.py'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
output = p.stdout.read()
p.stdin.write(raw_input())