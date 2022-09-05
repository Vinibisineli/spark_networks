with users as (
  SELECT
      user_id,
      createdat,
      updatedat,
      sha256(firstname) as firstname_anonymized,
      sha256(lastname) as lastname_anonymized,
      sha256(address) as address_anonymized,
      city,
      country,
      sha256(zipcode) as zipcode_anonymized,
      split_part(email, '@', 2) as email_domain,
      birthDate,
      gender,
      issmoking,
      profession,
      income
  FROM
    {{ ref('rename_users')}})

select * from users