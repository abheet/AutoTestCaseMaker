#!/usr/bin/python
# -*- coding: utf-8 -*-
from docx.shared import Inches


class TableCls:

    def setType(self, type):
        if(type == 'string'):
            theType = 'AN'
        elif(type == 'integer' or type == 'number'):
            theType = 'N'
        elif(type == 'boolean'):
            theType = 'Boolean'
        elif(type == 'array'):
            theType = 'Array'
        elif(type == 'object'):
            theType = 'Object'
        else:
            theType = 'N/A'
        return theType

    def get_string_type_object(self, param_path, requiredParams, parameter, param_name):
        paramList = []
        # If there are array params, capturing details of them and will club in master paramlist
        fields = param_path.get('properties').get(
            parameter) if 'properties' in param_path else param_path
        description = fields.get('description').strip(
        ) if 'description' in fields else ''
        paramtype = self.setType(fields.get('type')) if 'type' in fields else fields.get(
            'enum') if 'enum' in fields else ''
        maxLength = fields.get('maxLength') if 'maxLength' in fields else 0
        example = fields.get('example') if 'example' in fields else fields.get(
            'enum') if 'enum' in fields else ''
        definedIn = 'Request Payload'
        if param_path.get('required'):
            isRequired = 'R'
            requiredParams.append(param_name)
        elif param_name in requiredParams:
            isRequired = 'R'
        else:
            isRequired = 'O'

        # Retrun array index ['ParamName','AN/Numeric/String,'Required/Optional','description',MaxLength','paramExample','defeined in']
        records = [param_name, paramtype, isRequired,
                   description, maxLength, example, definedIn]
        paramList.append(records)
        return paramList

    def get_properties(self, path, allParamList, arrayMembers, example, typeOfChart, requiredParams, paramType, param):
        if('properties' in path):
            for parameters in path['properties']:
                # check if parameter is f type array or object with ref
                if path.get('properties').get(parameters).get('type') in ('array', 'object'):
                    parent_param = '{}_{}'.format(param, parameters)
                    param_path = path.get('properties').get(parameters)
                    paramType = path.get('properties').get(
                        parameters).get('type')
                    requiredParams, arrayMembers = self.getArray(
                        param_path, allParamList, arrayMembers, requiredParams, example, typeOfChart, "", paramType, parent_param)
                    # resetting param's parent name after complting inner loop
                    param = parent_param.split('_')
                    param.pop(-1)
                    param = '_'.join(param)
                    continue
                elif '$ref' in path.get('properties').get(parameters):
                    parent_param = '{}_{}'.format(param, parameters)
                    param_path = path.get('properties').get(parameters)
                    paramType = path.get('properties').get(parameters).get(
                        'type') if path.get('properties').get(parameters).get('type') else ""
                    requiredParams, arrayMembers = self.getArray(
                        param_path, allParamList, arrayMembers, requiredParams, example, typeOfChart, "", paramType, parent_param)
                    # resetting param's parent name after complting inner loop
                    param = parent_param.split('_')
                    param.pop(-1)
                    param = '_'.join(param)
                    continue
                else:
                    parent_param = '{}_{}'.format(param, parameters)
                    tempArray = self.get_string_type_object(
                        path, requiredParams, parameters, parent_param)
                    arrayMembers.extend(tempArray)
                    param = parent_param.split('_')
                    param.pop(-1)
                    param = '_'.join(param)
        elif path.get('type') == 'string':
            paramList = self.get_string_type_object(
                path, requiredParams, param, param)
            arrayMembers.extend(paramList)
        return requiredParams, arrayMembers

    def getArray(self, param_path, allParamList, arrayMembers, requiredParams, example, typeOfChart, description, paramType, param):
        if('$ref' in param_path):
            ref = param_path.get('$ref')
            ref_path = self.getRefPath(
                ref, '#/components/schemas/', self.swagger['components']['schemas'])
        elif 'items' in param_path:
            if '$ref' in param_path.get('items'):
                ref = param_path.get('items').get('$ref')
                ref_path = self.getRefPath(
                    ref, '#/components/schemas/', self.swagger['components']['schemas'])
            elif 'properties' in param_path.get('items'):
                ref_path = param_path.get('items')
        else:
            ref_path = param_path
        requiredParams, arrayMembers = self.get_properties(
            ref_path, allParamList, arrayMembers, example, typeOfChart, requiredParams, paramType, param)
        return requiredParams, arrayMembers

    def getRefPath(self, ref, splitString, refPrePath):
        refPathName = ref.split(splitString)[1]
        ref_path = refPrePath[refPathName]
        return ref_path

    def populateBodyTable(self, basePath, example, typeOfChart, allParamList, requiredParams):
        arrayMembers = []
        if(typeOfChart == 'requestTable'):
            basePath = basePath['items'] if ('items' in basePath) else basePath
            required = basePath.get(
                'required') if 'required' in basePath else ''
            requiredParams.extend(required)
            if('properties' in basePath):
                properties_path = basePath['properties']
                for param in properties_path:
                    param_path = properties_path[param]
                    example = param_path['example'] if ('example' in param_path) else basePath['example'] if (
                        'example' in basePath) else example
                    if('type' in param_path):
                        paramType = self.setType(param_path.get('type'))
                        description = ''
                        requiredParams, arrayMembers = self.getArray(
                            param_path, allParamList, arrayMembers, requiredParams, example, typeOfChart, description, paramType, param)
                        if len(arrayMembers) > 0:
                            allParamList.extend(arrayMembers)
                            arrayMembers.clear()
                    else:
                        paramType = 'None'
                        description = ''
                        if('$ref' in param_path):
                            requiredParams, arrayMembers = self.getArray(
                                param_path, allParamList, arrayMembers, requiredParams, example, typeOfChart, description, paramType, param)
                            if len(arrayMembers) > 0:
                                allParamList.extend(arrayMembers)
                                arrayMembers.clear()
                    # adding individual param details in main param list
                    # paramList['ParamName','AN/Numeric/String,'Required/Optional','description',MaxLength','paramExample','defeined in']
                    arrayPath = param_path['items'] if (
                        paramType == 'array') else param_path if (paramType == 'object') else None
                    if arrayPath is not None:
                        requiredParams, arrayMembers = self.getArray(arrayPath, allParamList, arrayMembers, requiredParams, example, typeOfChart,  description, paramType, param) if (
                            arrayPath != None) else (requiredParams, [])

                        if len(arrayMembers) > 0:
                            allParamList.extend(arrayMembers)
                            arrayMembers.clear()

        elif(typeOfChart == 'responseChart'):
            pass

        allParamList.append(example)
        allParamList[-1] = requiredParams

        # returns allParamList[['ParamName','AN/Numeric/String,'Required/Optional','description',MaxLength','paramExample','availableInbody'],example,[requiredparams,p1,p2]]
        return allParamList

    def response_sample(self, code, example):
        sample = []
        sample = [code, example]
        return sample

    def setUpParamTable_ReqSummary(self, parameter, tableType, paramsList):
        isRequired = ''

        param_name = parameter['name']

        if 'schema' in parameter:
            paramType = parameter.get('schema').get('type')
            if 'maxLength' in parameter.get('schema'):
                maxLength = parameter.get('schema').get('maxLength')
            elif 'maximum' in parameter.get('schema'):
                maxLength = parameter.get('schema').get('maximum')
            else:
                maxLength = 0

            if 'example' in parameter.get('schema'):
                paramExample = str(parameter.get(
                    'schema').get('example')).strip()
            elif 'enum' in parameter.get('schema'):
                paramExample = str(parameter.get('schema').get('enum'))
            elif 'pattern ' in parameter.get('schema'):
                paramExample = str(parameter('schema').get('pattern'))
            else:
                paramExample = 'Not defined'
        else:
            maxLength = 0
            paramExample = str(parameter.get('example')).strip(
            ) if 'example' in parameter else ''
            paramType = 'string'

        if(('required' in parameter) and (parameter.get('required') == True)):
            isRequired = (('R' if (parameter.get('required') == True) else 'O') if (
                'required' in parameter) else 'O')

        description = parameter.get('description') if (
            'description' in parameter) else ''
        description = ' '.join(description.split('\n\t'))
        #values = [param_name,paramType,isRequired,description,maxLength,paramExample,tableType]

        paramsList.append(param_name)
        paramsList.append(paramType)
        paramsList.append(isRequired)
        paramsList.append(description)
        paramsList.append(maxLength)
        paramsList.append(paramExample)
        paramsList.append(tableType)

        # return paramsList['ParamName','AN/Numeric/String,'Required/Optional','description',MaxLength','paramExample','HeaderType/Queary/Path']
        return paramsList

    def api_headers(self, parameterList):
        # Create Summary of Required Parameters for H, P, or Q inputs
        headerParamsList = []
        for parameter in parameterList:
            self.headerList = []
            if('$ref' in parameter):
                requestBodyHeaderRef = parameter['$ref']
                parameter = self.getRefPath(
                    requestBodyHeaderRef, '#/components/parameters/', self.swagger['components']['parameters'])
            if(('in' in parameter) and (parameter['in'] == 'header')):
                headerParamsList.append(self.setUpParamTable_ReqSummary(
                    parameter, 'Header', self.headerList))
            elif(('in' in parameter) and (parameter['in'] == 'query')):
                headerParamsList.append(self.setUpParamTable_ReqSummary(
                    parameter, 'Query', self.headerList))
            elif(('in' in parameter) and (parameter['in'] == 'path')):
                headerParamsList.append(self.setUpParamTable_ReqSummary(
                    parameter, 'Path', self.headerList))

        if len(self.headerList) > 0:
            sample_response = 'Its defined in {}'.format(
                headerParamsList[-1][-1])

        return headerParamsList, sample_response

    def api_request_body(self, requestBody, tempParamList, required_param):
        bodyReqExample = ''
        requestBodyRefPath = ''
        if('content' in requestBody):
            content_path = requestBody['content']
            requestBodyRef = ''
            if('application/json' in content_path and '$ref' in content_path['application/json']['schema']):
                requestBodyRef = requestBody['content']['application/json']['schema']['$ref']

            elif('application/problem+json' in content_path and '$ref' in content_path['application/problem+json']['schema']):
                requestBodyRef = requestBody['content']['application/problem+json']['schema']['$ref']

            elif('*/*' in requestBody['content']):
                requestBodyRef = requestBody['content']['*/*']['schema']['$ref']

            elif('text/json' in requestBody['content']):
                requestBodyRef = requestBody['content']['text/json']['schema']['$ref']

            if requestBodyRef != '':
                requestBodyRefPath = self.getRefPath(
                    requestBodyRef, '#/components/schemas/', self.swagger['components']['schemas'])

            # special case if no ref given and directly object defined in properties object
            if('multipart/form-data' in requestBody['content'] and 'properties' in requestBody['content']['multipart/form-data']['schema']):
                requestBodyRefPath = requestBody['content']['multipart/form-data']['schema']

             # Add Resquest Body Title
            bodyValues = self.populateBodyTable(
                requestBodyRefPath, bodyReqExample, 'requestTable', tempParamList, required_param)

        else:
            requestBodyRef = requestBody['$ref']
            requestBodyRefPath = self.getRefPath(
                requestBodyRef, '#/components/requestBodies/', self.swagger['components']['requestBodies'])
            # Add Resquest Body Title
            bodyValues = self.populateBodyTable(
                requestBodyRefPath, bodyReqExample, 'requestTable', tempParamList, required_param)

        if('example' in requestBodyRefPath):
            bodyReqExample = requestBodyRefPath['example']
        else:
            bodyReqExample = '--Todo--'
        return bodyValues, bodyReqExample
