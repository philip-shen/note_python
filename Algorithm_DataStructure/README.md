# note_python_Algorithm_DataStructure
Take some note of python

# Table of Content
[Top Interview Questions - Problems](top-interview-questions-problems)

[Table List](#table-list)  
[001 Two Sum](#001-two-sum)  
[009 Palindrome Number](#009-palindrome-number)  
[013 Roman to Integer](#013-roman-to-integer)  
[014 Longest Common Prefix](#014-longest-common-prefix)  
[020 Valid Parentheses](#020-valid-parentheses)  
[021 Merge Two Sorted Lists](#021-merge-two-sorted-lists)  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  



# Top Interview Questions - Problems   
[Top Interview Questions - Problems](https://leetcode.com/problemset/top-interview-questions/)

# Table List  
No. | Test Name | Difficulty | Lib | UniTest 
------------------------------------ | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- 
001 | Two Sum | Easy | [_001_Two_Sum.py](https://github.com/philip-shen/note_python/blob/master/Algorithm_DataStructure/lib/_001_Two_Sum.py) |  [test_Two_Sum_001.py](https://github.com/philip-shen/note_python/blob/master/Algorithm_DataStructure/test/test_Two_Sum_001.py)
009 |  	Palindrome_Number | Easy | [_009_Palindrome_Number.py](https://github.com/philip-shen/note_python/blob/master/Algorithm_DataStructure/lib/_009_Palindrome_Number.py) | [test_Palindrome_Number_009.py](https://github.com/philip-shen/note_python/blob/master/Algorithm_DataStructure/test/test_Palindrome_Number_009.py) 
013 |  	Roman to Integer  | Easy | [_013_Roman_to_Integer.py](https://github.com/philip-shen/note_python/blob/master/Algorithm_DataStructure/lib/_013_Roman_to_Integer.py) | [test_Roman_to_Integer_013.py](https://github.com/philip-shen/note_python/blob/master/Algorithm_DataStructure/test/test_Roman_to_Integer_013.py) 
014 | Longest Common Prefix | Easy | [_014_Longest_Common_Prefix.py](https://github.com/philip-shen/note_python/blob/master/Algorithm_DataStructure/lib/_014_Longest_Common_Prefix.py) | [test_Longest_Common_Prefix_014.py](https://github.com/philip-shen/note_python/blob/master/Algorithm_DataStructure/test/test_Longest_Common_Prefix_014.py) 
020 |  	Valid Parentheses   | Easy | []() | []() 
021 |  	Merge Two Sorted Lists   | Easy | []() | []() 
026 |  	Remove Duplicates from Sorted Array   | Easy | []() | []() 
027 |  	Remove Element    | Easy | []() | []() 
028 |  	Implement strStr()    | Easy | []() | []() 
035 |  	Search Insert Position   | Easy | []() | []() 
038 |  	Count and Say    | Easy | []() | []() 
053 |  	Maximum Subarray | Easy | []() | []() 
058 |  	Length of Last Word | Easy | []() | []() 
066 |  	Plus One    | Easy | []() | []() 
067 |  	Add Binary     | Easy | []() | []() 
069 |  	Sqrt(x)     | Easy | []() | []() 
070 |  	Climbing Stairs | Easy | []() | []() 
038 |  	Count and Say    | Easy | []() | []() 
125 |  	Valid Palindrome | Easy | []() | []() 
136 |  	Single Number    | Easy | []() | []() 
168 |  	Excel Sheet Column Title | Easy | []() | []() 
169 |  	Majority Element | Easy | []() | []() 
171 |  	Excel Sheet Column Number | Easy | []() | []() 
172 |  	Factorial Trailing Zeroes | Easy | []() | []() 
190 |  	Reverse Bits     | Easy | []() | []() 
191 |  	Number of 1 Bits | Easy | []() | []() 
202 |  	Happy Number     | Easy | []() | []() 
205 |  	Isomorphic Strings | Easy | []() | []() 
206 |  	Reverse Linked List| Easy | []() | []() 
038 |  	Count and Say    | Easy | []() | []() 
046 |  	Permutations     | Medium | []() | []() 
137 |  	Single Number II | Medium | []() | []() 
151 |  	Reverse Words in a String | Medium | []() | []() 
137 |  	Single Number II | Medium | []() | []() 
137 |  	Single Number II | Medium | []() | []() 
137 |  	Single Number II | Medium | []() | []() 

# 001 Two Sum  
```
Question:
Given an array of integers, return indices of the two numbers such that they add up to a specific target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.

Example:
Given nums = [2, 7, 11, 15], target = 9,Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
```

# 009 Palindrome Number  
```
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
```
[Reverse a string in Python Nov 20, 2011](https://stackoverflow.com/questions/931092/reverse-a-string-in-python)  
```
>>> 'hello world'[::-1]
'dlrow olleh'
```
```
This is extended slice syntax. It works by doing [begin:end:step] - 
by leaving begin and end off and specifying a step of -1, it reverses a string.
```
```
Paolo's s[::-1] is fastest; a slower approach 
(maybe more readable, but that's debatable) is ''.join(reversed(s)).
```
[Understanding string reversal via slicing Nov 16, 2018](https://stackoverflow.com/questions/766141/understanding-string-reversal-via-slicing)  
```
Sure, the [::] is the extended slice operator. 
It allows you to take substrings. 
Basically, it works by specifying which elements you want as [begin:end:step], 
and it works for all sequences. Two neat things about it:

You can omit one or more of the elements and it does "the right thing"
Negative numbers for begin, end, and step have meaning
```
[extended slice](https://docs.python.org/3/whatsnew/2.3.html#extended-slices)

# 013 Roman to Integer  
```
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
```

# 014 Longest Common Prefix  
```
Question:
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
```

# 020 Valid Parentheses
```
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
```

#  021 Merge Two Sorted Lists 
```
Merge two sorted linked lists and return it as a new list.
The new list should be made by splicing together the nodes of the first two lists.
Example:
Input: 1->2->4, 1->3->4
Output: 1->1->2->3->4->4
```

#   
```

```

#   
```

```

No. | Test Name 
------------------------------------ | --------------------------------------------- | 
001 | Two Sum
```

```

No. | Test Name 
------------------------------------ | --------------------------------------------- | 
001 | Two Sum
```

```

# Reference
* [30天學演算法和資料結構 2018-10-16](https://ithelp.ithome.com.tw/users/20111557/ironman/2110?page=1)  
* [從LeetCode學演算法 - 0 你應該知道的面試基礎和解題技巧 Jun 26 2019](https://medium.com/@desolution/%E5%BE%9Eleetcode%E5%AD%B8%E6%BC%94%E7%AE%97%E6%B3%95-0-6c121bd8b579)  

```
  
```

* []()  
```

```

* []()  
```

```

* []()  
![alt tag]()

# h1 size

## h2 size

### h3 size

#### h4 size

##### h5 size

*strong*strong  
**strong**strong  

> quote  
> quote

- [ ] checklist1
- [x] checklist2

* 1
* 2
* 3

- 1
- 2
- 3