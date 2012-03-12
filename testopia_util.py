#!/usr/bin/env python
# encoding: utf-8
"""
main.py

Created by guilechao on 2012-03-07.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import getopt
from testopia import Testopia
import os
import csv
import logging
import traceback
from httplib import HTTP
from urlparse import urlparse
from datetime import datetime


logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)   

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter1 = logging.Formatter("%(levelname)s - %(message)s")
ch.setFormatter(formatter1)
debug_log_path = "testopia_util.log"
if os.path.isfile(debug_log_path):os.unlink(debug_log_path)
fh = logging.FileHandler(debug_log_path)
fh.setLevel(logging.DEBUG)
formatter2 = logging.Formatter("%(asctime)s %(filename)s %(levelname)s - %(message)s")
fh.setFormatter(formatter2)
logger.addHandler(ch)
logger.addHandler(fh)

help_message = '''
The help message goes here.
'''

#testopia util version
ver = "1.0"

test_cases_result_path = "tc.csv"      
default_testplan_name = "ServerAPI"

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def get_testopia_product_id(tp, product):
    product_id = None
    try:
        product_id = int(product)
    except ValueError:
        #product is string
        #use workaround way to get product id
        for i in range(15):  
            try:      
                p = tp.product_check_by_id(i+1)
                if product.lower() == p['name'].lower():
                    product_id = p['id']
                    break
            except:
                pass            
        #product = tp.product_check_by_name(product)
        #product_id = product['product_id']
    return product_id
    
def get_testopia_author_id(tp, testopia_id):
    return tp.user_lookup_id_by_login(testopia_id)
    #hard code temporarily
    #return 2    
    
def get_testopia_type_id(tp, type_name):
    #testplan_lookup_type_id_by_name(self, name):
    if (type_name.lower() == "Unit".lower()):
        return 1    
    elif (type_name.lower() == "Integration".lower()):
        return 2   
    elif (type_name.lower() == "Function".lower()):
        return 3        
    elif (type_name.lower() == "System".lower()):
        return 4   
    elif (type_name.lower() == "Acceptance".lower()):
        return 5     
    elif (type_name.lower() == "Installation".lower()):
        return 6   
    elif (type_name.lower() == "Performance".lower()):
        return 7      
    else:
        return 0  
        
def get_testopia_testplan_id(tp, product_id, plan_name):    
    testplan_id = None    
    tp_list = tp.testplan_list(name=plan_name, product_id=product_id)
    if (len(tp_list) > 0):
        testplan_id = tp_list[0]['plan_id']
    return testplan_id
    
def get_testopia_testcase_id(tp, testcase):
    case_id = None
    try:
        case_id = int(testcase)
    except ValueError:
        tc_list = tp.testcase_list(alias=testcase)
        for tc in tc_list:
            if (tc['alias'].lower() == testcase.lower()) :
                case_id = tc['case_id']
    return case_id  
    
def get_testopia_build_id(tp, product_id, build):
    build = tp.build_check_by_name(build, product_id)
    return build['build_id']
    
def get_testopia_environment_id(tp, product_id, environment):
    environment_id = None    
    env_list = tp.environment_list(name=environment, product_id=product_id)
    if (len(env_list) > 0):
        environment_id = env_list[0]['environment_id']
    return environment_id    
    
def get_testopia_caserun_status_id(tp, tc_result):
    case_run_status_id = 1
    r = str(tc_result).strip().lower()
    if (r == '1' or r == 'true' or r == 'yes' or r == 't' or r == 'y') : 
        case_run_status_id = 2
    elif (r == '0' or r == 'false' or r == 'no' or r == 'f' or r == 'n') :  
        case_run_status_id = 3
        
    return case_run_status_id   
        
def check_url(url):
    p = urlparse(url)
    h = HTTP(p[1])
    h.putrequest('HEAD', p[2])
    h.endheaders()
    print h.getreply()[0]
    if h.getreply()[0] == 200: return True
    else: return False                                    

def main(argv=None):
    if argv is None:
        argv = sys.argv

    print "Command Line : %s" % argv

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output=", "mode=", "build_number="])
        except getopt.error, msg:
            raise Usage(msg)
            
        #default values, this will be overwritten by command line args or envronment vars
        #command line args > envronment vars > default values

        #mode can be add_build, write_results, update_test_cases
        mode = "write_result"
        testopia_url = "http://11.22.33.44/"
        testopia_xmlrpc_url = None
        testopia_id = "xxxxxxxx@gmail.com"
        testopia_password = "xxxxxxxx"
        product_name = "PI_SampleProduct"
        environment = "xxxxxxxx"
        build_number = "0000"      
            
        #replace default value by envronment vars
        logger.info("-------------Environment Variables-------------")
        for (k,v) in os.environ.items():
            logger.info("%-20s : %s" % (k, v))
        logger.info("-----------------------------------------------") 
            
        if (os.environ.get("BUILD_NUMBER", None) != None):
            build_number = os.environ["BUILD_NUMBER"]
        if (os.environ.get("TESTOPIA_URL", None) != None):
            testopia_url = os.environ["TESTOPIA_URL"]            
        if (os.environ.get("TESTOPIA_ID", None) != None):
            testopia_id = os.environ["TESTOPIA_ID"]          
        if (os.environ.get("TESTOPIA_PASSWORD", None) != None):
            testopia_password = os.environ["TESTOPIA_PASSWORD"]          
        if (os.environ.get("PRODUCT_NAME", None) != None):
            product_name = os.environ["PRODUCT_NAME"]        
        if (os.environ.get("ENVIRONMENT", None) != None):
            environment = os.environ["ENVIRONMENT"]              
                    
        #replace default value by command line args
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
            if option in ("--build_number"):
                build_number = value                
            if option in ("--mode"):
                mode = value  
                
        logger.info("-------------All Variables After Replace-------------")
        logger.info("%-20s : %s" % ("mode", mode))

        logger.info("%-20s : %s" % ("testopia_url", testopia_url))
        #testopia_xmlrpc_url = testopia_url + "bugzilla/xmlrpc.cgi"
        #logger.info(check_url(testopia_xmlrpc_url))
        testopia_xmlrpc_url = testopia_url + "xmlrpc.cgi"
        logger.info("%-20s : %s" % ("testopia_xmlrpc_url", testopia_xmlrpc_url))
        logger.info("%-20s : %s" % ("testopia_id", testopia_id))        
        logger.info("%-20s : %s" % ("testopia_password", testopia_password)) 
            
        #if the build number get from jenkins it will looks like "job/deploy%20build/3/"
        build_number = "PI%s" % (build_number.strip('/').split('/')[-1].zfill(4))
        logger.info("%-20s : %s" % ("build_number", build_number))
        
        logger.info("%-20s : %s" % ("product_name", product_name))
        logger.info("%-20s : %s" % ("environment", environment))
        
        logger.info("%-20s : %s" % ("test_cases_result_path", test_cases_result_path))
                
        logger.info("-------------Start Processing-------------")        
        tp = Testopia(testopia_id, testopia_password, testopia_xmlrpc_url)   
        
        author_id = get_testopia_author_id(tp, testopia_id)
        logger.info("author '%s' id is %d" % (testopia_id, author_id)) 

        product_id = get_testopia_product_id(tp, product_name)
        logger.info("product '%s' id is %d" % (product_name, product_id)) 

        if (mode == "add_build") :            
            build_description = "%s auto create this build" % str(datetime.now())
            logger.info("create a build") 
            build = tp.build_create(build_number, product_id, description=build_description)
            logger.info("build : %s" % (build))
        elif (mode == "write_result") :
            build_id = get_testopia_build_id(tp, product_id, build_number)
            logger.info("build '%s' id is %d" % (build_number, build_id)) 
            
            plan_id = get_testopia_testplan_id(tp, product_id, default_testplan_name)   
            logger.info("testplan '%s' id is %d" % (default_testplan_name, plan_id))         
            
            environment_id = get_testopia_environment_id(tp, product_id, environment)   
            logger.info("environment '%s' id is %d" % (environment, environment_id))                     
            
            #create a test run
            test_run_summary = "auto create test run"
            test_run_notes = "%s auto create this run" % str(datetime.now())
            logger.info("create a test run") 
            testrun = tp.testrun_create(build_id, environment_id, plan_id, test_run_summary, author_id, plan_text_version=0, notes=test_run_notes, product_version='unspecified')
            logger.info("testrun : %s" % testrun) 
            
            csv_reader = csv.reader(open(test_cases_result_path, 'rb'), delimiter=',', quotechar='"')
            for row in csv_reader:
                tc_alias = row[0]
                tc_summary = row[1]
                tc_result = row[2]
                
                #get test case id from alias
                case_id = get_testopia_testcase_id(tp, tc_alias)
                                
                if (case_id != None):             
                    logger.info("test case '%s' id is %d" % (tc_alias, case_id))    
                             
                    #add test case to test run
                    tp.testrun_add_cases(testrun['run_id'], case_id)
                
                    #update test case result in this run
                    case_run_status_id = get_testopia_caserun_status_id(tp, tc_result)
                    #logger.info("case result '%s' id is %d" % (tc_result, case_run_status_id))   
                    update_case_run = tp.testcaserun_update(testrun['run_id'], case_id, build_id, environment_id, case_run_status_id=case_run_status_id)
                    logger.info("update case result %s(case_run_status_id :%s)" % (tc_result, update_case_run['case_run_status_id']))   
                else:
                    logger.error("fail to get test case '%s' id" % tc_alias)                
        elif (mode == "update_test_cases") :                     
            type_id = get_testopia_type_id(tp, "Unit")
            
            #check is testplan exist
            logger.info("check is testplan '%s' exist" % default_testplan_name)   
            if (tp.testplan_is_exist(product_id, default_testplan_name)):
                logger.info("testplan '%s' is exist" % default_testplan_name) 
            else:
                logger.info("testplan '%s' is not exist so create it" % default_testplan_name) 
                tp.testplan_create(default_testplan_name, product_id, author_id, type_id, 'unspecified')
            plan_id = get_testopia_testplan_id(tp, product_id, default_testplan_name)    
            logger.info("testplan '%s' id is %d" % (default_testplan_name, plan_id)) 
            
            #update test cases to testplan              
            csv_reader = csv.reader(open(test_cases_result_path, 'rb'), delimiter=',', quotechar='"')
            for row in csv_reader:
                tc_alias = row[0]
                tc_summary = row[1]
                
                if (tp.testcase_is_exist(tc_alias)) :
                    logger.info("testcase '%s' is exist so update it" % tc_alias) 
                    testcase = tp.testcase_update(tc_alias, tc_summary, isautomated=True, case_status_id=2, priority_id=1)
                    logger.debug("testcase : %s" % testcase) 
                else :
                    logger.info("testcase '%s' is not exist so create it" % tc_alias) 
                    testcase = tp.testcase_create(summary=tc_summary, plan_id=plan_id, author_id=author_id, isautomated=True, category_id=1, case_status_id=2, alias=tc_alias, priority_id=1)
                    logger.debug("testcase : %s" % testcase) 

    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2



if __name__ == "__main__":
    logger.info("Testopia Util (version %s) start" % ver)

    sys.exit(main())

