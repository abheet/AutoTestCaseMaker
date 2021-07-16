#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import random
import string
import json
from Src import SimpleGui as gui
from Src import ReadConfig as config


class CreateTestCase():

    def __init__(self, api_details):

        self.objective = "Execution should be successful upon passing the value in the parameter."
        self.context = ''
        self.records = api_details
        self.saved_in = self.records.get(
            'dest_folder') if 'dest_folder' in self.records else ''
        self.r_api_name = self.records.get(
            'api_name') if 'api_name' in self.records else ''
        self.r_platform_support = self.records.get(
            'platform_support') if 'platform_support' in self.records else ''
        self.endpoint_path = self.records.get(
            'endpoint_path') if 'endpoint_path' in self.records else ''
        self.test_scenarios = {
            'NEG': {
                'InValid': 'Invalid Values',
                'LVT': 'Length validation Testing',
                'MVT': 'Mandatory Value Testing'
            },
            'POS': {
                'Valid': 'ValidValues',
                'MVT': 'Mandatory Value Testing'
            },
        }
        self.total_param_club = config.configValues.get('PARAMETER_CLUB')
        self.total_params_trigger = config.configValues.get(
            'API_PARAM_COUNT_TRIGGER')
        # call main execution function
        # self.masterDict()

    '''
    TestCase Steps
    Rally External Reference(project details) : Shop-APIs - SH102
    Rally Reference to Task: TA111
    Rally Sections/API with Multiple endpoints POST - /context
    Rally Title : API_NAME VALID
    Rally Objectives:Execution should be successful upon passing the value in the parameter.
    Rally Preconditions : "1: API code should be deployed published on server"
    Rally Steps :1. API client (Postman/Soapui) tool 2.Enter the string type data in the following field A. Param_name [Valid value] 3. Click on submit request
    Rally Expected Results : The system should return a response 200 OK Response: -Response = 0  -Message =[Successfully created!]
    Ticket References
    '''

    def precondition(self, api, precontion=''):
        precontion = ''
        precontion = "1: API code should be deployed to server \n 2: {} API should be published \n".format(
            api)
        return precontion

    def project_name(self):
        project_name = ''
        project_name = self.records['project_name']
        return project_name

    def qa_task(self):
        qatask = ''
        qatask = self.records['qa_task']
        return qatask

    def value_generator(self, datatype, scenario, length=6, param_value=''):
        datatype = str(datatype).upper()
        lettersAndDigits = ''
        if scenario == 'NEG':
            length = int(random.choice(string.digits))
        else:
            pass

        if datatype == 'AN':
            lettersAndDigits = string.ascii_uppercase + string.digits
            param_value = ''.join(random.choices(lettersAndDigits, k=length))
        elif datatype == 'ARRAY':
            pass
        elif datatype == 'NUMERIC':
            lettersAndDigits = string.digits
            param_value = ''.join(random.choices(lettersAndDigits, k=length))
        elif datatype == 'STRING':
            lettersAndDigits = string.ascii_letters
            param_value = ''.join(random.choices(lettersAndDigits, k=length))
        elif datatype == 'OBJECT':
            param_value = 'Its Object, check swagger for child params'

        return param_value

    def testcase_title(self, *args):
        '''
        Function to draft test case title in below format
        API-Name_Method_test-Scenario _param_test-validation
        eg: API Name Excludes_POST_POS _instId_Valid  
        api_name,method,test_scenario,param,test_validation
        '''
        title = "{}_{}_{}_{}_{}".format(*args)
        return title

    def expected_result(self, scenario, condition, response_sample, param, result=''):

        if scenario == 'NEG':
            if condition == 'InValid':
                result = "Http Status: 400 \n\nValidation message should state:\n\n InValid {}.".format(
                    param)
            elif condition == 'BVT' or 'LVT':
                result = "Http Status: 400 \n\nValidation message should state:\n\n {} Length is not correct".format(
                    param)
            elif condition == 'MVT':
                result = "Http Status: 400 \n\nValidation message should state:\n\n {} is mandatory.".format(
                    param)
        elif scenario == 'POS':
            if (response_sample != '' and '<?' not in response_sample):
                response = "Response Sample:\n\n" + \
                    json.dumps(json.loads(
                        response_sample.replace("\'", "\"")), indent=4)
            else:
                response = response_sample

            if condition == 'Valid':
                result = "Http Status: 20x\nMessage: 00-SUCCESS\n\n{}".format(
                    response)
            elif condition == 'BVT' or 'MVT':
                result = "Http Status: 20x\nMessage: 00-SUCCESS\n\n{}".format(
                    response)
        return result

    def section_name(self, val):
        self.context = val.split('<>')
        method = self.context[0]
        section = self.context[1] + ' - ' + method
        return section, method

    def divide_chunks(self, lst, n):
        # looping till length l
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def steps(self, *args):
        # ['clientId', 'AN', 'R', 'An assigned value associated with the shop ID', 4]
        # ['ParamName','AN/Numeric/String,'Required/Optional','description',MaxLength','paramExample']
        # returns allParamList[['ParamName','AN/Numeric/String,'Required/Optional','description',MaxLength','paramExample','availableInbody'],example,[requiredparams,p1,p2]]
        # self.steps(self.r_api_name,r_platform_support,r_api_url,r_method,r_method_summary,r_request_sample,r_response_sample,context,param)
        # self.testcase_title(self.r_api_name,r_method,test_scenario,param,test_validation)
        testCasesPerParameter = []
        apiName = str(args[0]).strip()
        platforms = str(args[1]).strip()
        endpoint = str(args[2]).strip()
        method = str(args[3])
        methodSummary = str(args[4]).strip()
        requestSample = str(args[5]).strip()
        responseSample = str(args[6]).strip()
        context_path = args[7]
        required_param_list = args[8]
        parameter_detail = args[9]

        for scenario in self.test_scenarios.keys():

            for condition in self.test_scenarios[scenario]:

                step_items = ''
                step = ''
                maxlength = 20
                value_example = ''
                param_dataType = 'String'
                isRequired = ''
                definedIn = ''
                try:
                    param_name = parameter_detail[0]
                    param_dataType = parameter_detail[1]
                    isRequired = parameter_detail[2]
                    description = parameter_detail[3]
                    maxlength = parameter_detail[4]
                    value_example = parameter_detail[5]
                    definedIn = parameter_detail[6] if parameter_detail[6] else ''
                except IndexError as e:
                    print(e)

                '''
                ************************************ TestCase CSV template *******************************    
                '''

                # External Reference(project details) : Ex ref
                external_reference = self.project_name()

                # Reference to QA Ticket Task: Ta111
                Ticket_reference = self.qa_task()

                # Sections/API with Multiple endpoints POST - /context
                section = context_path

                # Title : API Name Excludes_POST_POS _param_INVALID.
                title = self.testcase_title(
                    apiName, method, scenario, param_name, condition)

                # Objectives:Execution should be successful upon passing the value in the parameter.
                self.objective

                # Preconditions : "1: API code should be deployed to server 2: API should be published"
                precondition = self.precondition(apiName)
                if type(maxlength) == int:
                    maxlength = maxlength-1
                else:
                    maxlength = 25  # random number

                '''
                Test Cases conditions made based upon test case scenarios and condition
                '''
                if scenario == 'NEG':
                    if condition == 'InValid':
                        value = self.value_generator(
                            param_dataType, scenario, maxlength, value_example)
                        step_items = '{} = {} i.e. [{}]'.format(
                            param_name, value, condition)
                    elif condition == 'BVT':
                        value = self.value_generator(
                            param_dataType, scenario, maxlength, value_example)
                        step_items = '{} = {} i.e. [{}] and Max Value:{}'.format(
                            param_name, value, condition, maxlength)
                    elif condition == 'LVT':
                        value = self.value_generator(
                            param_dataType, scenario, maxlength, value_example)
                        step_items = '{} = {} i.e. [{}] and MAX Value : {}'.format(
                            param_name, value, condition, maxlength)
                    elif condition == 'MVT' and isRequired == 'R':
                        value = self.value_generator(
                            param_dataType, scenario, maxlength, value_example)
                        step_items = '{} = "BLANK" i.e. [{}]'.format(
                            param_name, condition)
                    else:
                        step_items = '{} = "" i.e. [{}]'.format(
                            param_name, condition)
                elif scenario == 'POS':
                    if condition == 'Valid':
                        value = self.value_generator(
                            param_dataType, scenario, maxlength, value_example)
                        step_items = '{} = {}  i.e. [{}] Note: Ask Platfrom Team for SIT values'.format(
                            param_name, value, condition)
                    elif condition == 'BVT' or 'MVT':
                        value = self.value_generator(
                            param_dataType, scenario, maxlength, value_example)
                        step_items = '{} = {} i.e. [{}]'.format(
                            param_name, value, condition)
                    else:
                        step_items = '{} = "" i.e. [{}]'.format(
                            param_name, condition)

                # Steps :1. GO to SOAP UI tool 2.Enter the string type data in the following field A. param [Valid value] 3. Click on submit request
                steps = "1. Goto SOAP UI/Postman tool.\n2. Hit API with following details.\n\nAPI Endpoint URL:\n{}\n\nRequired Params are:\n{}\n\n{}\n-------------Test Scenario-------------\n\nPayload with {} Parameter(s):\n{}\n\nTest data:\n{}\n\nHowever valid value would be:{}\n\n**NOTE ABOVE STEPS WERE GENERATED WITH AUTOMATION".format(endpoint,
                                                                                                                                                                                                                                                                                                                                                      '\n'.join(
                                                                                                                                                                                                                                                                                                                                                          required_param_list),
                                                                                                                                                                                                                                                                                                                                                      description,
                                                                                                                                                                                                                                                                                                                                                      definedIn.upper(),
                                                                                                                                                                                                                                                                                                                                                      param_name,
                                                                                                                                                                                                                                                                                                                                                      step_items,
                                                                                                                                                                                                                                                                                                                                                      value_example)

                # Expected Results : The system should return a response 200 OK Response: -Response = 0  -Message =[Successfully created]
                result = self.expected_result(
                    scenario, condition, responseSample, param_name)

                row = [external_reference, Ticket_reference, section, title,
                       self.objective, precondition, steps.strip(), result]
                testCasesPerParameter.append(row)
        return testCasesPerParameter

    def masterDict(self):
        csvSheet = []
        for key, value in self.records.items():
            if key not in ('api_name', 'platform_support', 'endpoint_path', 'qa_task', 'project_name', 'dest_folder'):
                context = self.section_name(key)
                contextPath = str(context[0])
                r_method = context[1]
                context_with_backslash = context[0] if '/' in context[0] else '/' + context[0]
                r_api_url = self.endpoint_path if 'https://api.xyz.com/' in self.endpoint_path else self.endpoint_path + \
                    context_with_backslash

                r_method_summary = self.records[key]['method_summary']
                param_records = self.records[key]['params']
                for param, val in param_records.items():

                    r_request_sample = param_records['request_sample']
                    r_response_sample = param_records['response_sample']

                    params_list = param_records['request_parameters']
                    requiredParamExist = param_records['request_parameters'][-1]

                    if type(requiredParamExist) is list and len(requiredParamExist) > 0:
                        required_params = param_records['request_parameters'][-1]

                    if 'Query' in requiredParamExist:
                        required_params = 'Params exist as Query'
                    elif 'Path' in requiredParamExist:
                        required_params = 'Param exist as Path parameters'
                    else:
                        required_params = requiredParamExist if requiredParamExist else 'Please check swaggers for required parameters'

                    '''
                    To reduce number of steps for bigger apis, we will clubbed optional param \
                        cases in single test case, i.e single test case for 2 optional params                            
                    '''
                    # self.total_params_trigger defined in Master class
                    total_params_in_api = self.total_params_trigger if self.total_params_trigger else 0
                    # checking if api params are huge in number as limit set above in total_params_in_api, will get those out from main param_list set

                    if len(params_list) >= int(total_params_in_api):
                        # created seprate optional params list
                        optional_params_of_api = [
                            i[0] for i in params_list[:-1] if i[2] == 'O']
                        # remove existing optional params from main params_list
                        for item in params_list[:-1]:
                            if item[2] == 'O':
                                params_list.pop(params_list.index(item))
                        # self.total_param_club defined in AutoTestCase-Run Init method
                        clubbed_param_set = list(self.divide_chunks(
                            optional_params_of_api, int(self.total_param_club)))
                        clubbed_list = []
                        for val in clubbed_param_set:
                            # getting params exact name i.e param1 from above string -> param2_param3_param1
                            club_params = []
                            for name in val:
                                if '_' in name:
                                    club_params.append(name.split('_')[-1])
                                else:
                                    club_params.append(name)

                            param_clubbed_name = " & ".join(club_params)
                            # as in test rail title can't be more than 250 char, will reduce it"
                            title_len = len(param_clubbed_name)
                            if title_len >= 230:
                                param_clubbed_name = param_clubbed_name[:170]

                            dataType = 'String'
                            isRequired = 'O'
                            description = ''
                            maxLength = 10
                            value = 'Not Defined'
                            request = ''
                            data = [param_clubbed_name, dataType, isRequired,
                                    description, maxLength, value, request]
                            clubbed_list.append(data)
                        # getting required param from main list as, we always kept required param records in the end.
                        required_param = params_list.pop()
                        # inserting clubbed records in main list
                        params_list.extend(clubbed_list)
                        # again putting required params in the end of main params list
                        params_list.append(required_param)

                    # getting exact param out from parent params, i.e. param1 from above string -> param2_param3_param1
                    required = []

                    for req in required_params:
                        if '_' in str(req):
                            required.append(req.split('_')[-1])
                        else:
                            required.append(req)

                    for param in params_list:
                        if len(param) >= 5:

                            # [['ParamName','AN/Numeric/String,'Required/Optional','description',MaxLength','inbody/query'],[required_params],'[paramExample]']
                            args = (self.r_api_name, self.r_platform_support, r_api_url, r_method,
                                    r_method_summary, r_request_sample, r_response_sample, contextPath, required, param)
                            paramTestCases = self.steps(*args)
                            csvSheet.extend(paramTestCases)
        return self.get_csv(csvSheet), csvSheet  # Save CSV file

    def get_csv(self, *args):
        file_name = self.r_api_name + '_Autoscript_Test Cases.csv'
        file_path = os.path.abspath(os.path.join(self.saved_in, file_name))
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as fp:
                writer = csv.writer(fp)
                writer.writerow(["External Reference(project details)",
                                 "Reference to task",
                                 "Sections",
                                 "Title",
                                 "Objectives",
                                 "Preconditions",
                                 "Steps",
                                 "Expected Results"
                                 "Ticket References"])
                for rows in args:
                    writer.writerows(rows)
                gui.completed('Test Case Generated Successfully!', 'Test Case of {} generated!\n\nFile Saved at {}'.format(
                    self.r_api_name, file_path))
                return True
        except PermissionError as e:
            gui.notificationMsg("Please close test case file and try again.")
