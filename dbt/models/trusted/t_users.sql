with users as (
  
  SELECT
      user_id,
      createdat,
      updatedat,
      firstname_anonymized,
      lastname_anonymized,
      address_anonymized,
      city,
      country,
      zipcode_anonymized,
      email_domain,
      birthdate,
      gender,
      issmoking,
      profession,
      income
FROM
  {{ ref('anonymize_users') }})

select * from users
