with messages as (

    select
        message_id,
        createdAt,
        reciverId,
        senderId
    from {{ source('sparknetworks','messages')}}

)

select * from messages