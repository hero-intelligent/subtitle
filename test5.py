class Trex:
    def __init__(self):
        self.q = self.f(1,2)
        self.qq = self.f(3,4)
        self.qqq = self.f(5,6)
        self.ddd = {
            "q": self.q,
            "qq": self.qq,
            "qqq": self.qqq
        }

    def f(self,a,b):
        ll = []

        for k in range(a):
            dd = {}

            for i in range(b):
                self.pritn = str(k) + "," + str(i)
                dd[str(i)] = str(k) + "," + str(i)
            ll.append(dd)
        return ll

tx = Trex()

print(tx.pritn)
