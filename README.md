# Twitter Discord Webhook

Automated script to track Twitter posts and post them on Discord using webhooks.

Set the following environment variables:

- `TWITTER_BEARER_TOKEN`: Get it from the Twitter Developer Portal  
- `DISCORD_WEBHOOK_URL`: Create a webhook integration in the Discord channel you want and use the link as the value  
- `TWITTER_USER_ID`: The **numerical** user ID of the Twitter account you want to track.  
   - You can fetch this with a GET request (using Postman or curl), or use a third-party tool like MediaMister.

User post
<img width="822" height="505" alt="Screenshot 2025-09-07 000553" src="https://github.com/user-attachments/assets/8a283e72-3eaf-4da0-ac10-f9ca4b7c5a60" />

Webhook post

<img width="348" height="366" alt="Screenshot 2025-09-07 000013" src="https://github.com/user-attachments/assets/cddf8120-d706-4854-8d49-ce6a303942cf" />



