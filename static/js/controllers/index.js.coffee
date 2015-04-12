FlaskStart.controller 'IndexCtrl', ['$scope', 'Areas', ($scope, Areas) ->

  $scope.track = "everything"
  lastUpdate = "everything"

  areas = Areas.areas()
  images = []
  socket = io.connect("http://#{document.domain }:#{location.port}")

  AmCharts.ready ->

    red = '#ff7a7a'
    green = '#7aff9b'
    yellow = '#FFFD7A'
    grey = '#c4c4c4'

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
        images: images
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
          {title: "Unknown", color: grey},
          {title: "Negative", color: red},
          {title: "Neutral", color: yellow},
          {title: "Positive", color: green}
        ]

    trackNewQuery = (track) ->
      if track != lastUpdate
        console.log "#{lastUpdate} -> #{track}"
        socket.emit 'closeStream',
          track: lastUpdate
        lastUpdate = track
        map.dataProvider.zoomLevel = 1
        areas = Areas.areas()
        images = []
        map.dataProvider.areas = areas
        map.dataProvider.images = images
        map.validateData()
        socket.emit 'openStream',
          track: track

    getColor = (value) ->
      color = switch
        when value < 50 then red
        when value == 50 then yellow
        when value > 50 then green
      factor = Math.abs(value - 50) / 2
      tinycolor(color).darken(factor).toString()

    socket.on 'status', (data) ->
      index = areaindexes[data.country]
      if areas[index]
        n = areas[index].customData + 1
        areas[index].customData = n
        value = areas[index].value
        sentiment = data.sentiment * 100
        newValue = (value * ((n - 1) / n)) + sentiment * (1 / n)
        newValue = newValue.toFixed(2)
        areas[index].value = newValue
        areas[index].color = getColor(newValue)

        if images.length > 50
          images = _.takeRight(images, 10)
          map.dataProvider.images = images

        images.push
          type: "circle"
          width: 6
          height: 6
          color: getColor(sentiment)
          longitude: data.coordinates.coordinates[0]
          latitude: data.coordinates.coordinates[1]
          name: data.text
          value: sentiment

        map.dataProvider.zoomLevel = map.zoomLevel()
        map.validateData()

        console.log data.country, newValue

    socket.on 'connect', ->
      socket.emit 'ping', 'pong'
      socket.emit 'openStream',
        track: $scope.track

    $scope.$watch 'track', _.debounce(trackNewQuery, 500)

    $(window).unload ->
      socket.emit 'closeStream',
        track: $scope.track
]
