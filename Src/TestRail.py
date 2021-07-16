"""TestRail API binding for Python 3.x.

(API v2, available since TestRail 3.0)

Compatible with TestRail 3.0 and later.

Learn more:

http://docs.gurock.com/testrail-api2/start
http://docs.gurock.com/testrail-api2/accessing

Copyright Gurock Software GmbH. See license.md for details.
"""
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import base64
import json
import Src.SimpleGui as gui
import requests
import Src.ReadConfig as config


class APIClient():
    def __init__(self):
        self.user = config.configValues.get('USER')
        self.password = config.configValues.get('PASSWORD')
        self.section_testrail = config.configValues.get('SECTION_TESTRAIL')
        base_url = config.configValues.get(
            'PATH') if config.configValues.get('PATH') else "/"
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/api/v2/'
        self.sg = gui

    def send_get(self, uri, filepath=None):
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for 'get_attachment/:attachment_id'.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request('GET', uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri

        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {'Authorization': 'Basic ' + auth}

        if method == 'POST':
            if uri[:14] == 'add_attachment':    # add_attachment API method
                files = {'attachment': (open(data, 'rb'))}
                response = requests.post(url, headers=headers, files=files)
                files['attachment'].close()
            else:
                headers['Content-Type'] = 'application/json'
                payload = bytes(json.dumps(data), 'utf-8')
                response = requests.post(url, headers=headers, data=payload)
        else:
            headers['Content-Type'] = 'application/json'
            response = requests.get(url, headers=headers)

        if response.status_code > 201:
            try:
                error = response.json()
            except:     # response.content not formatted as JSON
                error = str(response.content)
                self.sg.Debug('TestRail API returned HTTP %s (%s)' %
                              (response.status_code, error))
        else:
            if uri[:15] == 'get_attachment/':   # Expecting file, not JSON
                try:
                    open(data, 'wb').write(response.content)
                    return (data)
                except:
                    return ("Error saving attachment.")
            else:
                try:
                    return response.json()
                except:  # Nothing to return
                    return {}

    def get_sections(self, suitesID=1660, projectID=197):
        uri = 'get_sections/{}&suite_id={}'.format(projectID, suitesID)
        values = self.send_get(uri)
        return values

    def get_projects(self):
        uri = 'get_projects'
        values = self.send_get(uri)
        return values

    def get_section(self, section_id):
        uri = "get_section/{}".format(section_id)
        values = self.send_get(uri)
        print(values)
        return values

    def add_section(self, groupId, sectionName, projectId=197, suiteId=1660):
        uri = "add_section/{}".format(projectId)
        request = {
            "suite_id": suiteId,
            "name": sectionName,
            "parent_id": groupId
        }
        return self.send_post(self, uri, request)

    def upload_case(self, request, groupId=909172):
        gui.completed('Uploading on TestRail..', 'Test Cases uploading...')
        uri = "add_case/{}".format(groupId)
        for i in request:

            record = {
                "title": i[3],
                "type_id": 9,
                "priority_id": 2,
                "estimate": "3m",
                "refs": i[1],
                "custom_extref": i[0],
                "externlink": "wiki",
                "custom_mission": i[4],
                "custom_preconds": i[5],
                "custom_steps": i[6],
                "custom_expected": i[7],
            }

            response = self.send_post(uri, record)

        return response


class APIError(Exception):
    pass


if __name__ == "__main__":
    clsObject = APIClient()
    clsObject.get_section(clsObject.section_testrail)
