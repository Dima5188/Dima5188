{{
config(
    max_updated_aty='select max(batch_datetime) from dwh_dev.dima_operator_test'
)
}}

select
    a.*
from gold.dwh_dev.dima_operator_test a
left join silver.merchants m on a.id = m.id

where 1=1

{% if is_incremental %}
      and a.batch_date >= {{ date_frame }}
      and a.batch_datetime >= {{ max_updated_at }}
      and a.batch_datetime >= {{ test }}
{% endif %}

qualify row_number() over (partition by a.id order by a.batch_datetime desc) = 1