FlaskStart.controller 'IndexCtrl', ['$scope', ($scope) ->
  socket = io.connect("http://#{document.domain }:#{location.port}")
  socket.on 'status', (data) ->
    console.log data
  socket.on 'connect', ->
    socket.emit 'ping', 'pong'
]
