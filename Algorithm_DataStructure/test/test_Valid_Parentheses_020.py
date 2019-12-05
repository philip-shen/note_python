'''
Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
An input string is valid if:
Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Note that an empty string is also considered valid.
Example 1:
Input: "()"
Output: true
Example 2:
Input: "()[]{}"
Output: true
Example 3:
Input: "(]"
Output: false
Example 4:
Input: "([)]"
Output: false
Example 5:
Input: "{[]}"
Output: true
'''
import unittest
import os,sys

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from _020_Valid_Parentheses import *

class Test_Case(unittest.TestCase):

    def test_ans_01(self):
        input = "()"
        result = True
        self.assertEqual(Solution().isValid(input), result)

    def test_answer_02(self):
        input = "()[]{}"
        result = True
        self.assertEqual(Solution().isValid(input), result)

    def test_answer_03(self):
        input = "(]"
        result = False
        self.assertEqual(Solution().isValid(input), result)

    def test_answer_04(self):
        input = "([)]"
        result = False
        self.assertEqual(Solution().isValid(input), result)

    def test_answer_05(self):
        input = "{[]}"
        result = True
        self.assertEqual(Solution().isValid(input), result)

    def test_answer_06(self):
        input = "}[]{"
        result = False
        self.assertEqual(Solution().isValid(input), result)

    def test_answer_07(self):
        input = "["
        result = False
        self.assertEqual(Solution().isValid(input), result)

if __name__ == "__main__":
    #unittest.main()
    input = "()[]{}"
    ret_value = Solution_better().isValid(input)
    print(ret_value)

    pass           