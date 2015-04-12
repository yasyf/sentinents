FlaskStart.controller 'IndexCtrl', ['$scope', 'Areas', ($scope, Areas) ->

  $scope.track = "everything"
  lastUpdate = "everything"

  areas = Areas.areas()
  socket = io.connect("http://#{document.domain }:#{location.port}")

  AmCharts.ready ->

    red = '#ff7a7a'
    green = '#7aff9b'
    yellow = '#FFFD7A'

    areaindexes = _.object _.map areas, (area, i) ->
      [area.id, i]

    map = new AmCharts.makeChart 'map',
      type: 'map'
      theme: 'black'
      color: 'white'
      fontFamily: "Lato"
      fontSize: 20
      pathToImages: "https://cdnjs.cloudflare.com/ajax/libs/ammaps/3.13.0/images/"
      dataProvider:
        map: 'worldLow'
        areas: areas
      areasSettings:
        autoZoom: false
        rollOverColor: '#7a8eff'
        balloonText: "<b>[[title]]</b>: [[value]]%"
      zoomControl:
        zoomControlEnabled: false
        panControlEnabled: false
      legend:
        divId: "legend"
        align: "center"
        color: "white"
        width: "100%"
        top: 450
        data: [
          {title: "Negative Sentiment", color: red},
          {title: "Neutral Sentiment", color: yellow},
          {title: "Positive Sentiment", color: green}
        ]

    trackNewQuery = (track) ->
      if track != lastUpdate
        console.log "#{lastUpdate} -> #{track}"
        socket.emit 'closeStream',
          track: lastUpdate
        lastUpdate = track
        map.dataProvider.zoomLevel = 1
        areas = Areas.areas()
        map.dataProvider.areas = areas
        map.validateData()
        socket.emit 'openStream',
          track: track

    socket.on 'status', (data) ->
      if areas[areaindexes[data.country]]
        n = areas[areaindexes[data.country]].customData + 1
        areas[areaindexes[data.country]].customData = n
        value = areas[areaindexes[data.country]].value
        newValue = (value * ((n - 1) / n)) + (data.sentiment * 100) * (1 / n)
        newValue = newValue.toFixed(2)
        areas[areaindexes[data.country]].value = newValue
        areas[areaindexes[data.country]].color = switch
          when newValue < 50 then red
          when newValue == 50 then yellow
          when newValue > 50 then green
        console.log data.country, newValue
        map.dataProvider.zoomLevel = map.zoomLevel()
        map.validateData()

    socket.on 'connect', ->
      socket.emit 'ping', 'pong'
      socket.emit 'openStream',
        track: $scope.track

    $scope.$watch 'track', _.debounce(trackNewQuery, 500)

    $(window).unload ->
      socket.emit 'closeStream',
        track: $scope.track
]
