# teleflume

Python script to collect metrics from [Apache flume]([https://flume.apache.org/) and print InfluxDB compatible output.
It connects to the [flumes metrics endpoint](http://flume.apache.org/FlumeUserGuide.html#json-reporting) to get the stats in json format.
  
This tool is meant to be used with Telegraf's `inputs.exec` plugin.

The configuration of fields that are part of filed set for telegraf must be configured in a yaml file and must be supplied as a argument to the script.

`python teleflume.py --host 127.0.0.1 --port 34546 --config teleflume.yaml --measurement <measurement_name>`
