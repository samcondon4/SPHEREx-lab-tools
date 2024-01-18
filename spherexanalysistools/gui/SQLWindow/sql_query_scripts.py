sql_query_commands_dict = {
    'Spectral Cal Between Dates':'''
SELECT scn.*
FROM spherexlab.spectral_cal scn
WHERE scn.datetime BETWEEN '2022-08-29 17:00:00' and '2022-08-30 18:00:00'
ORDER BY scn.datetime desc
    ''',
'Spectral Cal For Specific Detectors': '''
SELECT spe.* from spherexlab.spectral_cal as spe
WHERE spe.fileid = "ID00_18831" OR spe.fileid = "ID00_18832" OR spe.fileid = "ID00_18833"  
ORDER BY spe.datetime desc
    ''',
    'Spectral Cal Between Dates and Wavelengths': '''
SELECT scn.*
FROM spherexlab.spectral_cal scn
WHERE scn.datetime BETWEEN '2022-08-29 17:00:00' and '2022-08-30 18:00:00'
AND scn.meta_mono_wavelength BETWEEN 0.5 AND 0.8
ORDER BY scn.datetime desc
        ''',
    'Spectral Cal Between Dates with Range of Exposure Times': '''
SELECT scn.*
FROM spherexlab.spectral_cal scn
WHERE scn.datetime BETWEEN '2022-08-29 17:00:00' and '2022-08-30 18:00:00'
AND scn.meta_exposure_time BETWEEN 14.99 AND 30.01
ORDER BY scn.datetime desc
        ''',
    'Spectral Cal with Shutter Closed and Minimum Exposure Time': '''
SELECT  scn.* 
FROM  spherexlab.spectral_cal scn 
WHERE scn.meta_mono_shutter = 'closed'
AND scn.meta_exposure_time > 15
ORDER BY datetime desc
''',
    'Spectral Cal + Lockin Averages':'''
SELECT scn.*, SQRT(POW(AVG(rd.lockin_x), 2) + POW(AVG(rd.lockin_y), 2)) AS lockin_out
FROM spherexlab.spectral_cal scn
INNER JOIN reference_detector rd
ON scn.RecordGroup = rd.RecordGroup
AND scn.RecordGroupInd = rd.RecordGroupInd
WHERE scn.proc_comment LIKE "20220926_SpectralCal%"
GROUP BY rd.RecordGroupInd
ORDER BY scn.meta_mono_wavelength asc
    ''',
    'Lockin Averages':'''
SELECT SQRT(POW(AVG(rd.lockin_x), 2) + POW(AVG(rd.lockin_y), 2)) AS lockin_out
FROM spherexlab.reference_detector rd
GROUP BY rd.RecordGroupInd
    ''',
    'PYHK Average Pressure and Temperature':'''
SELECT avg(pre.pt_20avg_20low) as avg_pt_20avg_20low,
       avg(pre.pt_20avg_20delta) as avg_pt_20avg_20delta,
       avg(pre.pt_20avg_20high) as avg_pt_20avg_20high,
       avg(tem.80k_20plate) as avg_80k_20plate,
       avg(tem.80k_20head) as avg_80k_20head,
       avg(tem.20k_20plate) as avg_20k_20plate,
       avg(tem.20k_20head) as avg_20k_20head
FROM blue.pressure as pre
INNER JOIN blue.temperature tem
ON pre.recordgroup = tem.recordgroup
AND pre.recordgroupind = tem.recordgroupind
WHERE tem.datetime BETWEEN '2022-08-29 17:00:00' and '2022-08-30 18:00:00'
GROUP BY pre.recordgroupind
    ''',
    'Spectral Cal + Blue':'''
SELECT spe.meta_miscval, spe.filename , avg(pre.datetime) as avg_datetime, avg(pre.PT_20Avg_20Low) as avg_PT_20Avg_20Low, avg(pre.PT_20Avg_20Delta) as avg_PT_20Avg_20Delta, avg(pre.PT_20Avg_20High) as avg_PT_20Avg_20High, avg(pre.Vacuum_20Shell) as avg_Vacuum_20Shell, avg(tem.datetime) as avg_datetime, avg(tem.PT_20H20_20Out) as avg_PT_20H20_20Out, avg(tem.PT_20H20_20In) as avg_PT_20H20_20In, avg(tem.20K_20Plate) as avg_20K_20Plate, avg(tem.PT_20Helium) as avg_PT_20Helium, avg(tem.80K_20Plate) as avg_80K_20Plate, avg(tem.PT_20Oil) as avg_PT_20Oil, avg(tem.80K_20Head) as avg_80K_20Head, avg(tem.20K_20Head) as avg_20K_20Head
FROM spectral_cal spe
INNER JOIN green.temperature tem ON spe.RecordGroup = tem.RecordGroup AND spe.RecordGroupInd = tem.RecordGroupInd 
INNER JOIN green.pressure pre ON tem.RecordGroup = pre.RecordGroup AND tem.RecordGroupInd = pre.RecordGroupInd 
WHERE fileid='id00_18831'
GROUP BY tem.RecordGroupInd
ORDER BY spe.meta_mono_wavelength asc 
'''
}