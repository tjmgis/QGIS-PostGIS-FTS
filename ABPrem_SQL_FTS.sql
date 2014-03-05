DROP TABLE IF EXISTS abpremium.dp_geo;
CREATE TABLE abpremium.dp_geo AS SELECT
b.uprn,
b.logical_status as blpu_logical_status,
l.logical_status as lpi_logical_status,
b.blpu_state,
b.parent_uprn,
b.rpc,
b.local_custodian_code,
b.start_date,
b.postal_address,
b.multi_occ_count,
d.rm_udprn,
d.postcode_type,
l.usrn,
l.level,
/*
Concatenate a single DELIVERY POINT (i.e. Royal Mail PAF) address line label
*/
--Concatenate single Royal Mail Delivery Point address label
(
  case
  when department_name != '' then department_name || ', ' else '' end
  || case when organisation_name != '' then organisation_name || ', ' else '' end
  || case when sub_building_name != '' then sub_building_name || ', ' else '' end
  || case when building_name != '' then building_name || ', ' else '' end
  || case when building_number is not null then building_number::varchar(4) || ', ' else '' end
  || case when po_box_number  != '' then 'PO BOX '||po_box_number::varchar(4)||', ' else '' end
  || case when dependent_thoroughfare_name != '' then dependent_thoroughfare_name || ', ' else '' end
  || case when throughfare_name != '' then throughfare_name || ', ' else '' end
  || case when double_dependent_locality != '' then double_dependent_locality || ', ' else '' end
  || case when dependent_locality != '' then dependent_locality || ', ' else '' end
  || case when post_town != '' then post_town || ', ' else '' end
  || postcode
) AS dp_address,


/*
Concatenate a single GEOGRAPHIC address line label

This code takes into account all possible combinations os pao/sao numbers and suffixes
*/
case when o.organisation != '' then o.organisation||', ' else '' end
--Secondary Addressable Information-------------------------------------------------------------------------------------------------------
||case when l.sao_text != '' then l.sao_text||', ' else '' end
--case statement for different combinations of the sao start numbers (e.g. if no sao start suffix)
||case when l.sao_start_number is not null and l.sao_start_suffix = '' and l.sao_end_number is null then l.sao_start_number::varchar(4)||', '
    when l.sao_start_number is null then '' else l.sao_start_number::varchar(4)||'' end
--case statement for different combinations of the sao start suffixes (e.g. if no sao end number)
||case when l.sao_start_suffix != '' and l.sao_end_number is null then l.sao_start_suffix||', '
    when l.sao_start_suffix != '' and l.sao_end_number is not null then l.sao_start_suffix else '' end
--Add a '-' between the start and end of the secondary address (e.g. only when sao start and sao end)
||case when l.sao_end_suffix != '' and l.sao_end_number is not null then '-'
        when l.sao_start_number is not null and l.sao_end_number is not null then '-' else '' end
--case statement for different combinations of the sao end numbers and sao end suffixes
||case when l.sao_end_number is not null and l.sao_end_suffix = '' then l.sao_end_number::varchar(4)||', '
        when l.sao_end_number is null then '' else l.sao_end_number::varchar(4) end
--pao end suffix
||case when l.sao_end_suffix != '' then l.sao_end_suffix||', ' else '' end
--Primary Addressable Information----------------------------------------------------------------------------------------------------------
||case when l.pao_text != '' then l.pao_text||', ' else '' end
--case statement for different combinations of the pao start numbers (e.g. if no pao start suffix)
||case when l.pao_start_number is not null and l.pao_start_suffix = '' and l.pao_end_number is null then l.pao_start_number::varchar(4)||', '
    when l.pao_start_number is null then '' else l.pao_start_number::varchar(4)||', ' end
--case statement for different combinations of the pao start suffixes (e.g. if no pao end number)
||case when l.pao_start_suffix != '' and l.pao_end_number is null then l.pao_start_suffix||', '
    when l.pao_start_suffix != '' and l.pao_end_number is not null then l.pao_start_suffix else '' end
--Add a '-' between the start and end of the primary address (e.g. only when pao start and pao end)
||case when l.pao_end_suffix != '' and l.pao_end_number is not null then '-'
    when l.pao_start_number is not null and l.pao_end_number is not null then '-' else '' end
--case statement for different combinations of the pao end numbers and pao end suffixes
||case when l.pao_end_number is not null and l.pao_end_suffix = '' then l.pao_end_number::varchar(4)||', '
        when l.pao_end_number is null then '' else l.pao_end_number::varchar(4) end
--pao end suffix
||case when l.pao_end_suffix != '' then l.pao_end_suffix||', ' else '' end
--Street Information----------------------------------------------------------------------------------------------------------------------------
||case when s.street_descriptor != '' then s.street_descriptor||', ' else '' end
--Locality------------------------------------------------------------------------------------------------------------------------------------------
||case when s.locality_name != '' then s.locality_name||', ' else '' end
--Town---------------------------------------------------------------------------------------------------------------------------------------------
||case when s.town_name != '' then s.town_name||', ' else '' end
--Postcode----------------------------------------------------------------------------------------------------------------------------------------
||case when b.postcode_locator != '' then b.postcode_locator else '' end
AS geo_address,
b.geom,
b.x_coordinate,
b.y_coordinate

FROM
addressbasepremium_epoch19.abp_blpu_record AS b full outer join addressbasepremium_epoch19.abp_delivery_point AS d on (b.uprn = d.uprn),
addressbasepremium_epoch19.abp_street_descriptor AS s,
addressbasepremium_epoch19.abp_lpi AS l full outer join addressbasepremium_epoch19.abp_organisation AS o on (l.uprn = o.uprn)
WHERE b.uprn = l.uprn
AND l.usrn = s.usrn
AND l.language = s.language;

--Time taken: 972818 ms


select pg_size_pretty(CAST((SELECT
SUM(pg_total_relation_size(table_schema || '.' || table_name) )
FROM information_schema.tables
WHERE table_schema = 'abpremium') As bigint) )  As tables_schema_size

SELECT * FROM addressbasepremium_epoch19.abp_lpi WHERE uprn ='60028242';

--size no indexes - "8766 MB"

CREATE INDEX dp_geo_geom_idx ON abpremium.dp_geo USING GIST (geom);
--Time taken: 572188 ms
--size no indexes - "10Gb"

ALTER TABLE abpremium.dp_geo ADD COLUMN dp_fts tsvector;

UPDATE abpremium.dp_geo SET dp_fts = to_tsvector('english', dp_address);
--Time taken:1988022 ms
--size no indexes - "23Gb"


CREATE INDEX dp_geo_dp_fts_tsvector_gin_idx ON abpremium.dp_geo USING GIN(dp_fts);
--Time taken: 373651 ms
--size no indexes - "25Gb"

SELECT * FROM abpremium.dp_geo WHERE dp_fts @@ plainto_tsquery('english', 'Redford')
