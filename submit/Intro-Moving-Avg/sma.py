import sys

string = '& 0 & 0 & 0 & 0 & 10 & 20 & 30 & 35 & 20 & 10 & 5 & 0 & 0 & 0 & 0'

str_numbers = string.split('&')
numbers = [int(str) for str in str_numbers if str <> '']

N = 4
delay_line = [0,0,0,0]
output_seq = []
for num in numbers:
    delay_line.append(num)
    del delay_line[0]
    output_seq.append(sum(delay_line) / float(N))

print '%r' % output_seq
output_str = []
for output in output_seq:
    output_str.append('%4.2f' % output)

print ' & '.join(output_str)

f = open('sma.dat', 'w')
for input,output in zip(numbers, output_seq):
    f.write('%4.2f %4.2f\n' % (input, output))
f.close()
