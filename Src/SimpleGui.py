#!/usr/bin/python3
# -*- coding: utf-8 -*-
# import PySimpleGUI as sg
import PySimpleGUI as sg
import os
from Src import TestRail as tr

testRailObj = tr.APIClient()


def projects():
    testRail_projects = testRailObj.get_projects()
    project_list = []
    for project in testRail_projects:
        name = project.get('name') + '-' + str(project.get('id'))
        project_list.append(name)
    return project_list


path = os.path.abspath(os.getcwd())


def setGUI():
    sg.theme('BrownBlue')
    layout = [[sg.Text('AutoTestCase Tool', justification='center', font=("Helvetica", 14))],
              [sg.Text(
                  '*Note:Test cases will be upload to TestRail\'s [AutoTestCase] section if count is upto 100 testcases')],

              [sg.Frame(layout=[
                  [sg.Text('API Swagger/CSV File', size=(20, 1)), sg.InputText('Swagger YAML/Parameter CSV file', size=(45, 1)),
                   sg.FileBrowse('Browse', size=(10, 1),  key='swagger-file')],
                  [sg.Text('Target/Output Folder', size=(20, 1)), sg.InputText(size=(45, 1), default_text=(path), key='dest_folder'),
                   sg.FolderBrowse('Location', size=(10, 1))],
                  #[sg.Text('Select TestRail Project', size=(20,1)), sg.DropDown(projects(),auto_size_text=True,key='testrail_project')],
                  [sg.Text('API Platfrom supported', size=(20, 1)), sg.InputText(
                      'Credit/Debit', size=(45, 1), key='platform_support')],
                  [sg.Text('QA Jira Task', size=(20, 1)), sg.InputText(
                      '', size=(45, 1), key='jira_task')],
                  [sg.Text('Project Name', size=(20, 1)), sg.InputText(
                      'PV_PROJECT_NAME', key='project_name', size=(45, 1))],
              ],
                  title='AutoTool V1.0', title_color='white', size=(50, 1), element_justification='left')],

              [sg.Frame(layout=[
                  [sg.Text(
                        'Can generate testcases with CSV, Prepare csv file w.r.t given template/example\nand upload it instead YAML file, Incase Failed to compile Swagger file')],
                  [sg.Text(text='CSV FORMAT:\nMethod,ContextPath,ParamName,ParamValue,Required,MaxLength,ParamDescriptions,DataType,Success-Response\ni.e seprated in none csv columns')],
                  [sg.Checkbox(
                      text='I Want to create test cases from CSV file', key='is_csv', default=False)]
              ], title='Alternative Option', title_color='white', size=(50, 1), element_justification='left')],

              [sg.Submit('Start Process', key='Submit'),
               sg.Cancel('Cancel', key='Cancel')],
              [sg.Text('Developed By: Abheet Singh Jamwal',
                       justification='center', font=("Helvetica", 10))]
              ]

    return sg.Window('AutoTestCase Tool', layout, finalize=True)


def notificationMsg(msg):
    sg.Popup(msg, keep_on_top=True)


def Debug(e):
    sg.Print(e)


def completed(title, msg):
    sg.SystemTray.notify(title, msg, fade_in_duration=30)


def close_window():
    sg.Window.close()
