with users as (
  SELECT
      user_id,
      createdat,
      updatedat,
      encode(sha256(firstname::bytea), 'hex') as firstname_anonymized,
      encode(sha256(lastname::bytea), 'hex') as lastname_anonymized,
      encode(sha256(address::bytea), 'hex') as address_anonymized,
      city,
      country,
      encode(sha256(zipcode::bytea), 'hex') as zipcode_anonymized,
      split_part(email, '@', 2) as email_domain,
      birthDate,
      gender,
      issmoking,
      profession,
      income
  FROM
    {{ ref('rename_users')}})

select * from users