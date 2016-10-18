#   KiCAD BOM to CSV converter

This is a Python 3 program to convert KiCAD Bills of Materials to a CSV format suitable
for uploading to major part distributors including Digi-Key and Mouser.

#   Usage

To use this program, each item in a KiCAD schematic needs some additional information for ordering.
The suggested information is:

    Mfgr        Manufacturer (TI, etc.)
    Part        Manufacturer part number
    Vendor      Vendor name (Mouser, etc.)
    Vendorpart  Vendor's part number
    
You can use any names; they just have to be consistent.
    
Use the BOM icon button in KiCAD's schematic editor to generate a BOM file with
an XML suffix. No filters are required.
    
 Run the program as follows:
 
    python3 kicadbomtovendor.py  --split Vendor BOMFILE.xml 
    
This will generate one .csv file for each different value of "Vendor".  The files are
generated in the same directory as the XML input file.

The output .csv files contain column headers and one line for each part.  Multiple
instances of the same part are combined into one line, with the quantity column updated
appropriately. The "REF" column will contain all the schematic instances using that
part number.

These files are acceptable to the BOM uploaders for both DigiKey and Mouser.
Once uploaded, the parts can be ordered.
    
