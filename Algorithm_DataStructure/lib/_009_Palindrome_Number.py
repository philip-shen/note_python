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
from logger import logger

class Solution:
    def isPalindrome(self,x):
        """
        :type x: int
        :rtype:bool
        """

        if x < 0:
            return False
        else:
            reversed_int = int(str(x)[::-1])
            logger.info('X:{} '.format(str(x)))
            logger.info('str(x)[::-1]:{} '.format(str(x)[::-1]));#debug purpose

            if x == reversed_int:
                return True

            return False

class Solution_better:
    def isPalindrome(self,x):
        """
        :type x: int
        :rtype:bool
        """
        return False if x < 0 else x == int(str(x)[::-1]) 

class Solution_2:

    def isPalindrome(self,x):
        """
        :type x: int
        :rtype:bool
        """
        # without converting the integer to a string

        if x < 0:
            return False

        result = 0
        original = x
        logger.info('x:{} \n'.format(x));#debug purpose

        while x:
            result = result * 10 + x % 10
            x = int (x/10)

            logger.info('result:{} '.format(result));#debug purpose
            logger.info('x:{} '.format(x));#debug purpose

        return result == original    

class Solution_type:
    def isPalindrome(self,x):

        return False if x < 0 else x == int(str(x)[::-1])