with messages as(
    SELECT
        *
    FROM
    {{ ref('rename_messages') }}
)

select * from messages