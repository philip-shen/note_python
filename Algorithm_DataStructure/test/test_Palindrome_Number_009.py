import unittest
import os, sys

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from _009_Palindrome_Number import *

'''
Determine whether an integer is a palindrome. An integer is a palindrome when it reads the same backward as forward.
Example 1:
Input: 121
Output: true
Example 2:
Input: -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
Example 3:
Input: 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
'''

class Test_Case(unittest.TestCase):

    def test_ans01(self):
        x = 121
        result = True
        self.assertEqual(Solution().isPalindrome(x), result)

    def test_ans02(self):
        x = -121
        result = False
        self.assertEqual(Solution().isPalindrome(x), result)    

    def test_answer_03(self):
        x = -123
        result = False
        self.assertEqual(Solution().isPalindrome(x), result)

    def test_answer_04(self):
        x = 10
        result = False
        self.assertEqual(Solution().isPalindrome(x), result)

if __name__ == "__main__":
    #unittest.main()
    x = 12321
    Solution().isPalindrome(x)
    #Solution_2().isPalindrome(x)
    pass            