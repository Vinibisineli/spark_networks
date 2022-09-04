with subscriptions as(
    SELECT
        *
    FROM
    {{ ref('rename_subscriptions') }}
)

select * from subscriptions