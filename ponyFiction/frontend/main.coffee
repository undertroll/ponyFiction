{render} = require 'react'
slider = require './slider'

sliderSettings =
  dots: true
  infinite: true
  speed: 500
  slidesToShow: 1
  slidesToScroll: 1
  className: "carousel"

render slider(sliderSettings), document.getElementById('slides')