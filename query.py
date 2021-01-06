from searchtweets import ResultStream, gen_rule_payload, load_credentials
from searchtweets import collect_results

import pandas as pd

search_args = load_credentials(filename='./twitter_keys.yaml',
                 yaml_key='twitter_keys',
                 env_overwrite=False)

def get_tweets(keyword, limit='100', begin_date=datetime.now().strftime('%Y-%m-%d'), end_date=datetime.now().strftime('%Y-%m-%d'), lang='id'):
    query = keyword + ' lang:' + lang

    rule = gen_rule_payload(query, from_date=begin_date, to_date=end_date, results_per_call=500)

    tweets = collect_results(rule, max_results=500, result_stream_args=search_args)

    return [tweet.all_text for tweet in tweets]

keyword = 'Indihome'
limit = 500
begin_date = '2020-01-01'
end_date = '2020-12-31'
language = 'id'

tweets = get_tweets(keyword, limit, begin_date, end_date, language)

df = pd.DataFrame(tweets)

df.to_csv('./tweets.csv')