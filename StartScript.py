#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Author: Abheet Jamwal
4/21/2020
'''
import os
import csv
import copy
import datetime
import json
import sys
import yaml

from Src import SimpleGui as gui
from Src import ReadConfig as config
from Src.DocTables import TableCls
from PySimpleGUI.PySimpleGUI import Print
from Src import TestCasesCreate as createTest
from Src import TestRail as tr
import traceback


class MasterDocGenerator(TableCls):

    def __init__(self):
        self.sg = gui
        self.rc = config
        self.message = ''
        self.dt = datetime.datetime.now()

        # Main
        self.window = self.sg.setGUI()
        # by default single doc generated
        self.generateMultipleDocsFlag = False

        self.dataKey = 'Data Type = {A – Alphabetic Value, AN- Alphanumeric Value, N- Numeric Value, N/A- Not Applicable, Object, Array, Boolean}'
        self.reqKey = 'REQ* = Required Fields: {R – Value is required, O – Value is optional, C – Conditionally Required}'
        self.inputTypeKey = '{H– Header Parameter, P - Path Parameter, Q- Query Parameter}'
        self.masterDict = {}

    def apiDetailSection(self, swagger):
        # Add API Name and Info
        self.info = swagger['info']
        self.base_path = swagger['servers'][0].get('url')

        api_details = {
            'api_name': self.info['title'],
            'platform_support': str(self.inputs['platform_support'].strip()),
            'qa_task': str(self.inputs['jira_task'].strip()),
            'project_name': str(self.inputs['project_name'].strip()),
            'dest_folder': str(self.inputs['dest_folder'].strip()),
            'endpoint_path': self.base_path
        }
        # update api  details in master dict
        self.masterDict.update(api_details)
        return True

    def docGenerator(self):
        while True:
            try:

                self.event, self.inputs = self.window.read()
                # self.window.finalize()
                # print(self.event,self.inputs)
                print(
                    '************************ Auto TestCase Generator********************************\n')
                if(self.event in (None, 'Cancel')):
                    break

                # Open Yaml FIle, Convert to Json, Store into Dictionary
                print('-- Reading Swagger YAML File\n')
                if (self.inputs['swagger-file'] != '' and self.inputs['is_csv'] is False):
                    with open(self.inputs['swagger-file'], encoding='utf-8') as yamlFile:
                        self.swagger = json.loads(
                            json.dumps(yaml.safe_load(yamlFile)))
                        ''' 
                        In case of Multiple Document Checkbox Selected
                        Fuction intializw new doc object and prepare first page with API details with foote
                        Returns document new object
                        docObj = self.apiDetailSection(self.swagger)
                        '''
                        self.apiDetailSection(self.swagger)
                        paths = self.swagger['paths']
                        for pathName in paths:
                            for httpMethod in paths[pathName]:
                                self.methodsDict = {}
                                self.paramDict = {}
                                self.tempParamList = []
                                self.required_param = []
                                httpMethod_path = paths[pathName][httpMethod]
                                methodDescription = httpMethod.upper().rstrip()
                                if('parameters' in httpMethod_path):
                                    self.tempParamList, sampleResponse = self.api_headers(
                                        httpMethod_path.get('parameters'))
                                    # update param dict
                                    header_details = {
                                        'request_parameters': self.tempParamList,
                                        'request_sample': str(sampleResponse)
                                    }

                                    self.paramDict.update(header_details)

                                # Body Request Parameters
                                if('requestBody' in httpMethod_path):
                                    # fnction call return list of request params and sample request
                                    request_body = ''
                                    request_body, sample_request = self.api_request_body(
                                        httpMethod_path['requestBody'], self.tempParamList, self.required_param)
                                    self.paramDict['request_parameters'] = request_body
                                    self.paramDict['request_sample'] = sample_request

                                    # update param dict
                                    # self.paramDict.update(request_details)
                                    if type(request_body[-1]) is list:
                                        self.required_param = request_body[-1]
                                    else:
                                        self.required_param = []

                                # Body Response Parameters
                                if('responses' in httpMethod_path):
                                    # add Response Body required summary
                                    self.tempSampleDict = []
                                    messageReceived = False
                                    sample = ''
                                    responseBody = httpMethod_path.get(
                                        'responses')
                                    if responseBody:
                                        for responseCode in responseBody:

                                            keys = [self.dataKey]
                                            responseParamTable = responseSampleExample = responseRef = ''
                                            if 'content' in responseBody.get(responseCode):
                                                responseSchemaRef = responseBody.get(
                                                    responseCode).get('content')
                                                messageReceived = False
                                                contentType = 'application/json' if ('application/json' in responseSchemaRef) else '*/*' if (
                                                    '*/*' in responseSchemaRef) else 'application/problem+json' if ('application/problem+json' in responseSchemaRef) else ''
                                                if(contentType in responseSchemaRef):
                                                    if('example' in responseSchemaRef[contentType]):
                                                        sample = responseSchemaRef[contentType]['example']
                                                        self.tempSampleDict.append(
                                                            self.response_sample(responseCode, sample))
                                                        messageRecieved = True
                                                    responseSchemaRef = responseSchemaRef[contentType]['schema']
                                                    if('example' in responseSchemaRef):
                                                        sample = responseSchemaRef['example']
                                                        self.tempSampleDict.append(
                                                            self.response_sample(responseCode, sample))
                                                        messageRecieved = True
                                                    responseSchemaRef = responseSchemaRef['items'] if (
                                                        'items' in responseSchemaRef) else responseSchemaRef
                                                    responseSchemaRef = responseSchemaRef['oneOf'][0] if (
                                                        'oneOf' in responseSchemaRef) else responseSchemaRef
                                                    responseRef = responseSchemaRef['$ref'] if (
                                                        '$ref' in responseSchemaRef) else ''
                                                if(responseRef != ''):
                                                    responseRefPath = self.getRefPath(
                                                        responseRef, '#/components/schemas/', self.swagger['components']['schemas'])

                                                    if('example' in responseRefPath):
                                                        sample = responseRefPath['example']
                                                        self.tempSampleDict.append(
                                                            self.response_sample(responseCode, sample))
                                                    if(messageReceived == False):
                                                        messageRecieved = True
                                                        self.tempSampleDict.append(
                                                            self.response_sample(responseCode, sample))
                                                    else:
                                                        self.tempSampleDict.append(
                                                            self.response_sample(responseCode, sample))
                                                else:
                                                    if('properties' in responseSchemaRef):
                                                        if(messageReceived == False):
                                                            messageRecieved = True
                                                            self.tempSampleDict.append(
                                                                self.response_sample(responseCode, sample))
                                                        else:
                                                            self.tempSampleDict.append(
                                                                self.response_sample(responseCode, sample))

                                            elif '$ref' in responseBody.get(responseCode):
                                                responseSchemaRef = responseBody.get(
                                                    responseCode)
                                                responseRef = responseSchemaRef['$ref'] if (
                                                    '$ref' in responseSchemaRef) else ''
                                                responseRefPath = self.getRefPath(
                                                    responseRef, '#/components/responses/', self.swagger['components']['responses'])
                                                if('example' in responseRefPath):
                                                    sample = responseRefPath['example']
                                                    self.tempSampleDict.append(
                                                        self.response_sample(responseCode, sample))
                                                if(messageReceived == False):
                                                    messageRecieved = True
                                                    self.tempSampleDict.append(
                                                        self.response_sample(responseCode, sample))
                                                else:
                                                    self.tempSampleDict.append(
                                                        self.response_sample(responseCode, sample))

                                        # self.tempSampleDict[0] only capturing success response
                                        parm_details = {
                                            'response_sample': self.tempSampleDict[0][1]}
                                        # update response example in param dict
                                        self.paramDict.update(parm_details)

                                method_details = {
                                    'method_summary': str(httpMethod_path['summary']).rstrip(),
                                    'params': self.paramDict
                                }

                                self.methodsDict.update(method_details)

                            masterDictKey = str(
                                httpMethod).upper().rstrip() + '<>' + pathName

                            # add contextpath dict
                            self.masterDict.update(
                                {masterDictKey: self.methodsDict})
                        return self.masterDict
                elif (self.inputs['is_csv'] is True and self.inputs['swagger-file'] != ''):
                    csv_file_path = self.inputs['swagger-file']
                    param_list = []
                    masterDict = {}
                    api_details = {
                        'api_name': str(self.inputs['project_name'].strip()),
                        'platform_support': str(self.inputs['platform_support'].strip()),
                        'qa_task': str(self.inputs['jira_task'].strip()),
                        'project_name': str(self.inputs['project_name'].strip()),
                        'dest_folder': str(self.inputs['dest_folder'].strip()),
                        'endpoint_path': 'https://api.xyz.com/'
                    }
                    masterDict.update(api_details)
                    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                        csv_reader = csv.reader(csvfile)
                        header = next(csv_reader)
                        # Check file as empty
                        if header != None:
                            for row in csv_reader:
                                methodsDict = {}
                                httpMethod = row[0].strip()
                                context = row[1].strip()
                                param_name = row[2].strip()
                                param_value = row[3].strip()
                                required = 'Required' if 'R' in row[4].strip(
                                ) else 'O'
                                max_length = int(
                                    row[5].strip()) if row[5] != '' else ''
                                details = row[6].strip()
                                data_type = row[7].strip()
                                response_sample = row[8].strip()

                                # ['httpMethod<>context','ParamName','AN/Numeric/String,'Required/Optional','description',MaxLength','paramExample','availableInbody']
                                masterDictKey = httpMethod.strip().upper() + '<>' + context.strip()
                                params_details = [masterDictKey, response_sample, param_name,
                                                  data_type, required, details, max_length, param_value, 'request']
                                param_list.append(params_details)

                    if param_list:

                        success_responses = [
                            '*'.join(i[:2]) for i in param_list if i[1] != '']
                        count = 0
                        dictKeyIndex = 0
                        self.paramList = []
                        self.flag = False
                        for row in param_list:
                            request = {}
                            method_details = {}
                            if len(param_list) > count+1:
                                nextItem = param_list[count+1]
                            else:
                                nextItem = []
                            # continue saving common records in comparision to next record,  as we have to fetch paramters based upon method context path
                            if row[0] in nextItem:
                                self.paramList.append(row[2:])
                                # ['ParamName','AN/Numeric/String,'Required/Optional','description',MaxLength','paramExample','availableInbody']
                                masterDictKey = row[0]
                                self.flag = True
                                count = count + 1
                                continue
                            # save next methods record
                            elif (self.flag is False and row[0] not in nextItem):
                                self.paramList.append(row[2:])
                                masterDictKey = row[0]
                            # save last common record
                            elif row[0] not in nextItem:
                                self.paramList.append(row[2:])
                                masterDictKey = row[0]

                            # check if item is last in csv, will save last row
                            elif len(nextItem) is 0:
                                self.paramList.append(row[2:])
                                masterDictKey = row[0]

                            if masterDictKey not in masterDict.keys():

                                for i in success_responses:
                                    v = i.split('*')
                                    if masterDictKey == v[0]:
                                        value = v[1]
                                        break
                                    else:
                                        value = ''

                                requiredParam = [
                                    k[0] for k in self.paramList if k[2] == 'Required']
                                require = copy.deepcopy(requiredParam)
                                self.paramList.append(require)
                                request = {
                                    'request_parameters': self.paramList.copy(),
                                    'request_sample': '',
                                    'response_sample': value
                                }
                                method_details = {
                                    'method_summary': 'Method Summary',
                                    'params': request
                                }
                                dictKeyIndex = dictKeyIndex + 1
                            methodsDict.update(method_details)
                            finalCopy = copy.deepcopy(methodsDict)
                            masterDict.update({masterDictKey: finalCopy})

                            count = count + 1
                            self.paramList.clear()
                            requiredParam.clear()

                    return masterDict

                elif self.inputs['swagger-file'] == '':
                    self.sg.notificationMsg(
                        'Please browse Swagger/CSV file first!')
                    continue

            except PermissionError as e:
                self.sg.notificationMsg(
                    'Please close output file to proceed!!')
            '''
            except Exception as e:
                value = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)) 
                self.sg.Debug(value)
            except StopIteration:
                pass    
            '''

        self.window.close()
        return True


if __name__ == "__main__":

    obj = MasterDocGenerator()

    records = obj.docGenerator()
    testcase = createTest.CreateTestCase(records)
    status, csv = testcase.masterDict()
    if (status == True and len(csv) < 100):
        testrail = tr.APIClient()
        testrail.upload_case(csv)
        pass
    else:
        gui.notificationMsg(
            'Warning: Auto testcase upload can\'t be done.\n Testcase count exceeds 100\nPlease upload test cases manually in testrail.')
