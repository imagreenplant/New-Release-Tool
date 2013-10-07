#!/usr/bin/env python

import xml.etree.ElementTree as ET
import urllib2


class BuildStatus():
    """Library for grabbing status."""
    
    def getXMLdata(self,data,tag):
        try:
            tree = ET.ElementTree()
            tree.parse(data)
            root = tree.getroot()
            xml_data = root.findall(tag)
            return xml_data
        except ExpatError, a:
            return a
        except:
            return False

    def getXMLRootChildren(self,data):
        try:
            toplevel = ET.ElementTree()
            toplevel.parse(data)
            root = toplevel.getroot()
            children_data = root.getchildren()
            return children_data
        except:
            print "Exception in getXMLChildren function"
            return False
        
    def getStatusRawData(self):
        try:        
            data = urllib2.urlopen('******')
            return data
        except:
            print "Unable to get listen id data from server.",sys.exc_info()
            return False
    
    def parseStatus(self):
        sandbox_response = self.getStatusRawData()
        
        try:
            server_status = self.getXMLdata(sandbox_response,'./groups/group/members/server')
            return server_status
        except:
            print " Status seems to have an error.  Please check back later."
            return False
        
    def getStatus(self):
        _raw_data = self.parseStatus()
        
        problem_servers = {}
        _info = {}
        for server in _raw_data:
            for cache_state in server.getchildren():
                if cache_state.text.lower() == "out of date":
                    if cache_state.items()[0][1] in problem_servers.keys():
                        problem_servers[cache_state.items()[0][1]].append(server.items()[0][1])
                    else:
                        problem_servers[cache_state.items()[0][1]] = [server.items()[0][1]]
                    
        counter = {}
        for cache_type in problem_servers.keys():
            counter[cache_type] = len(problem_servers[cache_type])
            
        _info['problem_servers'] =  problem_servers
        _info['count'] = counter
        _info['total_tested'] = len(_raw_data)
        
        return _info

    def getBuildRawData(self):
        try:        
            data = urllib2.urlopen('******')
            return data
        except:
            print "Unable to get build status data from server.",sys.exc_info()
            return False
        
    def getBuildStatus(self):
        _response = self.getBuildRawData()
        _xml_data = self.getXMLRootChildren(_response)

        _data = {}
        for xml_element in _xml_data:
            _data[xml_element.tag] = xml_element.text
            
        return _data

