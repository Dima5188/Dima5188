{{
config(
    max_updated_at='select max(batch_datetime) from dwh_dev.dima_operator_test'
)
}}

select
    a.*
from gold_production.dwh_dev.dima_operator_test a
left join silver_production.main.merchants m on a.id = m.id

where 1=1

{% if is_incremental %}
      and a.batch_date >= {{ date_frame }}
      and a.batch_datetime >= {{ max_updated }}
{% endif %}

qualify row_number() over (partition by a.id order by a.batch_datetime desc) = 1