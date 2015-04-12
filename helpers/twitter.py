import tweepy, os, random
from requests_futures.sessions import FuturesSession

TEST_MODE = True

class CustomStreamListener(tweepy.StreamListener):
  def __init__(self, socketio):
    super(CustomStreamListener, self).__init__()
    self.socketio = socketio
    self.session = FuturesSession()

  def on_status(self, status):
    if status.coordinates or status.author.location:
      data = {'text': status.text.encode('utf-8')}
      data.update({k:getattr(status.author, k) for k in ['time_zone', 'location']})
      data.update({k:getattr(status, k) for k in ['lang', 'coordinates']})

      def add_sentiment(session, response):
        data['sentiment'] = response.json()['results']
        self.socketio.emit('status', data)

      def add_country_code(session, response):
        try:
          json = response.json()
          if json['totalResultsCount'] > 0:
            data['country'] = json['geonames'][0]['countryCode']
          else:
            return
        except:
          data['country'] = response.text.strip()

        if TEST_MODE:
          data['sentiment'] = random.random()
          self.socketio.emit('status', data)
        else:
          url = "http://apiv2.indico.io/sentiment"
          args = {'key': os.getenv('INDICOIO_API_KEY')}
          self.session.post(url, data={'data': data['text']}, params=args, background_callback=add_sentiment)

      if status.coordinates:
        url = "http://ws.geonames.org/countryCode"
        args = {'lat': status.coordinates['coordinates'][1], 'lng': status.coordinates['coordinates'][0], 'username': 'yasyf'}
        self.session.get(url, params=args, background_callback=add_country_code)
      else:
        url = "http://api.geonames.org/search"
        args = {'q': status.author.location, 'username': 'yasyf', 'maxRows': 1, 'type': 'json'}
        self.session.get(url, params=args, background_callback=add_country_code)
    return True

  def on_error(self, status_code):
    print 'Encountered error with status code:', status_code
    return True

  def on_timeout(self):
    print 'Timeout...'
    return True

def get_stream_listener(socketio):
  listener = CustomStreamListener(socketio)
  auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET'))
  auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
  stream = tweepy.streaming.Stream(auth, listener)
  return stream, listener
