#!/usr/bin/env python

import xml.etree.ElementTree as ET
import urllib2
import copy
import sys

class NewReleasesTool():
    devkey = #removed    
    limit = 100
    nonsecure__url = #removed
    nonsecure_commerce_url = #removed    
    
    #defining success and failure classes, these will be used to translate into the html display type
    status = {'success':'success', 'failure':'failure', 'warning':'warning', 'allowed':'allowed', 'restricted':'restricted'}
    
    #unfriendly rights flags:
    unfriendly_rights_flags = ["Streamable(2)"]
    
    def int2bin(self, n, count=20):
        """returns the binary of integer n, using count number of digits"""
        return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])
    
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

    def int2bin(self, n, count=20):
        """returns the binary of integer n, using count number of digits"""
        return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])
        
    def returnRightsFlags(self,number):
        try:
            decimal = int(number)
        except:
            return False
        
        binary = self.int2bin(decimal)

        rights_list = []
        
        for i in range(len(binary)-2):
            if i == 1 and binary[-i-1] == '1':
                rights_list.append("Streamable(2)")
            if i == 4 and binary[-i-1] == '1':
                rights_list.append("Portable Tethered Download(16)")
            if i == 5 and binary[-i-1] == '1':
                rights_list.append("Non-Portable Tethered Download(32)")
            if i == 8 and binary[-i-1] == '1':
                rights_list.append("Purchase as part of Album only(256)")
            if i == 9 and binary[-i-1] == '1':
                rights_list.append("Purchase DRM Free(512)")
            if i == 10 and binary[-i-1] == '1':
                rights_list.append("Warner Free Stream(1024)")
                
        return rights_list
    
    def returnFriendlyRightsFlag(self,rights_flag):
        #defaults to restricted
        friendly_flags = {'streamable':self.status['restricted'],
                          }
        eval_flags = self.returnRightsFlags(rights_flag)
        
        for flag in eval_flags:
            if flag == self.unfriendly_rights_flags[0]:
                friendly_flags['streamable'] = self.status['allowed']
                
        return friendly_flags
    
    def parseTrackPrices(self,data):
        pricing = {}
        
        elems = self.getXMLdata(data,'./TrackPricingInfo')
        for elem in elems:
            try:
                pricing[elem.find('trackId').text.lower()] = '$' + elem.find('./prices/MediaEncodingPrice/price/finalPrice').text
            except AttributeError, e:
                pricing[elem.find('trackId').text.lower()] = 'none'
        
        return pricing
    
    def parseAlbumPrice(self,data):
        tree_elem = self.getXMLdata(data,'./prices/MediaEncodingPrice/price/finalPrice')
        try:
            price = '$' + tree_elem[0].text
        except AttributeError, e:
            price = 'none'
        
        return price
        
    def getTrackPriceRawData(self,track_id_list):
        query_string = ''
        
        for id in track_id_list:
            query_string += '&trackIds='
            query_string += id
        try:        
            data = urllib2.urlopen('%sgetTrackPricingInfos.xml?developerKey=%s' % (self.nonsecure_commerce_url,self.devkey + query_string))
            return data
        except:
            print "Unable to get track price data from server.",sys.exc_info()
            return False
        
    def getListenIdRawData(self,id_list):
        query_string = ''
        
        for id in id_list:
            query_string += '&kaniIds='
            query_string += id
        try:        
            data = urllib2.urlopen('%sgetListenId.xml?developerKey=%s' % (self.nonsecure__url,query_string))
            return data
        except:
            print "Unable to get listen id data from server.",sys.exc_info()
            return False
        
    def getAlbumPriceRawData(self,album_id):
        try:
            data = urllib2.urlopen('%sgetAlbumPricingInfo.xml?developerKey=%s&albumId=%s' % (self.nonsecure_commerce_url,self.devkey,album_id))
            return data
        except:
            print "Unable to get album price data from server."
            return False
            
    def parseNewReleasesData(self,data):  #grab album ids from new releases list
        data_list = []
        
        elems = self.getXMLdata(data,'./albums/LiteAlbumMetadata')
        for elem in elems:
            album = {}
            album['albumId'] = elem.getiterator('albumId')[0].text
        
            data_list.append(album)
            
        return data_list
    
    def parseAlbumImages(self,data,tests):
        album_images = {'sizes':{}}
        
        image_elems = self.getXMLdata(data,'./ImageMetadata')
        for elem in image_elems:
            image = {}
            try:
                album_images['sizes'][elem.getiterator('height')[0].text + 'x' + elem.getiterator('width')[0].text] = elem.getiterator('url')[0].text
            except:
                print "Problem getting image elements"
                
        tests.testAlbumImages(album_images)
        
        return album_images,tests
       
    def addPricesToTrackData(self,track_id_list,track_data_dict):
        #grab track prices in one lump call to avoid many calls to 
        price_data = self.getTrackPriceRawData(track_id_list)
        if price_data:
            track_prices = self.parseTrackPrices(price_data)
            
            #loop back around and pick up the prices
            for track_data_item in track_data_dict:
                try:
                    track_data_item['price'] = track_prices[track_data_item['trackId'].lower()]
                except KeyError,e:
                    print "EXCEPTION: Track prices not found, and cannot be attached to albums.", e
                    track_data_item['price'] = "error"
        else:
            for track_data_item in track_data_dict:
                track_data_item['price'] = "error"
            
        return track_data_dict
    
    def parseIdMapperResponse(self,_response,tests):
        string_elems = self.getXMLdata(_response,'string')
        
        if string_elems:
            for elem in string_elems:
                tests.testIdMapper(elem.text)
    
    def addPriceToAlbumData(self,album_id, album_metadata):
        #grab track prices in one lump call to avoid many calls to 
        album_price_data = self.getAlbumPriceRawData(album_id)
        if album_price_data:
            try:
                album_metadata['album_price'] = self.parseAlbumPrice(album_price_data)
            except:
                album_metadata['album_price'] = "none"
                print "exception found in addpricetoalbum"
        else:
            album_metadata['album_price'] = "error"
            
        return album_metadata
        
    def getTracksData(self,track_xml_elems,tests):
        track_data_list = []
        track_id_list = []  #for use with pricing
        track_index_list = []
        
        for elem in track_xml_elems:
            track = {}
            try:
                track['rightFlags'] = elem.getiterator('rightFlags')[0].text
                track['name'] = elem.getiterator('name')[0].text
                track['playbackSeconds'] = elem.getiterator('playbackSeconds')[0].text
                track['trackId'] = elem.getiterator('trackId')[0].text
                track['trackIndex'] = elem.getiterator('trackIndex')[0].text
            except AttributeError, track_error_message:
                tests.testForMissingTrackTags(track)
                print "Error getting attributes for track elements."
            
            track_data_list.append(track)
            track_index_list.append(track['trackIndex'])
            track_id_list.append(track['trackId'].lower())

        #test whether track index shows any missing tracks
        tests.testTrackIndex(track_index_list, len(track_xml_elems))
        tests.testTrackDurations(track_data_list)
        
        #test id mappers
        self.parseIdMapperResponse(self.getListenIdRawData(track_id_list),tests)
            
        #add pricing data
        track_data_list = self.addPricesToTrackData(track_id_list,track_data_list)
        
        return track_data_list,tests

    def parseAlbumData(self,album_id,raw_data, tests):
        album_metadata = {}
        album_metadata['errors'] = {}
        album_metadata['albumId'] = album_id
        album_metadata['releaseId'] = album_id.split('.')[1]
        
        album_tree = ET.ElementTree()
        album_tree.parse(raw_data)
        album_root = album_tree.getroot()

        if tests.testAlbumResponse(album_root):
            track_elems = album_root.findall('./trackMetadatas/LiteTrackMetadata')
            if track_elems:
                album_metadata['tracks'],tests = self.getTracksData(track_elems, tests)
            else:
                tests.markAlbumAsMissingAllTracks()
              
            try:
                album_metadata['albumRights'] = album_root.find('rightFlags').text
                album_metadata['albumId'] = album_root.find('albumId').text
                album_metadata['name'] = album_root.find('name').text
                album_metadata['primaryArtistDisplayName'] = album_root.find('primaryArtistDisplayName').text
                album_metadata['label'] = album_root.find('label').text
                album_metadata['releaseDate'] = album_root.find('releaseDate').text
                album_metadata['shortcut'] = album_root.find('shortcut').text
                album_metadata['artist_shortcut'] = album_root.find('./primaryArtist/shortcut').text
            except AttributeError, e:
                tests.markMissingAlbumTags()
                print "EXCEPTION: Error getting album tags. Could mean a missing 'artist_shortcut'.", e
                
            album_metadata['album_friendly_flags'] = self.returnFriendlyRightsFlag(album_metadata['albumRights'])
            
            #get and test the album images
            album_metadata['images'],tests = self.parseAlbumImages(self.getAlbumImageRawData(album_metadata['albumId']),tests)
            
            #add price info
            album_metadata = self.addPriceToAlbumData(album_id,album_metadata)
            tests.testForMissingAlbumPrice(album_metadata)
            tests.testForMissingTrackPrices(album_metadata)
            
            #id mapper test for album (must make a list first)
            album_id_to_list = [album_id]  #hacking id into 1 item list, to use id mapper function
            self.parseIdMapperResponse(self.getListenIdRawData(album_id_to_list),tests)
            
        return album_metadata, tests


    def getNewReleasesRawData(self):
        data = urllib2.urlopen('%sgetNewReleases.xml?developerKey=%s&filterRightsKey=0&start=0&end=%s' % (self.nonsecure__url,self.devkey,self.limit))
        return data
        
    def getNewReleasesData(self):
        new_releases = self.parseNewReleasesData(self.getNewReleasesRawData())
        return new_releases
    
    def getAlbumRawData(self,albumId):
        album_raw_data = urllib2.urlopen('%sgetAlbum.xml?developerKey=%s&filterRightsKey=0&albumId=%s' % (self.nonsecure__url,self.devkey,albumId))    
        return album_raw_data
    
    def getAlbumImageRawData(self,albumId):
        data = urllib2.urlopen('%sgetImagesForAlbum.xml?developerKey=%s&albumId=%s' % (self.nonsecure__url,self.devkey,albumId))
        return data
        
    def getAlbumData(self,albumId):
        tests = AlbumTests()
        try:
            album_raw_data = self.getAlbumRawData(albumId)
        except:
            tests.markAlbumNotFound()
        
        try:   
            album_metadata,tests = self.parseAlbumData(albumId,album_raw_data,tests)
        except UnboundLocalError,e:
            print "EXCEPTION: Timeout on calls to .", e

        #grab test results
        album_metadata['errors']['missing_album_tags'] = tests.errors['missing_album_tags']
        album_metadata['errors']['missing_images'] = tests.errors['missing_images']
        album_metadata['errors']['missing_tracks'] = tests.errors['missing_tracks']
        album_metadata['errors']['album_found'] = tests.errors['album_found']
        album_metadata['errors']['track_duration'] = tests.errors['track_duration']
        album_metadata['errors']['missing_track_prices'] = tests.errors['missing_track_prices']
        album_metadata['errors']['missing_album_price'] = tests.errors['missing_album_price']
        album_metadata['errors']['id_mapper'] = tests.errors['id_mapper']
        
        print album_metadata
        del tests
        return album_metadata
    
    def tallyErrors(self,album_list):
        tally_dict = {'total_albums':{'type':'info','count':0,'ids':[],'description':'total albums'},
                      'missing_album_tags_failures':{'type':'failure','count':0,'ids':[],'description':'missing 2+ album tags'},
                      'missing_images_failures':{'type':'failure','count':0,'ids':[],'description':'missing 2+ images'},
                      'missing_tracks_failures':{'type':'failure','count':0,'ids':[],'description':'missing tracks'},
                      'albums_missing_failures':{'type':'failure','count':0,'ids':[],'description':'missing albums'},
                      'missing_album_tags_warnings':{'type':'warning','count':0,'ids':[],'description':'missing an album tag'},
                      'missing_images_warnings':{'type':'warning','count':0,'ids':[],'description':'missing 1 image'},
                      'missing_track_prices':{'type':'failure','count':0,'ids':[],'description':'missing track prices'},
                      'missing_album_price':{'type':'failure','count':0,'ids':[],'description':'missing album price'},
                      'cannot_stream':{'type':'failure','count':0,'ids':[],'description':'not streamable'},
                      'track_duration_failure':{'type':'failure','count':0,'ids':[],'description':'missing track duration(s)'},
                      'id_map_failure':{'type':'failure','count':0,'ids':[],'description':'missing id mapper(s)'},
                      }

        for album in album_list:
            tally_dict['total_albums']['count'] += 1
            tally_dict['total_albums']['ids'].append(album['albumId'])
            
            #Is album missing?
            if album['errors']['album_found'] == self.status['failure']:
                tally_dict['albums_missing_failures']['count'] += 1
                tally_dict['albums_missing_failures']['ids'].append(album['albumId'])
            else:                
                #failures
                if album['errors']['missing_album_tags'] == self.status['failure']:
                    tally_dict['missing_album_tags_failures']['count'] += 1
                    tally_dict['missing_album_tags_failures']['ids'].append(album['albumId'])
                if album['errors']['missing_images'] == self.status['failure']:
                    tally_dict['missing_images_failures']['count'] += 1
                    tally_dict['missing_images_failures']['ids'].append(album['albumId'])
                if album['errors']['missing_tracks'] == self.status['failure']:
                    tally_dict['missing_tracks_failures']['count'] += 1
                    tally_dict['missing_tracks_failures']['ids'].append(album['albumId'])
                
                if album['errors']['track_duration'] == self.status['failure']:
                    tally_dict['track_duration_failure']['count'] += 1
                    tally_dict['track_duration_failure']['ids'].append(album['albumId'])
                    
                if album['errors']['id_mapper'] == self.status['failure']:
                    tally_dict['id_map_failure']['count'] += 1
                    tally_dict['id_map_failure']['ids'].append(album['albumId'])
                    
                #warnings
                if album['errors']['missing_album_tags'] == self.status['warning']:
                    tally_dict['missing_album_tags_warnings']['count'] += 1
                    tally_dict['missing_album_tags_warnings']['ids'].append(album['albumId'])
                if album['errors']['missing_images'] == self.status['warning']:
                    tally_dict['missing_images_warnings']['count'] += 1
                    tally_dict['missing_images_warnings']['ids'].append(album['albumId'])
                    
                #rights
                if album['album_friendly_flags']['streamable'] == self.status['restricted']:
                    tally_dict['cannot_stream']['count'] += 1
                    tally_dict['cannot_stream']['ids'].append(album['albumId'])

                #prices
                if album['errors']['missing_track_prices'] == self.status['failure']:
                    tally_dict['missing_track_prices']['count'] += 1
                    tally_dict['missing_track_prices']['ids'].append(album['albumId'])
                if album['errors']['missing_album_price'] == self.status['failure']:
                    tally_dict['missing_album_price']['count'] += 1
                    tally_dict['missing_album_price']['ids'].append(album['albumId'])
        
        #this helps the web page to gray out warnings with 0 messages            
        for failure_items in tally_dict.keys():
            if tally_dict[failure_items]['count'] == 0:
                tally_dict[failure_items]['display'] = 'ignore'
            else:
                tally_dict[failure_items]['display'] = 'display' 
        return tally_dict

    def getAlbumDataForAlbumList(self,album_list):
        album_datas = []
        
        if album_list:
            for album_id in album_list:
                album_datas.append(self.getAlbumData(album_id))
        
        error_tally = self.tallyErrors(album_datas)
        
        return album_datas, error_tally
        
