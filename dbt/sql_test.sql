-- How many total messages are being sent every day?

select 
date(createdat),
count(*) as msg_sent_count
from postgres."trusted".t_message tm 
group by date(createdat)
order by date(createdat) desc


-- Are there any users that did not receive any message?

with users as (
	select user_id from postgres."trusted".t_users tu 
),
user_recive as (
	select tm.reciverid from postgres."trusted".t_message tm 
	group by tm.reciverid
)
select user_id from users
left join user_recive on (user_id=reciverid)
where reciverid is null


-- How many active subscriptions do we have today?

select count(*) from postgres."trusted".t_subscriptions ts 
where status='Active'
and enddate >= current_timestamp 

-- Are there users sending messages without an active subscription? (some extra
-- context for you: in our apps only premium users can send messages).

with fraud_detection as (
	select tm.senderid, case when tm.createdat between ts2.createdat and ts2.enddate then 'OK' else 'ALERT' end as fraud
		from postgres."trusted".t_message tm 
		inner join postgres."trusted".t_subscriptions ts2 on (tm.senderid=ts2.user_id)
)
select count(*) from fraud_detection
where fraud = 'ALERT'


-- How much is the average subscription amount (sum amount subscriptions /
-- count subscriptions) breakdown by year/month (format YYYY-MM)?

with first_sub as (
	select DATE_TRUNC('month',ts.createdat) as first_sub_date from postgres."trusted".t_subscriptions ts order by ts.createdat limit 1
), periods as (
	select generate_series(first_sub_date::timestamp, current_timestamp , '1 month') as start_date  from first_sub
), total_period as (
	select start_date,((start_date+interval '1 month') + interval '-1 second') as end_date from periods
) 
select to_char(tp.start_date,'YYYY-mm'),sum(amount)/count(*) as avg_sub_amount
from postgres."trusted".t_subscriptions ts2 
full join total_period tp on 1=1
where DATE_TRUNC('month',ts2.createdat) <= tp.start_date and (DATE_TRUNC('month',ts2.enddate) + interval '1 month') + interval '-1 second'>=tp.end_date
group by tp.start_date
order by tp.start_date 