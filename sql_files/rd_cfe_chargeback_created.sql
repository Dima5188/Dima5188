select
       kafka_headers_event_meta.id                                                           as event_id,
       bigint(_eventContext.subjectIdentifier)                                               as chargeback_id,
       _eventContext.requestId                                                               as request_id,
       case when _eventContext.foreignEntity.entityType = 'order'
            then _eventContext.foreignEntity.entityId else null end                          as order_id,
       _eventContext.initiator                                                               as initiator,
       _eventContext.initiatorId                                                             as initiator_id,
       bigint(m.id)                                                                          as merchant_id,
       cfe._eventContext.shopUrl                                                             as shop_url,
       kafka_headers_event_meta.domain                                                       as domain_name,
       kafka_headers_event_meta.eventType                                                    as event_type,
      'created'                                                                              as event_name,
       timestamp_millis(_eventContext.eventTimestamp)                                        as event_timestamp,
       _eventContext.eventTimestamp                                                          as event_at,
       date(timestamp_millis(_eventContext.eventTimestamp))                                  as event_date,

       timestamp_millis(cfe.datalake_bronze_created_at)                                      as batch_updated_at,
       date(timestamp_millis(cfe.datalake_bronze_created_at))                                as batch_date,
       current_timestamp()                                                                   as dwh_updated_at

from bronze_production.main.cfe_chargeback_created_rc_b cfe
    left join silver_production.main.merchants m on lower(cfe._eventContext.shopUrl) = lower(m.shop_url)

where cfe.date >= '2024-05-01'
and cfe._eventContext.shopUrl not in ('test.pass.com', 'test_pre_sync.com', 'drorit.com')

{% if is_incremental() %}

and cfe.date >= {% date_frame %}

{% endif %}

qualify row_number() over (partition by _eventContext.subjectIdentifier,_eventContext.requestId order by cfe._eventContext.eventTimestamp desc) = 1