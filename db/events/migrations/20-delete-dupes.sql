-- remove duplicate entries before creating the unique constraint
with a as (select id,
row_number() over(partition by title, organization_id, geocode_id, start_time, end_time) as r
from events.event)
delete from events.event e 
where e.id in (select id from a where a.r > 1);
