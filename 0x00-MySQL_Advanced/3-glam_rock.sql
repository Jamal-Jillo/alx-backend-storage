-- Name: 3-glam_rock.sql
SELECT band_name, 
       EXTRACT(YEAR FROM AGE(split, formed)) AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;
