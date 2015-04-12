FlaskStart.controller 'IndexCtrl', ['$scope', 'Areas', ($scope, Areas) ->
  AmCharts.ready ->

    areas = Areas.areas()
    areaindexes = _.object _.map areas, (area, i) ->
      [area.id, i]

    map = new AmCharts.makeChart 'mapdiv',
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

    socket = io.connect("http://#{document.domain }:#{location.port}")
    socket.on 'status', (data) ->
      if areas[areaindexes[data.country]]
        value = areas[areaindexes[data.country]].value + if data.sentiment >= 0.5 then 1 else -1
        areas[areaindexes[data.country]].value = value
        areas[areaindexes[data.country]].color = switch
          when value < 0 then "red"
          when value == 0 then "yellow"
          when value > 0 then "green"
        console.log data.country, areas[areaindexes[data.country]].color, value
        map.validateData()

    socket.on 'connect', ->
      socket.emit 'ping', 'pong'
]
