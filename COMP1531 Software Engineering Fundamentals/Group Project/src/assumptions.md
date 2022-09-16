Assumptions for auth
    - Assuming no emojis or numbers entered for first and last names
    - Assuming no emojis used for password
    - Assuming there will be no repetition in the password reset request code considering it is 40 characters long

Assumptions for handle:
    - assuming not more than 1001 people will have the same forst and last names for handle as random range is from 0-1000 only

For Channel:
    - If a channel exists, it must have at least one owner

for channel_invite:
    -if user1 want to invite user2 into channel, assume they are both log in now

for channel_addowner:
    -assume u_id must be a member in that channel

for channel_leave:
    -if an owner want to leave that channel, a random member will be the new owner

fot message_send:
    -message can be empty

for message_edit:
    -if the message is greater than 1000 characters, then raise input error
    -if the edited message is same as previous message, the timestamp will change 

for standup:
    - A standup will be started for greater then 0 seconds
    - A standup message will not be more than 1000 characters