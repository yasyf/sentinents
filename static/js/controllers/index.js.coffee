FlaskStart.controller 'IndexCtrl', ['$scope', 'Areas', ($scope, Areas) ->
  AmCharts.ready ->

    red = '#ff7a7a'
    green = '#7aff9b'
    yellow = '#FFFD7A'

    areas = Areas.areas()
    areaindexes = _.object _.map areas, (area, i) ->
      [area.id, i]

    map = new AmCharts.makeChart 'map',
      type: 'map'
      theme: 'black'
      pathToImages: "https://cdnjs.cloudflare.com/ajax/libs/ammaps/3.13.0/images/"
      dataProvider:
        map: 'worldLow'
        areas: areas
      areasSettings:
        autoZoom: true
      zoomControl:
        zoomControlEnabled: false
        panControlEnabled: false
      legend:
        divId: "legend"
        width: "100%"
        top: 450
        data: [
          {title: "Negative Sentiment", color: red},
          {title: "Neutral Sentiment", color: yellow},
          {title: "Positive Sentiment", color: green}
        ]


    socket = io.connect("http://#{document.domain }:#{location.port}")
    socket.on 'status', (data) ->
      if areas[areaindexes[data.country]]
        value = areas[areaindexes[data.country]].value + if data.sentiment >= 0.5 then 1 else -1
        areas[areaindexes[data.country]].value = value
        areas[areaindexes[data.country]].color = switch
          when value < 0 then red
          when value == 0 then yellow
          when value > 0 then green
        console.log data.country, areas[areaindexes[data.country]].color, value
        map.dataProvider.zoomLevel = map.zoomLevel()
        map.validateData()

    socket.on 'connect', ->
      socket.emit 'ping', 'pong'
]
