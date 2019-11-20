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
from logger import logger

class Solution:
    def longestCommonPrefix(self,strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if strs:
            strs.sort(key=len)
            s = strs[0]
            if not s:
                return ""
        else:
            return ""        

        for idx,value in enumerate(s):
            for str_per in strs:
                if str_per == s:
                    continue
                if str_per[idx] != value:
                    return s[:idx]

        return s

class Solution_debug:
    def longestCommonPrefix(self,strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if strs:
            strs.sort(key=len)
            #print("strs: {}".format(strs))
            logger.info('strs:{} '.format(strs));#debug purpose
    
            s = strs[0]
            if not s:
                #print("s:{}".format(s))
                logger.info('s:{} '.format(s));#debug purpose
                return ""
        else:
            return ""        

        #print("s:{}".format(s))
        logger.info('s:{} '.format(s));#debug purpose
        for idx,value in enumerate(s):
            #print("idx:{}, value:{}".format(idx,value))
            logger.info("idx:{}, value:{}".format(idx,value));#debug purpose

            for str_per in strs:
                #print("str_per:{}\n".format(str_per))
                logger.info("str_per:{}\n".format(str_per));#debug purpose

                if str_per == s:
                    #print("str_per:{} == s:{}".format(str_per,s))
                    logger.info("str_per:{} == s:{}".format(str_per,s));#debug purpose

                    continue
                if str_per[idx] != value:
                    #print("str_per[idx]:{} != value:{}".format(str_per[idx],value))
                    logger.info("str_per[idx]:{} != value:{}".format(str_per[idx],value));#debug purpose
                    
                    logger.info("s[:idx]:{}".format(s[:idx]));#debug purpose
                    return s[:idx]

        return s

class Solution:
    def longestCommonPrefix(self,strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:
            return ""
        # retrieved min max by alphabetical order    
        s1 = min(strs)
        s2 = max(strs)

        for idx, value in enumerate(s1):
            if value != s2[idx]:
                return s2[:idx]

        return s1        