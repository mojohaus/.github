#!/usr/bin/env ruby
# frozen_string_literal: true

# The MojoHaus maven-verify wrapper exposes a subset of the inputs of
# apache/maven-gh-actions-shared@v5 and its comments promise that every default
# matches upstream. This script compares the two and prints a Markdown report.
# Read-only; the workflow opens an issue in this repo when defaults drift.

require 'json'
require 'net/http'
require 'uri'
require 'yaml'

UPSTREAM = 'https://raw.githubusercontent.com/apache/maven-gh-actions-shared/v5/.github/workflows/maven-verify.yml'
WRAPPER = 'https://raw.githubusercontent.com/mojohaus/.github/master/.github/workflows/maven-verify.yml'

def fetch(url)
  uri = URI(url)
  response = Net::HTTP.get_response(uri)
  raise "HTTP #{response.code} for #{url}" unless response.is_a?(Net::HTTPSuccess)

  response.body
end

def inputs(yaml)
  doc = YAML.safe_load(yaml, permitted_classes: [], aliases: false)
  trigger = doc.fetch('on', doc.fetch(true, {}))
  trigger.fetch('workflow_call', {}).fetch('inputs', {})
rescue KeyError => e
  raise "unexpected workflow shape: #{e.message}"
end

upstream = inputs(fetch(UPSTREAM))
wrapper = inputs(fetch(WRAPPER))

drift = []
wrapper.each do |name, spec|
  next unless upstream.key?(name)

  ours = spec['default']
  theirs = upstream[name]['default']
  drift << [name, theirs, ours] unless ours == theirs
end

report = ['# maven-verify wrapper default drift', '']
if drift.empty?
  report << "All #{wrapper.size} wrapper defaults match upstream `v5`."
else
  report << 'The following defaults no longer match `apache/maven-gh-actions-shared@v5`. Review each; MojoHaus may deliberately keep the old value, in which case update this comment in the wrapper so the choice is recorded.'
  report << ''
  drift.each do |name, theirs, ours|
    report << "- `#{name}`: upstream `#{theirs.inspect}`, wrapper `#{ours.inspect}`"
  end
end

puts report.join("\n")
warn "Checked #{wrapper.size} wrapper inputs, #{drift.size} drifting"
