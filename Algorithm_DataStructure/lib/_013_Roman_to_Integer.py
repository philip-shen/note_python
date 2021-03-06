'''
Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
I can be placed before V (5) and X (10) to make 4 and 9.
X can be placed before L (50) and C (100) to make 40 and 90.
C can be placed before D (500) and M (1000) to make 400 and 900.
Given a roman numeral, convert it to an integer. 
Input is guaranteed to be within the range from 1 to 3999.

Example 1:
Input: "III"
Output: 3

Example 2:
Input: "IV"
Output: 4

Example 3:
Input: "IX"
Output: 9

Example 4:
Input: "LVIII"
Output: 58
Explanation: L = 50, V= 5, III = 3.

Example 5:
Input: "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.
'''
from logger import logger

class Solution:
    def romanToInt(self,s):
        """
        :type s: str
        :rtype: int
        """
        mapping = {
            'I':1,
            'V':5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

        temp = ''
        total = 0

        for roman in s:
            if temp:
                logger.info( 'temp:{}'.format(temp) );#debug purpose
                logger.info( 'roman:{}'.format(roman) );#debug purpose

                if mapping[roman] > mapping[temp]:
                    logger.info('mapping[roman]:{} mapping[temp]:{}'.format(mapping[roman], mapping[temp]));#debug purpose

                    total += mapping[roman] - mapping[temp]
                    logger.info( 'total:{}'.format(total) );#debug purpose
                    temp = ''
                    continue

                total += mapping[temp]
                logger.info('total:{} mapping[temp]:{}'.format(total, mapping[temp]));#debug purpose

            temp = roman

        if temp:
            logger.info( 'temp:{}'.format(temp) );#debug purpose
            
            total += mapping[temp]
            logger.info('total:{} mapping[temp]:{}'.format(total, mapping[temp]));#debug purpose

        return total    

class Solution_better:
    def romanToInt(self,s):
        """
        :type s: str
        :rtype: int
        """
        mapping = {
            'I':1,
            'V':5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

        total = 0

        for roman in range(len(s)-1):
            logger.info('range(len(s)-1):{} len(s)-1:{}'.format(range(len(s)-1), len(s)-1) );#debug purpose
            logger.info( 'roman:{}'.format(roman) );#debug purpose
            
            if mapping[s[roman]] > mapping[s[roman+1]]:
                total += mapping[s[roman]]
            else:
                total -= mapping[s[roman]]    

        total += mapping[s[-1]] 

        return total

class Solution_type:
    def romanToInt(self,s):
        mapping = {
            'I':1,
            'V':5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

        total=0
        logger.info( 's:{}'.format(s) );#debug purpose

        for idx in range(len(s)-1):
            logger.info('range(len(s)-1):{} len(s)-1:{}'.format(range(len(s)-1), len(s)-1) );#debug purpose
            logger.info( 'idx:{}'.format(idx) );#debug purpose

            if mapping[s[idx]] >= mapping[s[idx+1]]:
                logger.info('s[idx]:{} s[idx+1]:{}'.format(s[idx], s[idx+1]) );#debug purpose

                total += mapping[s[idx]]
                logger.info('total:{} mapping[s[idx]]:{}'.format(total, mapping[s[idx]]) );#debug purpose
            else:
                logger.info('s[idx]:{} s[idx+1]:{}'.format(s[idx], s[idx+1]) );#debug purpose
                total -=mapping[s[idx]]    
                logger.info('total:{} mapping[s[idx]]:{}'.format(total, mapping[s[idx]]) );#debug purpose

        total += mapping[s[-1]]        
        logger.info('total:{} mapping[s[-1]]:{}'.format(total, mapping[s[-1]]) );#debug purpose

        return total