{map} = require 'lodash'
{post} = require 'npm-zepto'
{Request, parse} = require 'json-rpc.js'
{createFactory, createClass, DOM} = require 'react'
Slider = require 'react-slick'

ENDPOINT = '/api/'

StorySlider = createFactory createClass
  getInitialState: -> stories: []

  componentDidMount: ->
    post ENDPOINT, Request('stories.get_random').toString(), (response) =>
      response = parse response
      if response.error?
        console.debug response.toString()
      else
        @setState stories: response.result

  render: ->
    Slider @props.settings,
      map @state.stories, (story) ->
        DOM.div className: "story-item",
          DOM.h3 null, DOM.a href: story.url, story.name
          DOM.p className: "meta",
            DOM.span className: "category-list",
              map story.categories, (category) ->
                DOM.a className: "gen", style: {backgroundColor: category.color}, href: category.url,
                  category.name
          DOM.p null, story.summary
          DOM.p className: "meta",
            DOM.span className: "category-list",
              map story.characters, (character) ->
                DOM.a href: character.url,
                  DOM.img alt: character.name, title: character.name, src: character.thumb


module.exports = StorySlider
