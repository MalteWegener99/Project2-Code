# Tseries File format
- little endian
Header:
- 8byte number of samplse
Sample:
- 8byte long: time
- 8byte double *3: x,y,z
- 8byte double *9: rowmajor covmat

# Tseries.neu File format
- little endian
Header:
- 8byte number of samplse
Sample:
- 8byte long: time
- 8byte double *3: x,y,z
- 8byte double *3: error