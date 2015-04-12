import tweepy, os


class CustomStreamListener(tweepy.StreamListener):
  def __init__(self, socketio):
    super(CustomStreamListener, self).__init__()
    self.socketio = socketio

  def on_status(self, status):
    data = {'text': status.text.encode('utf-8')}
    data.update({k:getattr(status.author, k) for k in ['time_zone', 'location']})
    data.update({k:getattr(status, k) for k in ['lang', 'coordinates']})
    self.socketio.emit('status', data)
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
