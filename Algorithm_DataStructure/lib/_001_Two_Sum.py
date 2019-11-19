'''
Given an array of integers, return indices of the two numbers such that they add up to a specific target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
Example:
Given nums = [2, 7, 11, 15], target = 9,
Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
'''
class Solution:
    def twoSum(self,nums,target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for idx_one, one in enumerate(nums):
            for idx_two, two in enumerate(nums):
                if (one != two) and (one+two==target):
                    return [idx_one,idx_two] 

    """
    If there is a repetition in nums , will FAILED
    """                
class Solution_Improve:
    def twoSum(self,nums,target):
        for idx_one in range(len(nums)):
            for idx_two in range(len(nums)):
                if nums[idx_one]+nums[idx_two] == target:
                    return [idx_one,idx_two]    

class Solution_better:
    def twoSum(self,nums,target):
        dic_idx={}
        for idx, value in enumerate(nums):
            if target-value in dic_idx:
                return [dic_idx[target-value], idx]
                
            dic_idx[value]=idx    