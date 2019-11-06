# note of_Rubber Duck Debugging 小黃鴨除錯法
Take some note of Rubber Duck Debugging

# Table of Content
[小黃鴨除錯法Rubber Duck Debugging]()  

[Top 40 QA Interview Questions & Answers](#top-40-qa-interview-questions-&-answers)  
[1) What is the difference between the QA and software testing?](#1-what-is-the-difference-between-the-qa-and-software-testing)
[2) What is Testware?](#2-what-is-testware)  
[3) What is the difference between build and release?](#3-what-is-the-difference-between-build-and-release)  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  
[]()  



# 小黃鴨除錯法Rubber Duck Debugging   
[小黃鴨除錯法Rubber Duck Debugging – Possability.Me – Medium Sep 5, 2018](https://medium.com/%E6%8C%87%E7%B4%8B%E7%9A%84%E7%A7%98%E5%AF%86/%E5%B0%8F%E9%BB%83%E9%B4%A8%E9%99%A4%E9%8C%AF%E6%B3%95-rubber-duck-debugging-e5e37e8645e8)  
```
     思維速度 > 聽說話速度 > 講說話速度

在指紋學上，右手二手指 R2 代表邏輯思維區，而右手四手指 R4 代表言語區。若你發現自己 R4 的紋數，相對低分過 R2，代表你把事情想得通後，但是用說話解釋就會比較吃力，詞不達意就是這樣。相反，若你發現自己 R4 的紋數，相對高分過 R2，即是你會傾向想「講」多過想「思考」，所以口快過腦可能就是這個情況。當然，這裡只是特意 pin point 這兩個區，其他區的影響這裡暫時不談。

    「小黃鴨除錯法」：R4 幫助 R2 及 R5

「小黃鴨除錯法」的原理，就是用說話拖慢自己的思維，慢慢看（程式碼），慢慢想，慢慢講，令程式員慢慢幫自己 go through 程式邏輯及輸入校對。啊，忘了說，右手五手指 R5 代表文字符號區。

現實生活中，常常把概念或問題困在腦中，當沒有出路時，倒不如用此方法，和公仔，和寵物，和朋友傾下計，用心把自己的思維細心解釋給他聽，靈感和生機很快會出現！ 
```

# Top 40 QA Interview Questions & Answers   
[Top 40 QA Interview Questions & Answers Oct 15, 2019](https://www.guru99.com/qa-interview-questions-answers.html)  
## 1) What is the difference between the QA and software testing?  
```
The role of QA (Quality Assurance) is to monitor the quality of the "process" used to produce the software.   
```
```
While the software testing, is the process of ensuring the functionality of final product meets the user's requirement.   
```

## 2) What is Testware?  
```
Testware is test artifacts like test cases, test data, test plans needed to design and execute a test.   
```

## 3) What is the difference between build and release?  
```
Build: It is a number given to Installable software that is given to the testing team by the development team.  
```
```
Release: It is a number given to Installable software that is handed over to the customer by the tester or developer.   
```

##  4) What are the automation challenges that SQA(Software Quality Assurance) team faces while testing?  
```
    Mastering the automation tool
    Reusability of Automation script
    Adaptability of test case for automation
    Automating complex test cases.  
```

## 5) What is bug leakage and bug release?  
```
Bug release is when software or an application is handed over to the testing team knowing that the defect is present in a release. 
During this the priority and severity of bug is low, as bug can be removed before the final handover.   
```
```
Bug leakage is something, when the bug is discovered by the end users or customer, 
and not detected by the testing team while testing the software.   
```

## 6) What is data driven testing?  
```
Data driven testing is an automation testing framework, which tests the different input values on the AUT. 
These values are read directly from the data files. The data files may include csv files, excel files, data pools and many more.   
```

## 7) Explain the steps for Bug Cycle?  
```
In open status,    Once the bug is identified by the tester, it is assigned to the development manager 

    If the bug is a valid defect the development team will fix it.
    
    If it is not a valid defect, the defect will be ignored and marked as rejected
    
    The next step will be to check whether it is in scope. 
    If the bug is not the part of the current release then the defects are postponed
    
DUPLICATE status, If the defect or bug is raised earlier then the tester will assign a DUPLICATE status
    
IN-PROGRESS status, When bug is assigned to developer to fix, it will be given a IN-PROGRESS status
    
FIXED, CLOSED status, Once the defect is repaired, the status will change to FIXED at the end the tester will give CLOSED status if it passes the final test.  
```

## 8) What does the test strategy include?  
```
The test strategy includes:

an introduction, 
resource, 
scope and 
schedule for test activities, 
test tools, 
test priorities, 
test planning and 
the types of test that has to be performed.  
```

## 9) Mention the different types of software testing?  
```
    Unit testing
    
    Shakeout testing
    
    Integration testing and regression testing

    Functional testing
    Performance testing
    Load testing and stress testing
    System testing

    Smoke testing    
    White box and Black box testing
    Alpha and Beta testing      
```

## 10) What is branch testing and what is boundary testing?  
```
The testing of all the branches of the code, which is tested once, is known as branch testing. 
```

```
While the testing, that is focused on the limit conditions of the software is known as boundary testing.   
```

## 11) What are the contents of test plans and test cases?  
```
    Testing objectives
    Testing scope
    Testing the frame
    The environment
    Reason for testing
    The criteria for entrance and exit
    Deliverables
    Risk factors  
```

## 12) What is Agile testing and what is the importance of Agile testing?  
```
Agile testing is software testing, is testing using Agile Methodology. 

The importance of this testing is that, unlike normal testing process, 
this testing does not wait for the development team to complete the coding first and then doing testing. 

The coding and testing both goes simultaneously. It requires continuous customer interaction.   
```

## 13) What is Test case?    
```
Test case is a specific condition to check against the Application Under Test. 

It has information of 
test steps, 
prerequisites, 
test environment, and 
outputs.   
```

##  14) What is the strategy for Automation Test Plan?   
```
Preparation of Automation Test Plan

Recording the scenario

Error handler incorporation

Script enhancement by inserting check points and looping constructs

Debugging the script and fixing the issues

Rerunning the script
Reporting the result  
```

## 15) What is quality audit?    
```
The systematic and independent examination for determining the effectiveness of quality control procedures 
is known as the quality audit.   
```

## 16) What are the tools used by a tester while testing?    
```
    Selenium
    Firebug
    OpenSTA
    WinSCP
    YSlow for FireBug
    Web Developer toolbar for firebox

Above are just sample tools. The tools a Tester may vary with his/her project.   
```

## 17) Explain stress testing, load testing and volume testing?  
```
Load Testing: 
Testing an application under heavy but expected load is known as Load Testing. 
Here, the load refers to the large volume of users, messages, requests, data, etc.
```
```
Stress Testing: 
When the load placed on the system is raised or accelerated 
beyond the normal range then it is known as Stress Testing.
```
```
Volume Testing: 
The process of checking the system, whether the system can handle 
the required amounts of data, user requests, etc. is known as Volume Testing.  
```

## 18) What are the five common solutions for software developments problems?    
```
Setting up the requirements criteria, 
the requirements of a software should be complete, clear and agreed by all

The next thing is the realistic schedule like time for planning , designing, testing, 
fixing bugs and re-testing

Adequate testing, 
start the testing immediately after one or more modules development.

Use rapid prototype during design phase so that it can be easy for customers to find what to expect

Use of group communication tools  
```

## 19) What is a 'USE' case and what does it include?    
```
The document that describes, the user action and system response, 
for a particular functionality is known as USE case. 

It includes 
revision history, 
table of contents, 
flow of events, 
cover page, 
special requirements, 
pre-conditions and 
post-conditions.   
```

## 20) What is CRUD testing and how to test CRUD?    
```
CRUD stands for Create, Read, Update and Delete. CRUD testing can be done using SQL statements.   
```

## 21) What is thread testing?    
```
A thread testing is a top-down testing, 
where the progressive integration of components follows 
the implementation of subsets of the requirements, 

as opposed to the integration of components by successively lower levels.   
```

## 22) What is configuration management?    
```
It is a process to control and document any changes made during the life of a project. 

Release control, 
Change control and 
Revision control 
are the important aspects of configuration management.  
```

## 23) What is Ad Hoc testing?    
```
It is a testing phase where the tester tries to break the system 
by randomly trying the system's functionality. 

It can include negative testing as well.   
```

## 24) List out the roles of Software Quality Assurance engineer?    
```
    Writing source code
    Software design
    Control of source code
    Reviewing code
    Change management
    Configuration management
    Integration of software
    Program testing
    Release management process  
```

## 25) Explain what are test driver and test stub and why it is required?   
```
The stub is called from the software component to be tested. 
It is used in top down approach

The driver calls a component to be tested. It is used in bottom up approach
   
It is required when we need to test the interface between modules X and Y and 
we have developed only module X. 

So we cannot just test module X but if there is any dummy module we can use that dummy module to test module X
```

## 26) Explain what is Bug triage? 
```
A bug triage is a process to

    Ensure bug report completeness

    Assign and analyze the bug
    
    Assigning bug to proper bug owner
    
    Adjust bug severity properly
    
    Set appropriate bug priority
```

## 27) List out various tools required to support testing during development of the application?  
```
To support testing during development of application following tools can be used

Test Management Tools: JIRA, Quality Center etc.

Defect Management Tools: Test Director, Bugzilla
    
Project Management Tools: Sharepoint
    
Automation Tools: RFT, QTP, and WinRunner
```

## 28) Explain what is a cause effect graph?   
```
A cause effect graph is a graphical representation of inputs and 
the associated outputs effects that can be used to design test cases. 
```

## 29) Explain what is Test Metric is software testing and what information does it contains?   
```
In software testing, Test Metric is referred to the standard of test measurement. 
They are the statistics narrating the structure or content of a testing. 

It contains information like

    Total test
    Test run
    Test passed
    Test failed
    Tests deferred
    Test passed the first time
```

## 30) Explain what is traceability matrix?  
```
A test matrix is used to map test scripts to requirements. 
```

## 31) Explain what is the difference between Regression testing and Retesting?  
```
Retesting is carried out to check the defects fixes, 

while regression testing is performed to check whether the defect fix 
have any impact on other functionality. 
```

## 32) List out the software quality practices through the software development cycle?   
```
Software quality practices includes

    Review the requirements before starting the development phase

    Code Review
    
    Write comprehensive test cases
    
    Session based testing
    Risk based testing
    
    Prioritize bug based on usage
    Form a dedicated security and performance testing team
    Run a regression cycle
    Perform sanity tests on production
    
    Simulate customer accounts on production
    
    Include software QA Test Reports
```

## 
```

```
## 
```

```
## 
```

```
## 
```

```

# Reference
* []()  
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