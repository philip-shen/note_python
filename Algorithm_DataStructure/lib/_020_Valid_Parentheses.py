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

from logger import logger

class Solution:
    def isValid(self,s):
        """
        :type s: str
        :rtype: bool
        """
        while s.find("()") != -1 or s.find("[]") != -1 \
            or s.find("{}") != -1:
            
            s_empty = ""
            if s.find("()") != -1:
                s=s.replace("()",s_empty)

            if s.find("[]") != -1:
                s=s.replace("[]",s_empty)

            if s.find("{}") != -1:
                 s=s.replace("{}",s_empty)

        return len(s) == 0

class Solution_better:
    def isValid(self,s):
        """
        :type s: str
        :rtype: bool
        """
        mapping = {
            '(':')',
            '{':'}',
            '[':']'
        }

        stack = []
        logger.info( 's:{}'.format(s) );#debug purpose

        for char in s:
            logger.info( 'char:{}'.format(char) );#debug purpose
            
            if char in mapping:
                logger.info( 'char:{}'.format(char) );#debug purpose
                stack.append(char)
                logger.info( 'stack.append(char):{}'.format(stack) );#debug purpose
            else:
                if not stack:
                    logger.info( 'not stack:{}'.format(stack) );#debug purpose
                    return False
                if mapping[stack.pop()] != char:
                    logger.info( 'mapping[stack.pop()]:{}'.format(mapping[stack.pop()]) );#debug purpose
                    return False

            if not stack:
                logger.info( 'not stack:{}'.format(stack) );#debug purpose
                return True

            return False
            # return True if not stack else False
            # return False if stack else True    