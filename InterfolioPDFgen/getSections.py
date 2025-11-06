"""
This library uses table of contents (TOC) information to extract
specific parts. Interfolio injects these when compiling applications
into a single PDF
"""

def outline_dict(r):
    # recursively get the TOC as a list of sections
    result = []
    for item in r.outline:
        if isinstance(item, list):
            # recursive call
            l = outline_dict(item)
            result += l
        else:
            pageNum = r.get_destination_page_number(item) 
            result.append((pageNum,item['/Title']))
    return result


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Given a downloaded zip file of PDFs"\
                            " extract an anonymized section.")
    parser.add_argument("PDFzip", help="zip file with one PDF per applicant")
    #parser.add_argument("CSV", help="CSV Report file with IDs and names")
    parser.add_argument("-section", help="Which section to extract (integer "\
                        "indexed from 1)",
                        type=int, default=3)
    parser.add_argument("-secname", help="Name of the section to be extracted",
                        default="Research")
    parser.add_argument("-exdir", help="Output directory for extracted PDFs",
                        default='Extracted')
    parser.add_argument("-outdir", help="Output directory for whole PDFs",
                        default='Originals')
    parser.add_argument('-v', help='Verbose output', action="store_true")
    args = parser.parse_args()
    
    import zipfile, sys, os
    import PyPDF2
    from glob import glob
    import re

    if args.section < 1:
        print("Error:  you must chose a section number > 1")
        sys.exit(1)

    # Make working folders and extract PDFs
    if os.path.isdir(args.outdir) or os.path.isdir(args.exdir):
        print("Error:  outdir and exdir directories exist already.")
        print("   Save and/or delete them before using this script")
        sys.exit(1)
    os.mkdir(args.outdir)
    os.mkdir(args.exdir)
    # Extract the original PDFs
    with zipfile.ZipFile(args.PDFzip, 'r') as zipf:
        zipf.extractall(path=args.outdir)
    files = glob(os.path.join(args.outdir,"*.pdf"))
    
    for j,file in enumerate(files):
        # Extract the unique user ID from the pdf file name
        ID = file.split("_")[-1].split('.')[0]
        r = PyPDF2.PdfReader(file)
        w = PyPDF2.PdfWriter()
        l = outline_dict(r)
        if args.v: 
            print("Processing file {}".format(file))
            print("   {} sections".format(len(l)))
        if args.section >= len(l):
            print("Warning:  file {} only has {} sections... skipping".format(
                file, len(l)))
            continue
        start = l[args.section-1][0]
        stop = l[args.section][0]
        for i in range(start,stop):
           page = r.pages[i]
           w.add_page(page)
        efile = "{}{}.pdf".format(args.secname, ID)
        outfile = os.path.join(args.exdir, efile)
        with open(outfile, "wb") as fout:
            w.write(fout)
        #os.rename(file, os.path.join(args.outdir,ofile))
       
    