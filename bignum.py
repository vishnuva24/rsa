import time
from random import randint

class BigNum:
    def __init__(self, digits) -> None:
        if type(digits) == int:
            self.list = []
            while digits > 0:
                self.list.append(digits%10)
                digits = digits//10
        elif type(digits) == list:
            self.list = digits
    

    @property
    def length(self):
        self.remove_redundant_zeros()
        return len(self.list)
    
    def remove_redundant_zeros(self):
        i = -1        
        while self.list[i] == 0:
                self.list.pop()
                i = i-1
                if abs(i) >= len(self.list):
                    break
        return self

    def __add__(self, other):
        l1 = self.length
        l2 = other.length
        i,j = 0, 0
        sum = []
        carry = 0
        self.list.append(0)
        other.list.append(0)
        # assert: l1,l2, self, other, sum are established
        # INV: after k iterations, sum contaings the sum of self and other, considered till only k digits,
        #      carry = 1 if self[k-1] + other[k-1] + carry >= 10, 0 otherwise
        while (i < l1 or j < l2):
            s = self.list[i] + other.list[j] + carry
            sum.append(s%10)
            carry = s//10
            if i < l1:
                i = i+1
            if j < l2:
                j = j+1
        if carry == 1:
            sum.append(1)
        
        # assert: sum contaings the sum of self and other, carry = 0
        return BigNum(sum)
    
    def __sub__(self, other):
        l1 = self.length
        l2 = other.length
        if l1 < l2:
            raise ValueError("Operand 1 should be greater than Operand 2")
        i,j = 0, 0
        diff = []
        borrow = 0
        self.list.append(0)
        other.list.append(0)
        # assert: l1,l2, self, other, diff are established
        # INV: after k iterations, diff contains the difference of self and other, considered upto k digits, (0<= k <= min(l1,l2)) 
        #      d = self[k-1] - other[k-1] - borrow; if d < 0, d = 10 + d, borrow = 1, else borrow = 0
        while (i < l1 or j < l2):
            d = self.list[i] - other.list[j] - borrow
            if d < 0:
                d = 10 + d
                borrow = 1
            else:
                borrow = 0
            diff.append(d)
            if i < l1:
                i = i+1
            if j < l2:
                j = j+1
        # assert: diff contains the difference of self and other, carry = 0
        return BigNum(diff)
    
    def __mul__(self, other):
        l1 = self.length
        l2 = other.length
        self.list.append(0)
        other.list.append(0)
        pdt = BigNum([0])
        i = 0
        # assert l1,l2, self, other, pdt are established
        # INV: after i iterations, pdt contains the product of self and the other number considered only upto i digits. 
        while (i < l2):
            j = 0
            carry = 0
            current_digit = other.list[i]
            c_sum = []
            while (j< l1):
                p = (self.list[j] * current_digit) + carry
                c_sum.append(p%10)
                carry = p//10
                j += 1
            if carry != 0:
                c_sum.append(carry)
            
            pdt = pdt+BigNum([0]*i + c_sum)
            i += 1
        # assert pdt contains the product of the two numbers. 
        return pdt
    
    def __eq__(self, other):
        l1 = self.length
        l2 = other.length
        if l1 != l2:
            return False
        i = 0
        # assert: l1, l2, self, other are established
        # INV: after i iterations, self[0..i-1] == other[0..i-1]
        while i < l1:
            if self.list[i] != other.list[i]:
                return False
            i += 1
        return True
    
    def __lt__(self, other):
        l1 = self.length
        l2 = other.length
        if l1 < l2:
            return True
        if l1 > l2:
            return False
        i = 1
        # assert: l1, l2, self, other are established
        # INV: after i iterations, self[l-i..l-1] == other[l-i..l-1]
        while i <= l1:
            if self.list[-i] < other.list[-i]:
                return True
            if self.list[-i] > other.list[-i]:
                return False
            i += 1
        return False
    
    def __le__(self, other):
        l1 = self.length
        l2 = other.length
        if l1 < l2:
            return True
        if l1 > l2:
            return False
        i = 1
        # assert: l1, l2, self, other are established
        # INV: after i iterations, self[l-i..l-1] == other[l-i..l-1]
        while i <= l1:
            if self.list[-i] < other.list[-i]:
                # assert: self < other
                return True
            if self.list[-i] > other.list[-i]:
                # assert: self > other
                return False
            i += 1
        # assert: self == other
        return True
   
    def __gt__(self, other):
        return not self <= other
    
    def __ge__(self, other):
        return not self < other
    
    def __floordiv__(self, other):
        r = self
        q = BigNum([0])
        one = BigNum([1])
        # assert: r, q, one, other are established
        # INV: after k iterations, q = k, r = self - k*other, 0 <= r < other
        while other <= r:
            r = r - other
            q = q + one
        
        # assert: r = self % other, q = self // other
        return q
    
    def __mod__(self, other):
        r = self
        q = BigNum([0])
        one = BigNum([1])
        # assert: r, q, one, other are established
        # INV: after k iterations, q = k, r = self - k*other, 0 <= r < other
        while other < r:
            r = r - other
            q = q + one

        # assert: r = self % other, q = self // other
        return r
    
    def sqr(self):
        return self*self
    
    def __pow__(self, exp):
        if exp == BigNum([0]):
            return BigNum([1])
        if exp == BigNum([1]):
            return self
        if exp%BigNum([2]) == BigNum([0]):
            return (self**(exp//BigNum([2]))).sqr()
        else:
            return self*((self**(exp//BigNum([2]))).sqr())
    
        
def randgen(l:int, r:int) -> BigNum:
    return BigNum(randint(l, r))
