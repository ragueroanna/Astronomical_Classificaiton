source:
https://skyserver.sdss.org/dr17/SearchTools/sql

SQL:
-- This query does a table JOIN between the imaging (PhotoObj) and spectra
--(SpecObj) tables and includes the necessary columns in the SELECT to upload
--the results to the SAS(Science Archive Server) for FITS file retrieval.
SELECT TOP 100000
p.objid,p.ra,p.dec,p.u,p.g,p.r,p.i,p.z,
p.run, p.rerun, p.camcol, p.field,
s.specobjid, s.class, s.z as redshift,
s.plate, s.mjd, s.fiberid
FROM PhotoObj AS p
JOIN SpecObj AS s ON s.bestobjid = p.objid
WHERE 
  p.u BETWEEN 10.99 AND 32.8
  AND g BETWEEN 10.49 AND 31.61
  AND p.i BETWEEN 9.45 AND 32.15
  AND p.z BETWEEN 9.6 AND 29.39
  AND s.z BETWEEN -0.0099 AND 7.012
  AND s.mjd BETWEEN 51607 AND 58933

SQL:
-- This query does a table JOIN between the imaging (PhotoObj) and spectra
--(SpecObj) tables and includes the necessary columns in the SELECT to upload
--the results to the SAS(Science Archive Server) for FITS file retrieval.
SELECT TOP 500000
p.objid,p.ra,p.dec,p.u,p.g,p.r,p.i,p.z,
p.run, p.rerun, p.camcol, p.field,
s.specobjid, s.class, s.z as redshift,
s.plate, s.mjd, s.fiberid
FROM PhotoObj AS p
JOIN SpecObj AS s ON s.bestobjid = p.objid
WHERE 
  p.u BETWEEN 10.99 AND 32.8
  AND g BETWEEN 10.49 AND 31.61
  AND p.i BETWEEN 9.45 AND 32.15
  AND p.z BETWEEN 9.6 AND 29.39
  AND s.z BETWEEN -0.0099 AND 7.012
  AND s.mjd BETWEEN 51607 AND 58933