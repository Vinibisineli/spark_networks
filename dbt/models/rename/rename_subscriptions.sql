with subscriptions as (

    select
        subscription_id,
        user_id,
        createdAt,
        updatedAt,
        endDate,
        status,
        amount	
    from {{ source('sparknetworks','subscription')}}

)

select * from subscriptions