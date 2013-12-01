class expAvg(object):
    def __init__(self, alpha):
        self.alpha = alpha
        self.y_D = 0.0
    def input(self, input):
        y = self.alpha * input + (1-self.alpha) * self.y_D
        self.y_D = y
        return y

avg2 = expAvg(0.2)
avg4 = expAvg(0.4)
avg6 = expAvg(0.6)
avg8 = expAvg(0.8)

Avg2Seq = []
Avg4Seq = []
Avg6Seq = []
Avg8Seq = []
InputSeq = []

f = open('avg_exp.dat', 'w')
for i in range(100):
    input = 10.0 if i > 6 else 0.0
    avg2_y = avg2.input(input)
    avg4_y = avg4.input(input)
    avg6_y = avg6.input(input)
    avg8_y = avg8.input(input)

    f.write('%8.7f %8.7f %8.7f %8.7f %8.7f\n' % (input, avg2_y, avg4_y, avg6_y, avg8_y))
    
    Avg2Seq.append(avg2_y)
    Avg4Seq.append(avg4_y)
    Avg6Seq.append(avg6_y)
    Avg8Seq.append(avg8_y)

f.close()    


        
