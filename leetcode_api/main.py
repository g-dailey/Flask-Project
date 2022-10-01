import leetcode

# Get the next two values from your browser cookies
leetcode_session = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNjY3MzA4OSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjExMDI3NmU4M2U4YTY1M2ZlNTQwNTJmYTUzNTkxN2Q1OGIwOTZiMGYiLCJpZCI6NjY3MzA4OSwiZW1haWwiOiJndWxhZnJvei5yZXphaUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6Ikd1bGFmcm96NzciLCJ1c2VyX3NsdWciOiJHdWxhZnJvejc3IiwiYXZhdGFyIjoiaHR0cHM6Ly9zMy11cy13ZXN0LTEuYW1hem9uYXdzLmNvbS9zMy1sYy11cGxvYWQvYXNzZXRzL2RlZmF1bHRfYXZhdGFyLmpwZyIsInJlZnJlc2hlZF9hdCI6MTY2NDA5ODk4OSwiaXAiOiIxMzYuNTMuNzYuOTAiLCJpZGVudGl0eSI6ImEwNWRmMDA3ZWZjZWZlMjg5NDE0Y2Q2ZDBlMTBlNzE3Iiwic2Vzc2lvbl9pZCI6MjgzMDMxNjUsIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMH0.Vsh935L-9ZiWkVq08p1LRL6uVLInKBIDK8M12droBIU"
csrf_token = "mE30sGcxyPiMVu9s2yILM1RHYLg2rfiCCTCOuNlsniozGYwcHO6x41rwr9rIuPI9"

# Experimental: Or CSRF token can be obtained automatically
import leetcode.auth
csrf_token = leetcode.auth.get_csrf_cookie(leetcode_session)

configuration = leetcode.Configuration()

configuration.api_key["x-csrftoken"] = csrf_token
configuration.api_key["csrftoken"] = csrf_token
configuration.api_key["LEETCODE_SESSION"] = leetcode_session
configuration.api_key["Referer"] = "https://leetcode.com"
configuration.debug = False

api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

graphql_request = leetcode.GraphqlQuery(
    query="""
      {
        user {
          username
          isCurrentUserPremium
        }
      }
    """,
    variables=leetcode.GraphqlQueryVariables(),
)

print(api_instance.graphql_post(body=graphql_request))


api_response = api_instance.api_problems_topic_get(topic="algorithms")

slug_to_solved_status = {
    pair.stat.question__title_slug: True if pair.status == "ac" else False
    for pair in api_response.stat_status_pairs
}



import time

from collections import Counter


topic_to_accepted = Counter()
topic_to_total = Counter()


# Take only the first 10 for test purposes
for slug in list(slug_to_solved_status.keys())[:2]:
    time.sleep(1)  # Leetcode has a rate limiter

    graphql_request = leetcode.GraphqlQuery(
        query="""
            query getQuestionDetail($titleSlug: String!) {
              question(titleSlug: $titleSlug) {
                topicTags {
                  name
                  slug
                }
              }
            }
        """,
        variables=leetcode.GraphqlQueryVariables(title_slug=slug),
        operation_name="getQuestionDetail",
    )

    api_response = api_instance.graphql_post(body=graphql_request)

    for topic in (tag.slug for tag in api_response.data.question.topic_tags):
        topic_to_accepted[topic] += int(slug_to_solved_status[slug])
        topic_to_total[topic] += 1

print(
    list(
        sorted(
            ((topic, accepted / topic_to_total[topic]) for topic, accepted in topic_to_accepted.items()),
            key=lambda x: x[1]
        )
    )
)