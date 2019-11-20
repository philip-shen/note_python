import unittest
import os,sys

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
str_split=os.path.split(strdirname)
prevdirname=str_split[0]
dirnamelib=os.path.join(prevdirname,"lib")
dirnamelog=os.path.join(prevdirname,"logs")
sys.path.append(dirnamelib)

from _014_Longest_Common_Prefix import *
'''
Write a function to find the longest common prefix string amongst an array of strings.
If there is no common prefix, return an empty string "".
Example 1:
Input: ["flower","flow","flight"]
Output: "fl"
Example 2:
Input: ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.
Note:
All given inputs are in lowercase letters a-z.
'''

class Test_Case(unittest.TestCase):

    def test_ans_01(self):
        input = ["flower", "flow", "flight"]
        result = "fl"
        self.assertEqual(Solution().longestCommonPrefix(input), result)

    def test_answer_02(self):
        input = ["dog", "racecar", "car"]
        result = ""
        self.assertEqual(Solution().longestCommonPrefix(input), result)

    def test_answer_03(self):
        input = []
        result = ""
        self.assertEqual(Solution().longestCommonPrefix(input), result)

    def test_answer_04(self):
        input = [""]
        result = ""
        self.assertEqual(Solution().longestCommonPrefix(input), result)

    def test_answer_05(self):
        input = ["a"]
        result = "a"
        self.assertEqual(Solution().longestCommonPrefix(input), result)

    def test_answer_06(self):
        input = ["aa", "aa"]
        result = "aa"
        self.assertEqual(Solution().longestCommonPrefix(input), result)

    def test_answer_07(self):
        input = ["", "b"]
        result = ""
        self.assertEqual(Solution().longestCommonPrefix(input), result)

    def test_answer_08(self):
        input = ["aaa", "aa", "aaa"]
        result = "aa"
        self.assertEqual(Solution().longestCommonPrefix(input), result)

    def test_answer_09(self):
        input = ["aaa", "aa", "aaaa", "aac"]
        result = "aa"
        self.assertEqual(Solution().longestCommonPrefix(input), result)


if __name__ == '__main__':
    #unittest.main()    
    
    input = ["flower", "flow", "flight"]
    result = "fl"
    #input = ["", "b"]
    #result = ""
    print("input: {}".format(input))
    ret = Solution_debug().longestCommonPrefix(input)
    print("ret: {}".format(ret))