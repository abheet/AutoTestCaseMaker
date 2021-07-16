*AUTO TEST Case Maker tool*
Developed by:
Abheet Singh Jamwal on 17-April-2020


****************Namaskaram***********************

About The Tool:
Preparing test cases is a time consuming process and eventually where the  scenarios will
remain same in most of the time.
In API testing we have to cover some basic validations which will be common 
for with API parameters (i.e. request and response), like covering Positive and Negative 
scenarios (i.e. MIN/MAX lengths, Invalid data, Mandatory,Optional param validations etc.)
this will become more tedious when there were APIs with more than 
hundreds of request/response parameters!!

Drafting Test Cases for such huge APIs, sometimes eats lot of time and also eye 
paining activity!! where you need to cross check the Swagger and requirement document precisely.

To overcome the problem, I  have tried to solve the problem with a small solution where we can
auto generate test cases from swagger or from CSV files  with this AutoToo.

Test  scenarios covered under this auto tool will be:
It actually cover/create 4 test cases for each request parameters
(i.e Below Scenarios are configurable). 
1: 2 Positive test cases i.e Valid Value and Mandatory Check
2: 2 Negative  test cases i.e Blank Value and Invalid Value

-If test cases are less in numbers it can automatically upload to TestRail too.
-If test cases count exceed 100 count (configurable)  then we can upload the generated CSV file 
directly to TestRail manually.

Benefits:
IT SAVES TIME AND ENERGY (Especially your precious EYES)


-------------Find the ScreenShots from pdf file---------------

-HOW INSTALL AND RUN:
If Running Locally:
	- Must have Python 3.x.x installed on  your System
	- cd \Your working dir\
	- pip3 install -r requirement.txt
	- After all packages installed with above command 

-How to RUN this:
1> In your terminal/Command prompt Go to your working dir
2> Enter command > Python3 StartScript.py
3> Once GUI opened, Browse the Swagger file and click on Proceed button.(Script might come up with 
some swagger errors,as it support swagger 2.0 only)
4> Then use the Most Prefered way, Use Temaplate to prepare the CSV file refer CSV_testcase_TEMPLATE.csv 
file to prepare it accordingly. Put all your API/Parameters details w.r.t template and save the csv file.

+ HOW TO USE ALTERNATIVE(CSV) OPTION:
    1. Upload the CSV file you may created w.r.t template file CSV_TestCase_TEMPLATE.csv file 
    2. Fill the GUI form and MUST click on CHECKBOX i.e. I want to generate with csv
    3. Hit the Generate button! and that's it, the test case will be generated  automatically.

-Addon: Test Case Clubbed functionality!! 
Auto test case generation tool actually generate test case for each and every 
request parameter and this might increase the test case count massively 
(in 1000s) so to easeout we have clubbing options available too.

i.e. we can club OPTIONAL params in a single test case. However for all required
params there will be still 4 test cases for each required param.
We can select how many optional params should be added in a single test case, 
and when to use this functionality!

To use the above case Go to Src\config.ini file and set values as required.

PARAMETER_CLUB = 2 > i.e. how many optional params need to be clubbed
API_PARAM_COUNT_TRIGGER = 40 > If API params count is more than 40 
(i.e. 40 param into 4 test scenarios = 160 testcase) then it will be triggered 
and clubbed test cases will be created.

Test Cases were uploaded as soon as script finished with auto generation and
will only uploaded to testRail if count of test cases is not exceeds to 100

I hope it will saves lots of QA time and efforts, Use it and SHARE it.

Happy testing!

