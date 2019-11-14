# note of_Rubber Duck Debugging 小黃鴨除錯法
Take some note of Rubber Duck Debugging

# Table of Content
[小黃鴨除錯法Rubber Duck Debugging]()  

[Top 40 QA Interview Questions & Answers](#top-40-qa-interview-questions--answers)  
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

[Top 15 Automation Testing Interview Questions & Answers](#top-15-automation-testing-interview-questions--answers)  



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
The role of QA (Quality Assurance) is to monitor the quality of the "process" 
used to produce the software.   
```
```
While the software testing, is the process of ensuring the functionality of 
final product meets the user's requirement.   
```

## 2) What is Testware?  
```
Testware is test artifacts like test cases, test data, test plans needed to design and execute a test.   
```

## 3) What is the difference between build and release?  
```
Build: It is a number given to Installable software 
that is given to the testing team by the development team.  
```
```
Release: It is a number given to Installable software 
that is handed over to the customer by the tester or developer.   
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
Bug release is when software or an application is handed over to 
the testing team knowing that the defect is present in a release. 

During this the priority and severity of bug is low, 
as bug can be removed before the final handover.   
```
```
Bug leakage is something, when the bug is discovered by the end users or customer, 
and not detected by the testing team while testing the software.   
```

## 6) What is data driven testing?  
```
Data driven testing is an automation testing framework, 
which tests the different input values on the AUT. 

These values are read directly from the data files. 
The data files may include csv files, excel files, data pools and many more.   
```

## 7) Explain the steps for Bug Cycle?  
```
In open status,    
    
    Once the bug is identified by the tester, it is assigned to the development manager 

    If the bug is a valid defect the development team will fix it.
    
    If it is not a valid defect, the defect will be ignored and marked as rejected
    
    The next step will be to check whether it is in scope. 
    If the bug is not the part of the current release then the defects are postponed
    
DUPLICATE status, 
    If the defect or bug is raised earlier then the tester will assign a DUPLICATE status
    
IN-PROGRESS status, 
    When bug is assigned to developer to fix, it will be given a IN-PROGRESS status
    
FIXED, CLOSED status, 
    Once the defect is repaired, the status will change to FIXED at the end 
    the tester will give CLOSED status if it passes the final test.  
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

## 33) Explain what is the rule of a "Test Driven Development"?  
```
The rule of a Test Driven Development is to prepare test cases before writing the actual code. 
Which means you are actually be writing code for the tests before you write code for the application. 
```

## 34) Mention what are the types of documents in SQA?  
```
The types of documents in SQA are

    Requirement Document

    Test Metrics
    Test cases and Test plan
    Task distribution flow chart
    
    Transaction Mix
    User profiles
    
    Test log
    Test incident report
    Test summary report
```

## 35) Explain what should your QA documents include?  
```
    List the number of defects detected as per severity level
    
    Explain each requirement or business function in detail
    
    Inspection reports

    Configurations
    
    Test plans and test cases
    
    Bug reports
    
    User manuals
    
    Prepare separate reports for managers and users
```

## 36) Explain what is MR and what information does MR consists of?  
```
MR stands for Modification Request also referred as Defect report. 
It is written for reporting errors/problems/suggestions in the software. 
```

## 37) What does the software QA document should include?  
```
    Specifications
    
    Designs
    Business rules
    Configurations

    Code changes
    
    Test plans
    Test cases
    
    Bug reports
    
    User manuals, etc
```

## 38) Mention how validation activities should be conducted?  
```
Validation activities should be conducted by following techniques

    Hire third party independent verification and validation

    Assign internal staff members that are not involved in validation and verification activities
    
    Independent evaluation
```

## Difference between Verification and Validation?  
[Verification和Validation的意義及區別 20130604](https://blog.xuite.net/metafun/life/75244104-Verification%E5%92%8CValidation%E7%9A%84%E6%84%8F%E7%BE%A9%E5%8F%8A%E5%8D%80%E5%88%A5)  

簡單【結論】：
Verification：確認達成規格 (requirements)；
Validation：確認達成目的 (intended use)。

```
CMMI-SVC, V1.2

Verification: 
Confirmation that work products properly reflect the requirements specified for them. 

In other words, verification ensures that “you built it right.” 

Validation: 
Confirmation that the product or service, as provided (or as it will be provided), 
will fulfill its intended use.

In other words, validation ensures that “you built the right thing.” 
```

```
 ISO 9000:2000

Verification: Confirmation, through the provision of objective evidence (3.8.1), 
that specified requirements (3.1.2) have been fulfilled. (達成規格)

Validation: Confirmation, through the provision of objective evidence (3.8.1), 
that the requirements (3.1.2) for a specific intended use or application have been fulfilled. (達成目的)
```

# Top 15 Automation Testing Interview Questions & Answers   
[Top 15 Automation Testing Interview Questions & Answers](https://www.guru99.com/automation-testing-interview-questions.html)  

## 1) What is Automation testing?  
```
Automation Testing is a technique using an automation tool to write and execute tester's test scripts and cases.

The main goal of Automation Testing is 
to reduce the number of test cases to be run manually and 
not eliminate Manual Testing altogether. 
```

## 2) When will you automate a test?  
```
Automation in preferred in following cases

    Repetitive Tasks
    Smoke and Sanity Tests
    Test with multiple data set
    Regression test cases

Usually, the decision is based on the ROI (Return on Investment) 
```

## 3) When will you not automate testing?  
```
One should not automate in following cases

    When the Application Under Test changes frequently
    One time test cases
    Adhoc – Random testing
```

## 4) What are the steps involved in the Automation Process?  
```
    Selecting the Test tool

    Define scope of automation
    
    Planning, design, and development
    
    Test execution
    
    Maintenance
```

## 5) What are the points that are covered while planning phase of automation?  
```
uring planning phase of automation things which must be taken in concern are

    Selection the "right" Automation tool

    Selection Automation Framework if any
    
    List of In scope and out of scope items for automation
    
    Test Environment Setup
    
    Preparing Grant Chart of Project timelines for test script development & execution.
    
    Identify Test Deliverables
```

## 6) In what condition we cannot use automation testing for the Agile method?  
```
Automation testing is not useful for agile methods in following conditions

    When Agile testing always ask for changes in requirements

    When Exhaustive level of documentation is required in Agile

    Only suitable for those regression tests during agile testing like continuous integration
```

## 7) What are the primary features of good automation tool?     
```
    Test Environment support and easy to use

    Good debugging facility
    
    Robust object identification
    
    Object and Image testing abilities
    
    Object identification
    
    Testing of database
    
    Support multiple frameworks 
```

##  8) What are the types of the framework used in software automation testing?   
```
In software automation testing four types of framework used are

    Data-driven automation framework

    Keyword driven automation framework
    
    Modular automation framework
    
    Hybrid automation framework
```

##  9) What is the scripting standard while performing automation testing?   
```
While writing the scripts for automation, you must consider following things,

    Uniform naming convention.

    3 Lines of comments for every 10 lines of code
    
    Adequate indentation.
    
    Robust error handling and recovery scenario
    
    Use of Frameworks wherever possible
```

##  10) What are the most popular tools for automation testing?   
```
The most popular test tool for automation testing are

    QTP (HP UFT)
    Rational Robot
    Selenium
```

##  11) On what basis you can map the success of automation testing?   
```
    Defect Detection Ratio
    
    Automation execution time and time savings to release the product
    
    Reduction in Labour & other costs
```

##  12) Can list out some disadvantages of manual testing?   
```
    Manual Software Testing requires more time and more resources.

    Inaccuracy
    
    Executing same test case repeatedly is error prone and boring.
    
    It is impractical to do manual testing on very large projects 
    and time bounded projects.
```

## 13) Tell me what you know about Selenium  
```
Selenium is a free (open source) Test automation library. It is used to automate Web and Mobile environments. It consists of

    Selenium IDE (Browser Addon – Record and Playback Tool)

    Selenium WebDriver
    
    Selenium Grid (Distributed Testing)

Selenium supports scripting in languages like Java, C#, Python, Ruby, PHP, Perl, Javascript. 
```

## 14) Tell me about QTP   
```
QTP (Quick Test Professional) is now known as HP UFT. 
It is a commercial automation tool and supports a very wide range of test environments Web, 
Desktop, SAP, Delphi, Net, ActiveX, Flex, Java, Oracle, Mobile, PeopleSoft, PowerBuilder, Siebel, 
Stingray, Visual Basic amongst others.

The scripting language is VBScript. 
The tool gels well with HP ALM (Test Management Tool) and 
HP LoadRunner (Performance Testing Tool).

Salient features of QTP include Business Process Testing, 
keyword driven framework, XML support, robust checkpoints, test results. 
```

## 15) Explain what Sikuli is?  
```
Sikuli is a tool that uses "Visual Image Match" method to automate graphical user interface. All the web elements in Sikuli should be taken as an image and stored inside the project.

Sikuli is comprised of

    Sikuli Script
    Visual Scripting API for Jython
    Sikuli IDE

Practical uses of Sikuli is that

    It can be used to automate flash websites or objects
    It can automate window based application and anything you see on screen without using internal API support
    It provides simple API
    It can be easily linked with tools like Selenium
    Desktop application can be automated
    Sikuli offers extensive support to automate flash objects
    To automate desktop, it uses powerful "Visual Match" and Flash objects
    It can work on any technology-.NET, Java,
```

## 16) Mention what is the difference between Selenium and Sikuli?  
```

Sikuli
    It provides extensive support to automate flash objects
    
    It has simple API
    
    It uses a visual match to find elements on the screen. So, we can automate anything we see on the screen
    
    It can automate the web as well as windows application


Selenium 
    It cannot automate flash objects like video player, audio player,
    
    It has got complicated API
    
    It does not have visual match
    
    It can automate only web applications

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