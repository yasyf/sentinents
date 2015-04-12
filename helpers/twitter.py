import tweepy, os, random
from requests_futures.sessions import FuturesSession

TEST_MODE = os.getenv('TEST_MODE') == "true"
streams = {}

class CustomStreamListener(tweepy.StreamListener):
  def __init__(self, socketio, track):
    super(CustomStreamListener, self).__init__()
    self.socketio = socketio
    self.room = track
    self.session = FuturesSession()

  def get_geonames_username(self):
    return "yasyf{}".format(random.randint(1,5))

  def on_status(self, status):
    if status.coordinates or status.author.location:
      data = {'text': status.text.encode('utf-8')}
      data.update({k:getattr(status.author, k) for k in ['time_zone', 'location']})
      data.update({k:getattr(status, k) for k in ['lang', 'coordinates']})

      def add_sentiment(session, response):
        data['sentiment'] = response.json()['results']
        self.socketio.emit('status', data, self.room)

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
          self.socketio.emit('status', data, self.room)
        else:
          url = "http://apiv2.indico.io/sentiment"
          args = {'key': os.getenv('INDICOIO_API_KEY')}
          self.session.post(url, data={'data': data['text']}, params=args, background_callback=add_sentiment)

      if status.coordinates:
        url = "http://ws.geonames.org/countryCode"
        args = {'lat': status.coordinates['coordinates'][1], 'lng': status.coordinates['coordinates'][0],
               'username': self.get_geonames_username()}
        self.session.get(url, params=args, background_callback=add_country_code)
      else:
        url = "http://api.geonames.org/search"
        args = {'q': status.author.location, 'username': self.get_geonames_username(),
                'maxRows': 1, 'type': 'json'}
        self.session.get(url, params=args, background_callback=add_country_code)
    return True

  def on_error(self, status_code):
    print 'Encountered error with status code:', status_code
    return True

  def on_timeout(self):
    print 'Timeout...'
    return True

def get_random_twitter_auth():
  i = random.randint(0,2)
  auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY').split(';')[i],
                              os.getenv('TWITTER_API_SECRET').split(';')[i])
  auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN').split(';')[i],
                        os.getenv('TWITTER_ACCESS_TOKEN_SECRET').split(';')[i])
  return auth

def open_stream(socketio, track):
  if track:
    track = track.lower()
  else:
    track = 'everything'

  if track not in streams:
    listener = CustomStreamListener(socketio, track)
    auth = get_random_twitter_auth()
    stream = tweepy.streaming.Stream(auth, listener)
    if track == "everything":
      stream.sample(async=True)
    else:
      stream.filter(track=[track], async=True)

    streams[track] = [stream, 0]
  streams[track][1] += 1
  return streams[track][0]

def close_stream(track):
  if track:
    track = track.lower()
  else:
    track = 'everything'
  if track in streams:
    streams[track][1] -= 1
    if streams[track][1] < 1:
      stream = streams.pop(track)
      stream[0].disconnect()
