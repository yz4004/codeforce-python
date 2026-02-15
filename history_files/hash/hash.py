
class Solution:
    def __init__(self):
        self.base = 499
        self.M = 2**64 - 1  # Equivalent to pow(2, 64) - 1

    def equalDigitFrequency(self, s):
        n = len(s)
        f = [0] * (n + 1)  # Prefix hash array
        cnt = [[0] * (n + 1) for _ in range(10)]  # Count of each digit up to index i

        # Initialize prefix hash and count arrays
        for i in range(n):
            f[i + 1] = (f[i] * self.base + (ord(s[i]) - ord('0')) + 1) % self.M
            for j in range(10):
                cnt[j][i + 1] = cnt[j][i] + (1 if ord(s[i]) - ord('0') == j else 0)

        # Use a set to store unique hash values
        values = set()
        for i in range(n):
            for j in range(i + 1, n + 1):
                freq = -1
                valid = True
                for k in range(10):
                    t = cnt[k][j] - cnt[k][i]
                    if t == 0:
                        continue
                    if freq != -1 and t != freq:
                        valid = False
                        break
                    elif freq == -1:
                        freq = t

                if not valid:
                    continue

                hashcode = (f[j] - f[i] * pow(self.base, j - i, self.M) % self.M + self.M) % self.M
                values.add(hashcode)

        return len(values)