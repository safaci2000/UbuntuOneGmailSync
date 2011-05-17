#!/usr/bin/env python
import atom
import gdata.contacts
import gdata.contacts.service
import ConfigParser
import sys
import optparse


global configM



def PrintFeed(feed):
    for i, entry in enumerate(feed.entry):
      print '\n%s %s' % (i+1, entry.title.text)
      if entry.content:
        print '    %s' % (entry.content.text)
      # Display the primary email address for the contact.
      for email in entry.email:
        if email.primary and email.primary == 'true':
          print '    %s' % (email.address)
      # Show the contact groups that this contact is a member of.
      for group in entry.group_membership_info:
        print '    Member of group: %s' % (group.href)
      # Display extended properties.
      for extended_property in entry.extended_property:
        if extended_property.value:
          value = extended_property.value
        else:
          value = extended_property.GetXmlBlobString()
        print '    Extended Property - %s: %s' % (extended_property.name, value)

def processConfig(config_file):
    global configM
    config = ConfigParser.ConfigParser()
    #Open File
    try:
        config.readfp(open(config_file))
    except:
        print("Configuration file not found")
        sys.exit(2);

    try:
        #read gmail section
        gmail  = {} 
        gmail['user'] = config.get('gmail','user')
        gmail['pass'] = config.get('gmail','pass')
        gmail['source'] = config.get('gmail','source')
        configM['gmail'] = gmail
    except:
        print("Could not read gmail configuration... terminating")
        sys.exit(1)

def main():
   global configM
   configM = {} 

   p = optparse.OptionParser()
   p.add_option('--config', '-c', default="config.ini",help="Specifies a configuration file")

   options, arguments = p.parse_args()

   processConfig(options.config)
   gmail = configM['gmail']
   gd_client = gdata.contacts.service.ContactsService()
   gd_client.email = gmail['user']
   gd_client.password = gmail['pass']
   gd_client.source = gmail['source']
   gd_client.ProgrammaticLogin()

   feed = gd_client.GetContactsFeed()
   PrintFeed(feed)


if __name__ == '__main__':
    main()


