# In the future, we'll use this to test the sync endpoints.

# TEST_SYNC_ENDPOINTS = [
#     "/n/6rhcf8db14sq3i8aixskd8n1z/sync/events?stamp=0",
#     "/n/6rhcf8db14sq3i8aixskd8n1z/sync/events?stamp=0&type=tag,thread",
# ]

# Mark as read
# -X POST -H "Accept: application/json" -d '{"add_tags":[], "remove_tags": ["unread"]}' "https://lol:@gunks.inboxapp.com/n/6rhcf8db14sq3i8aixskd8n1z/threads/2qzpuwm60t74mzw3a4r0x4ysi" -o\
#      "./n/6rhcf8db14sq3i8aixskd8n1z/threads/_2qzpuwm60t74mzw3a4r0x4ysi.put.json"

# # Create draft in reply to thread
# -X POST -H "Accept: application/json" -d '{"namespace":"6rhcf8db14sq3i8aixskd8n1z","date":1402961116.968154,"replying_to_thread":"2qzpuwm60t74mzw3a4r0x4ysi","body":"Thisisatestdraftcreation!\n\nSentfromInbox","state":null,"updated_at":null,"created_at":1402961133.659725,"from":[{"name":"ben@inboxapp.com","email":"ben@inboxapp.com"}],"subject":"MissedZulipfromChristineSpang","files":null,"thread":"2qzpuwm60t74mzw3a4r0x4ysi","to":[{"name":"ChristineSpang","email":"zulip@zulip.com"}]}' "https://lol:@gunks.inboxapp.com/n/6rhcf8db14sq3i8aixskd8n1z/drafts" -o\
#      "./n/6rhcf8db14sq3i8aixskd8n1z/drafts/index.post.json"

# # Delete draft. NOTE requires DRAFT_ID from previous line
# -X DELETE "https://lol:@gunks.inboxapp.com/n/6rhcf8db14sq3i8aixskd8n1z/drafts/DRAFT_ID" -o\
#      "./n/6rhcf8db14sq3i8aixskd8n1z/drafts/DRAFT_ID.delete.json"

# # Generate sync stamp
# -X POST -d '{"start": 1392247858}' "https://lol:@gunks.inboxapp.com/n/6rhcf8db14sq3i8aixskd8n1z/sync/generate_stamp" -o\
#      "./n/6rhcf8db14sq3i8aixskd8n1z/sync/generate_stamp/index.post.json"
