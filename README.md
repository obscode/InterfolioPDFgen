# InterfolioPDFgen
Re-processes PDF zip downloads from Interfolio into different formats/bundles for the Committee.
Currently there are two scripts:  `InterfolioPDFgen` and `ExtractSection`. Both are outlined 
below.

## InterfolioPDFgen:

Interfolio generates PDF bundles, but not in the format we want. We prefer to have cover-sheets
for each applicant and re-bundle the PDFs into a zip file that contains sub-folders based on
a keyword from the application (e.g., Carnegie Fellowship type).

## ExtractSection:

This script extracts a particular section from each of the bundled PDFs downloaded from Interfolio.
The idea is that one section (Research statement, e.g.) is anonymized, so should be extracted with
no identifying information (only the user ID number).

# Installation

Downdload to your local disk and use pip to install:

`git clone https://github.com/obscode/InterfolioPDFgen`

`cd InterfolioPDFgen`

`pip install .`

## Usage

1. **InterfolioPDFgen**:
   1. Generate a PDF zip file of all the applicants you want to consider. Hint: login as position manager,
      go to position, select all applicants you want, click "Download" and "Zip file".
   2. Generate a report:  login as position manager, to go "Reports", then filter by position name. Select
      all appropriate applicants (you can use other filters, like tags to do this autotmatically). Click
      "Download CSV".
   3. With the .zip and .csv files, run the PDF generator command:

     `InterfolioPDFgen [-subkey subkey] [-outzip outzip] zipfile csvfile`

   4. You will end up with a new .zip file that you can share.
  
2. **ExtractSection**
   1. Generate a PDF zip file of all the applicants you want to consider. Hint: login as position manager,
      go to position, select all applicants you want, click "Download" and "PDF file". Note this is sligtly
      different than the procedure for `InterfolioPDFgen`
   2. With the .zip file, run the extractor command:

      `ExtractSection [-section #] [-secname SECNAME] [-exdir EXDIR] [-outdir OUTDIR] zipfile`

      You can specify which section with the `-section` argument.

   3. The output sections will be saved as separate PDFs in the `EXDIR` folder (default `Extracted`)
      with filenames constructed as: `SECNAME+ID.pdf` where the `ID` is the applicant's Interfolio ID number.
   4. The original PDFs are saved in the `OUTDIR` folder (default `Originals`) and have filenames that
      are constructed of the applicant's first and last names and user ID.
