from requests import Session
import praw
import pandas as pd
import datetime

session = Session()
session.verify = '/path/to/certfile.pem'
reddit = praw.Reddit(client_id='o3TzQZFbeeP04w',
                     client_secret='Nq6emenW7pdyv1iNDB5gtjWzamY',
                     password='Beardie1',
                     user_agent='Sam_Reddit API',
                     username='confused_analyst')


def get_submission_date(submission):
    time = submission.created
    return datetime.date.fromtimestamp(time)


results = []

df = pd.DataFrame(pd.read_excel(r'C:\Users\samantha.riley\PycharmProjects\Honeywell\Terms.xlsx'))
keywords = df.Terms.tolist()

for i in keywords:
    for submission in reddit.subreddit('all').search(i):
        date = get_submission_date(submission)
        title = submission.title
        text = submission.selftext
        sub = submission.subreddit.display_name
        sub_author = submission.author
        url = submission.url
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            comment_body = comment.body
            comment_author = comment.author
            data = {"keyword": i,
                    "submission_url": url,
                    "date": date,
                    "title": title,
                    "submission_text": text,
                    "submission_author": sub_author,
                    "comment": comment_body,
                    "comment_author": comment_author,
                    "subreddit": sub}
            results.append(data)
    print(i)

df = pd.DataFrame(results)
df.to_csv('allsubs-honeywell.csv', index=False)
print(df.head())