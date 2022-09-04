with users as (
  SELECT
      user_id,
      createdat,
      updatedat,
      md5(firstname) as firstname_anonymized,
      md5(lastname) as lastname_anonymized,
      md5(address) as address_anonymized,
      city,
      country,
      md5(zipcode) as zipcode_anonymized,
      split_part(email, '@', 2) as email_domain,
      birthDate,
      gender,
      issmoking,
      profession,
      income
  FROM
    {{ ref('rename_users')}})

select * from users