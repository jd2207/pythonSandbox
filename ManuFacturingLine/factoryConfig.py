'''
Provides a class to represent the factory flow configuration and associated parsing '''

from xml.dom import minidom

# ----------------------------------------
# Non instance functions for XML parsing
# ----------------------------------------

def fetchNodeValue( node, name ):
  if node.hasChildNodes():
    for child in node.childNodes:
      if child.nodeName == name:
        return child.firstChild.nodeValue    
  return None
        
def fetchNode( node, name ):
  if node.hasChildNodes():
    for child in node.childNodes:
      if child.nodeName == name:
        return child    
  return None        
        
def fetchNodeList( node, name ):
  nlist = []
  if node.hasChildNodes():    
    for child in node.childNodes:
      if child.nodeName == name:
        nlist.append( child )    
  if len(nlist) > 0:
    return nlist    
  return None

# -----------------------------------------------------------------
#  Base class for XML nodes which are menu-able
# -----------------------------------------------------------------

class factoryXMLparser(object) :
    
  def __init__( self ):
    self.descriptionKey = "description"
    self.name = None
    self.subClassName = None
    self.attribs = { 'id' : 'id' }

#    def itemsFromXML(self, xml):
#        config = minidom.parse(xml).getElementsByTagName('nvpn')
#        return self.itemsFromXMLNode(config)

  def itemsFromXML(self, xml, tag):
    config = minidom.parse(xml).getElementsByTagName(tag)
    return self.itemsFromXMLNode(config)

  def itemsFromXMLNode(self,nodeList):
#    
#   Takes an XMLnode and returns a dictionary of the form:
#         { 'id1' :  { 'description' : 'description1 text',
#                      'subItem'  : list or value
#                      'attribute1' : 'attribute1 value',
#                      'attribute2' : 'attribute2 value'
#                       ...
#                    }
#         }
#
#   The XML node must have one of two forms:
#
#   <node>
#        value
#   </node>
#
#    OR 
#
#   <node self.attribs['id'] = "id1" self.attribute1 = attribute1 self.attribute2 = attribute2  ... >
#            <self.descriptionKey = 'description1 text'>
#            <self.subClassName> node </self.subClassName>
#            <self.subClassName> node </self.subClassName>
#            <self.subClassName> node </self.subClassName>
#            ... 
#   </node>        
#        
    mlist = {}
    if not nodeList == None :
      for node in nodeList:
        id = node.getAttribute( self.attribs ['id'] )
        mlist[ id ] = {}

        desc = fetchNodeValue( node, self.descriptionKey  )
        if not desc == None:
          mlist[ id ][ "description" ] = desc 

        for attrib in self.attribs.iterkeys():
          if not attrib == 'id': 
            mlist [ id ] [ attrib ] = node.getAttribute( attrib )
                
        if not self.subClassName == None:
          module = __import__("factoryConfig")
          subItemClass = getattr(module, self.subClassName)
          subItem = subItemClass()
          subNodeList = fetchNodeList( node, subItem.name )
          mlist[ id ][ 'subItem' ] = subItem.itemsFromXMLNode( subNodeList ) 

        else:
          mlist [ id ] = node.firstChild.nodeValue

    return mlist

# -----------------------------------------------------------------
#  Specialist classes derived from base MenuList class
# -----------------------------------------------------------------

class nvpnsParser (factoryXMLparser) :
  def __init__ (self):
    super(nvpnsParser,self).__init__()
#        self.name = 'nvpn'
    self.subClassName = 'stationsParser'
    self.attribs [ 'productName' ] = 'productName'
    self.attribs [ 'fuseImage' ] = 'fuseImage'
    
class stationsParser (factoryXMLparser): 
  def __init__ (self):
    super(stationsParser,self).__init__()
    self.name = 'station'
    self.subClassName = 'operationsParser'
    self.attribs [ 'id' ] = 'name'
           
class operationsParser (factoryXMLparser): 
  def __init__ (self):
    super(operationsParser,self).__init__()
    self.name = 'operation'
    self.subClassName = 'operationOptionsParser'
    self.attribs [ 'id' ] = 'class'
    self.attribs [ 'order' ] = 'order'
               
class operationOptionsParser (factoryXMLparser):
  def __init__ (self):
    super(operationOptionsParser,self).__init__()
    self.name = 'option'
    self.attribs [ 'id' ] = 'name'


# ---------------------------------------------------------------
# Testing
# ---------------------------------------------------------------

if __name__ == "__main__":

  testXML = 'factoryFlow.xml'
  nvpns = nvpnsParser().itemsFromXML( testXML, 'nvpn')

# Print nvpns and stations
  for i in nvpns.iterkeys():
    print 'NVPN: %s Desc: %s (ProdName = %s)' % (i, nvpns[i]['description'], nvpns[i]['productName'])  
    stations = nvpns [ i ]['subItem']
    for j in stations.iterkeys():
      print '\t' + 'station: %s (%s)' % (j, stations[j]['description'])  
      operations = stations [ j ]['subItem']
      for k in operations.iterkeys():
        print '\t\t' + 'operation: %s order= %s' % (k, operations[k]['order'])
        options = operations[k]['subItem']
        for l in options.iterkeys():
          print '\t\t\t' + 'option: %s = %s' % (l, options[l])  
  
  print 'done'