class AlbumTests():
    """Tests object for testing condition of album release failures."""
    image_set_number = 3  #default expected number of images
    errors = {}
    
    #defining success and failure classes, these will be used to translate into the html display type
    status = {'success':'success', 'failure':'failure', 'warning':'warning', 'allowed':'allowed', 'restricted':'restricted'}
    
    important_track_tags = ['rightFlags','name','playbackSeconds','trackId','trackIndex']
                
    def __init__(self):
        #sets default state of album to success, as tests fail the flag is flipped
        self.errors['missing_album_tags'] = self.status['success']
        self.errors['missing_images'] = self.status['success']
        self.errors['missing_tracks'] = self.status['success']
        self.errors['album_found'] = self.status['success']
        self.errors['track_duration'] = self.status['success']
        self.errors['missing_track_prices'] = self.status['success']
        self.errors['missing_album_price'] = self.status['success']
        self.errors['id_mapper'] = self.status['success']

    def testTrackIndex(self,indexes_text,total):
        # if the number of tracks is less than the reported index, FAILURE!!!
        if len(indexes_text) < total:
            self.errors['missing_tracks'] = self.status['failure']
        
        #if the highest track number is larger than the total index, FAILURE!!!
        indexes = []
        for number_text in indexes_text:
            try:
                indexes.append(int(number_text))
            except:
                "There was a problem converting the track indexes to numbers."
        try:
            if max(indexes) > total:
                self.errors['missing_tracks'] = self.status['failure']
        except ValueError, e:
            print "Trying to test a missing album, failure.", e
            self.errors['missing_tracks'] = self.status['failure']

    def markAlbumAsMissingAllTracks(self):
        self.errors['missing_tracks'] = self.status['failure']
        self.errors['track_duration'] = self.status['failure']
        
    def testAlbumImages(self,images_dict):
        number_of_missing_images = self.image_set_number - len(images_dict['sizes'])

        if number_of_missing_images == 0:
            self.errors['missing_images'] = self.status['success']
        elif number_of_missing_images == 1:
            #This is a matter of human perception.  It is only a 'warning' if 1 image is missing.
            #Though really, it is a failure.
            self.errors['missing_images'] = self.status['warning']
        else:
            self.errors['missing_images'] = self.status['failure']

            
    def markMissingAlbumTags(self):
        self.errors['missing_album_tags'] = self.status['failure']
        
    def testForMissingTrackTags(self,track_dict):
        for key in track_dict.keys():
            if not track_dict[key]:
                self.errors['missing_album_tags'] = self.status['failure']
                print "Track is missing tag data."
        for track_tag in self.important_track_tags:
            if track_tag not in track_dict.keys():
                self.errors['missing_album_tags'] = self.status['failure']
                print "Track is missing important tags."
        
    def testAlbumResponse(self,album_root):
        try:
            if album_root.tag != 'exception':
                return True
            else:
                self.errors['album_found'] = self.status['failure']
                print "Exception in Album Response.  Album Not found."
                return False
        except:
            self.errors['album_found'] = self.status['failure']
            return False
        
    def markAlbumNotFound(self):
        self.errors['album_found'] = self.status['failure']
 
    def testTrackDurations(self,track_list):
        for track in track_list:
            if track['playbackSeconds'] == '0':
                self.errors['track_duration'] = self.status['failure']
                break
            
    def testForMissingTrackPrices(self,album):
        missing_track_price = False
        nrtool = NewReleasesTool()
        
        try:
            for track in album['tracks']:
                track_rights = nrtool.returnFriendlyRightsFlag(track['rightFlags'])
                try:
                    if track['price'] in ['none','error'] and track_rights['purchaseable'] == self.status['allowed']:
                        missing_track_price = True
                        break
                except KeyError,e:
                    print "EXCEPTION: Unable to use track price data.", e
                    missing_track_price = True
                    
            if album['album_friendly_flags']['purchaseable'] == self.status['allowed'] and missing_track_price == True:
                self.errors['missing_track_prices'] = self.status['failure']
        except KeyError, track_price_test:
            self.errors['missing_track_prices'] = self.status['failure']
            print "Unable to correlate track prices with tracks.  Inidicates possibility of no tracks in index."
            
        
    def testForMissingAlbumPrice(self,album):
        missing_album_price = False
        try:
            if album['album_price'] in ['none','error']:
                missing_album_price = True
        except KeyError,e:
            print "EXCEPTION: Unable to use album price data.", e
            missing_album_price = True

        if album['album_friendly_flags']['purchase_album'] == self.status['allowed'] and missing_album_price == True:
            self.errors['missing_album_price'] = self.status['failure']
            
    def testIdMapper(self,id_mapper_string):
        if id_mapper_string.find('null') > -1:
            self.errors['id_mapper'] = self.status['failure']