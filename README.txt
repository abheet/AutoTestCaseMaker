#  AutoTestCase Maker

Hi! I'm Abheet this tool is created to easeout the process of test casenter code heree creation, which done by many of QA guys in excelsheets! which is quite time consuming process. As we all knew preparing test cases is a time consuming process and eventually when scenarios will remains same in most of the time.


# About It
**AutoTestCase**  tool helps us **automate API level testcases.**
In API testing we have to cover some basic validations which will be common 
for most of the API parameters , like covering **Positive and Negative 
scenarios**  like to cover:
 1. MIN/MAX lengths check
 2. Invalid data
 3. Mandatory
 4. Optional param validations etc.

This will become more tedious when some APIs are so huge in terms of request/response params i.e. hundreds of request/response parameters!! that it tooks hours of efforts to draft testcase and paining activity too!!

To overcome the problem, I  have tried to solve the problem with a small solution where we can auto generate test cases from swagger or from CSV files  with this **AutoTestCase** So that testcases can be drafted quickly and acurately, this tool will generates testcases in no time for huge APIs too.


## Scenarios Covered will be:

It actually cover/create 4 test cases for each request parameters
(i.e Below Scenarios are configurable). 

 1. Two Positive test cases 
	 > i.e Valid Value and Mandatory Check
	 
2. Two Negative  test cases 
	 > i.e Blank Value and Invalid Value

If test cases are less in numbers it can automatically upload to TestRail too.
**If test cases count exceed 100 count (configurable)  then we can upload the generated CSV file directly to TestRail manually.**
>
## Benefits

IT SAVES TIME AND ENERGY (Especially your precious EYES).
> **Screenshots of application available in pdf file**

### How to setup and run:
#### Setup ####
> If Running Locall y:
	- Must have Python 3.x.x installed on  your System
	- `cd \Your working dir\`
	- `pip3 install -r requirement.txt`
	- After all packages installed with above command
#### How to Run ####
> If Running Locally:
 1. In your terminal/Command prompt Go to your working dir
 2. `Python3 StartScript.py`
 3. Once GUI Opened
 4. Browse the Swagger file and click on Proceed button.
 > (Script might come up with some swagger errors,as it support swagger 2.0 only)
 6. Then use the Most Prefered way, Use Temaplate to prepare the CSV file refer CSV_testcase_TEMPLATE.csv file to prepare it accordingly. Put all your API/Parameters details w.r.t template and save the csv file.

## How use CSV Option:
    1. Upload the CSV file you may created w.r.t template file   CSV_TestCase_TEMPLATE.csv file
    2. Fill the GUI form and MUST click on CHECKBOX i.e. I want to generate with csv
    3. Hit the Generate button! and that's it, the test case will be generated  automatically.

# Addon functionality
>**Test Case Clubbed functionality!!**
Auto test case generation tool actually generate test case for each and every request parameter and this might increase the test case count massively **(in 1000s)** so to easeout we have clubbing options available too. 

Here we can club **OPTIONAL params** in a single test case. However for all required params there will be still 4 test cases for each required param.
We can select how many optional params should be added in a single test case, and when to use this functionality!

>To use the above case Go to Src\config.ini file and set values as required.

**PARAMETER_CLUB = 2**

> i.e. how many optional params need to be clubbed

**API_PARAM_COUNT_TRIGGER = 40**
 > If API params count is more than 40 (i.e. 40 param into 4 test scenarios = 160 testcase) then it will be triggered and clubbed test cases will be created.

Test Cases were uploaded as soon as script finished with auto generation and
will only uploaded to testRail if count of test cases is not exceeds to 100

>I hope it will saves lots of QA time and efforts, Use it and SHARE it.

**Happy testing!**
