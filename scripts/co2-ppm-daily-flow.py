import datetime
import os
import urllib.request

from dataflows import PackageWrapper, ResourceWrapper, Flow, dump_to_path


def get_all_data():
    all_years = {}
    # first source containing info from 01.01.1958 to 2004
    header = True
    resource = urllib.request.urlopen('http://scrippsco2.ucsd.edu/assets/data/atmospheric/stations/in_situ_co2/daily/'
                                      'daily_in_situ_co2_mlo.csv')
    for row in resource.readlines():
        # Stop at 1974
        if '1974' in row.decode('utf-8'):
            break
        usable_row = row.decode('utf-8').replace('\n', '')
        parts = usable_row.split(',')
        if not usable_row.startswith('%'):
            header = False
        if not header:
            date = parts[0].strip()+'-'+parts[1].strip()+'-'+parts[2].strip()
            value = parts[3].strip()

            if 'NaN' not in value:
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
                all_years[date] = value


def get_only_2018_and_on():
    all_years = {}

    header = True
    for row in open('data/co2-ppm-daily.csv'):
        usable_row = row.replace('\n', '')
        parts = usable_row.split(',')
        if header:
            header = False
        else:
            date = parts[0]
            value = parts[1]
            if value is not '':
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
                all_years[date] = value

    # third source containing info from 1974 until today
    header = True
    resource = urllib.request.urlopen(
        'https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_weekly_mlo.csv')
    # Skip 35 lines
    for row in resource.readlines()[36:]:
        parts = row.decode('utf-8').strip().split(',')
        year, month, day, _, value = parts[:5]
        date_obj = datetime.datetime(int(year), int(month), int(day))
        all_years[date_obj] = value
    all_years = sorted(all_years.items())
    for date, value in all_years:
        yield dict(
            date=date.strftime("%Y-%m-%d"),
            value=value
        )


def change_path(package: PackageWrapper):

    package.pkg.descriptor['title'] = 'CO2 PPM - Trends in Atmospheric Carbon Dioxide'
    package.pkg.descriptor['name'] = 'co2-ppm-daily'

    package.pkg.descriptor['resources'][0]['path'] = 'data/co2-ppm-daily.csv'
    package.pkg.descriptor['resources'][0]['name'] = 'co2-ppm-daily'

    package.pkg.descriptor['views'] = []
    view = {
        "specType": "vega",
        "resources": [
          {
            "name": "co2-ppm-daily",
            "transform": []
          }
        ],
        "spec": {
          "$schema": "https://vega.github.io/schema/vega/v3.json",
          "width": 900,
          "height": 400,
          "padding": 30,
          "data": [
            {
              "name": "co2-ppm-daily",
              "format": {"parse": {"date": "date"}},
              "transform": [
                {"type": "extent", "field": "value", "signal": "extent"}
              ]
            }
          ],

          "scales": [
            {
              "name": "xscale",
              "type": "utc",
              "range": "width",
              "domain": {"data": "co2-ppm-daily", "field": "date"}
            },
            {
              "name": "yscale",
              "type": "linear",
              "range": "height",
              "nice": True,
              "zero": False,
              "domain": {"data": "co2-ppm-daily", "field": "value"}
            }
          ],

          "axes": [
            {
              "orient": "bottom",
              "scale": "xscale",
              "labelFont": "Lato",
              "format": "%b %Y",
              "domain": False,
              "ticks": False
            }
          ],

          "marks": [
            {
              "type": "area",
              "from": {"data": "co2-ppm-daily"},
              "encode": {
                "enter": {
                  "x": {"scale": "xscale", "field": "date"},
                  "y": {"scale": "yscale", "field": "value"},
                  "y2": {"scale": "yscale", "signal": "floor(extent[0])"},
                  "fill": {"value": "#FBE7E8"},
                  "stroke": {"value": "#E3B3BD"}
                }
              }
            },
            {
              "type": "text",
              "encode": {
                "enter": {
                  "text": {"signal": "extent[1] + ' PPM'"}
                },
                "update": {
                  "x": {"value": -94},
                  "font": {"value": "Lato"},
                  "fontSize": {"value": 16},
                  "opacity": {"value": 0.4}
                }
              }
            },
            {
              "type": "text",
              "encode": {
                "enter": {
                  "text": {"signal": "extent[0] + ' PPM'"}
                },
                "update": {
                  "x": {"value": -94},
                  "y": {"value": 385},
                  "font": {"value": "Lato"},
                  "fontSize": {"value": 16},
                  "opacity": {"value": 0.4}
                }
              }
            },
            {
              "type": "text",
              "encode": {
                "enter": {
                  "text": {"signal": "extent[1] + ' PPM'"}
                },
                "update": {
                  "x": {"value": 910},
                  "font": {"value": "Lato"},
                  "fontSize": {"value": 16},
                  "opacity": {"value": 0.4}
                }
              }
            },
            {
              "type": "text",
              "encode": {
                "enter": {
                  "text": {"signal": "extent[0] + ' PPM'"}
                },
                "update": {
                  "x": {"value": 910},
                  "y": {"value": 385},
                  "font": {"value": "Lato"},
                  "fontSize": {"value": 16},
                  "opacity": {"value": 0.4}
                }
              }
            }
          ]
        }
    }
    package.pkg.descriptor['views'].append(view)

    yield package.pkg
    res_iter = iter(package)
    first: ResourceWrapper = next(res_iter)
    yield first.it
    yield from package


if os.path.exists('data/co2-ppm-daily.csv'):
    co2_ppm_daily = Flow(get_only_2018_and_on(), change_path, dump_to_path())
else:
    co2_ppm_daily = Flow(get_all_data(), change_path, dump_to_path())


if __name__ == '__main__':
    co2_ppm_daily.process()
