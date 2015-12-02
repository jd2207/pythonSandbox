import csv
class productionDeviceData(dict):
  ''' Class extends dictionary corresponding to the device IMEI lookup table'''
   
  def __init__(self, CSVfileName):
    dataFile = open(CSVfileName, mode='r')
    reader = csv.reader(dataFile)

    first = True
    for row in reader:      # first row is a header of column names
      if first: 
        colNames = row
        first = False
        self[ 'header' ] = colNames
      else:
        colsDict = {}
        for i in range(1,len(row)):
          colsDict[ colNames[i] ] = row[i]    
          self[ row[0].strip("'") ] = colsDict

if __name__ == '__main__':
  strFormat = '%15s %10s %36s %36s'
  pdd = productionDeviceData('production_files.csv')
  print strFormat % tuple( pdd['header'] )

  for dev in pdd.iterkeys():
    if not dev == 'header': 
      print strFormat % ( dev, pdd[dev]['DEVICE_FID'], pdd[dev]['DeviceConfig Filename'], pdd[dev]['IMEI Filename']) 
  
  print 'done'
  
