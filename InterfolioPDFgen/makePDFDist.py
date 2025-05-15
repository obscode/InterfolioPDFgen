'''
makePDFDist
Author:  Chris Burns <cburns@carnegiescience.edu>
Purpose:  Make cover sheets for PDFs downloaded from Interfolio and bundle
          them into a .zip file with optional folder hierarchy.
'''
from argparse import ArgumentParser
import sys

def main():
   parser = ArgumentParser(description="Generate cover sheets for PDFs from"\
         " Interfolio and bundle them into a new .zip file")
   parser.add_argument('PDFzip', help="The .zip file containing the PDFs")
   parser.add_argument('reportcsv', 
                       help="The .csv file containing the meta data")
   parser.add_argument('-subkey', help="Optional field in the reportcsv that "\
         "will be used to make sub-folders in the resulting .zip file",
                       default=None)
   parser.add_argument('-outzip', help="The name of the output .zip file. "\
         "Default is to append 'out.zip' to PDFzip", default=None)
   args = parser.parse_args()
   
   # Check for modules that are not usually shipped with anaconda
   try:
      from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
      from reportlab.platypus import TableStyle
      from reportlab.lib.styles import getSampleStyleSheet
      from reportlab.rl_config import defaultPageSize
      from reportlab.lib.units import inch
   except:
      print("Error. This scripts requires reportlab > 4.0.0. You can install it")
      print("using 'pip install reportlab>=4.0.0'")
      sys.exit(1)
   
   try:
      from PyPDF2 import PdfMerger
   except:
      print("Error. This scripts requires pyPDF2 > 2.10.0. You can install it")
      print("using 'pip install reportlab>=2.10.0'")
      sys.exit(1)
   
   
   import csv, os
   import glob
   import zipfile
   import tempfile
   
   PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
   styles = getSampleStyleSheet()
   
   def getField(field, data, header, missing=""):
      '''Search for a given in field in the CSV data. If the field does not
      exist or the value is empty, return [missing]'''
      if field not in header:
         return missing
      value = data[header.index(field)]
      if not value:  return missing
      return value
   
   if not os.path.isfile(args.PDFzip):
      print("Error:  file not found {}".format(args.PDFzip))
      sys.exit(1)
   
   if not os.path.isfile(args.reportcsv):
      print("Error:  file not found {}".format(args.reportcsv))
      sys.exit(1)
   
   with open(args.reportcsv, 'r') as csvfile:
      reader = csv.reader(csvfile, quotechar='"')
      data = []
      for row in reader:
         data.append(row)
   
   headers = data[0]
   data = data[1:]
   
   # If subkey is specified, check it exists in the .csv file
   if args.subkey:
      if args.subkey not in headers:
         print("Error: you asked for sorting by {}, but the .csv file does "\
               "not have that field".format(args.subkey))
         sys.exit(1)
   
   # We'll do all the work in a temporary folder
   with tempfile.TemporaryDirectory() as tmpdir:
      PDFs = os.path.join(tmpdir, "PDFs"); os.mkdir(PDFs)
      merged = os.path.join(tmpdir,"merged"); os.mkdir(merged)
      covers = os.path.join(tmpdir,"covers"); os.mkdir(covers)
   
      # Extract the original PDFs
      with zipfile.ZipFile(args.PDFzip, 'r') as zipf:
         zipf.extractall(path=PDFs)
   
      # Open new zip file for the results
      if args.outzip is None:
         outzip = args.PDFzip + "_out.zip"
      else:
         outzip = args.outzip
      with zipfile.ZipFile(outzip, "w") as fout:
   
         # Now make our way through the applicants
         for row in data:
            title = row[headers.index('Firstname')] + " " + \
                  row[headers.index('Lastname')]
            # Make an address string with newlines
            fulladdr = ""
            addr = getField('Address', row, headers)
            if addr:  fulladdr += addr + "<br/>"
            addr2 = getField('Address2', row, headers)
            if addr2: fulladdr += addr2 + "<br/>"
            city = getField('City', row, headers)
            if city: fulladdr += city
            state = getField('State', row, headers)
            if state: fulladdr += ', ' + state
            zipcode = getField('Zip', row, headers)
            if zipcode: fulladdr += ', ' + zipcode
            country = getField('Country', row, headers)
            if country: fulladdr += '<br/>' + country
         
            tdata = [['Address:', Paragraph(fulladdr)]]
         
            fields = ['Email','Telephone','Highest degree','Highest degree date',
                      'Highest degree school']
            for field in fields:
               tdata.append([field, getField(field, row, headers,
                                             missing="Not provided")])
         
            ID = getField('\ufeffId', row, headers)  # Weird
            coverfile = os.path.join(covers, "cover_{}.pdf".format(ID))
            cover = SimpleDocTemplate(coverfile)
            story = [Paragraph(title, styles['Title'])]
            story.append(Spacer(1,0.2*inch))
            tab = Table(tdata)
            tab.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), "TOP")]))
            story.append(tab)
            story.append(Spacer(1,0.2*inch))
            status = getField('Completeness level', row, headers)
            if status:
               story.append(Paragraph("<B>Application Status:</B> " + status))
            cover.build(story)
         
            pdf = glob.glob(os.path.join(PDFs, '*'+ID+'*.pdf'))
            if len(pdf) != 1:
               print("Error, no PDF found for {} ({})".format(title,ID))
               continue
            pdf = pdf[0] 
            merger = PdfMerger()
            merger.append(coverfile)
            merger.append(pdf)
            merger.write(os.path.join(merged,os.path.split(pdf)[-1]))
         
            # Write the PDF to the zipfile
            if args.subkey:
               keyval = getField(args.subkey, row, headers)
            else:
               keyval = ""
            zipfilename = os.path.join(keyval, os.path.split(pdf)[-1])
            fout.write(os.path.join(merged,os.path.split(pdf)[-1]), 
                    arcname=zipfilename)
   
         
