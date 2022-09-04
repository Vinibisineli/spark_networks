with users as (

    select
        user_id,
        createdat,
        updatedat,
        firstname,
        lastname,
        address,
        city,
        country,
        zipcode,
        email,
        birthdate,
        gender,
        issmoking,
        profession,
        income
    from {{ source('sparknetworks','users')}}

)

select * from users