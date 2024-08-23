# InterfolioPDFgen
Re-processes PDF zip download from Interfolio to generate cover sheets and bundle by keyword.

## What this does:

Interfolio generates PDF bundles, but not in the format we want. We prefer to have cover-sheets
for each applicant and re-bundle the PDFs into a zip file that contains sub-folders based on
a keyword from the application (e.g., Carnegie Fellowship type).

## Installation

Use pip to install:

`pip install InterfolioPDFgen`

## Usage

1. In Interfolio:
   1. Generate a PDF zip file of all the applicants you want to consider. Hint: login as position manager,
      go to position, select all applicants you want, click "Download" and "Zip file".
   2. Generate a report:  login as position manager, to go "Reports", then filter by position name. Select
      all appropriate applicants (you can use other filters, like tags to do this autotmatically). Click
      "Download CSV".
2. With the .zip and .csv files, run the PDF generator command:

   `InterfolioPDFgen [.zip file] [.csv file]`

3. You will end up with a new .zip file that you can share.
