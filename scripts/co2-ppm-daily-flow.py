import urllib.request
import csv


'''Data looks like ...
% Created 04-Mar-2025 10:04:59
%
% Yr    - Year
% Mn    - Month
% Dy    - Day
% CO2   - CO2 baseline value
% NB    - Number of hourly averages in the baseline
% scale - Calibration scale code
% sta   - Sampling station. Occasional samples have been recorded at the Maunakea Observatory (mko)
%
% Yr, Mn, Dy,    CO2, NB, scale, sta
1958, 01, 01,    NaN,  0, 12.0, mlo
1958, 01, 02,    NaN,  0, 12.0, mlo
1958, 01, 03,    NaN,  0, 12.0, mlo
'''
def get_all_data():
    all_years = {}
    header = True
    resource = urllib.request.urlopen(
      'https://scrippsco2.ucsd.edu/assets/data/atmospheric/stations/in_situ_co2/daily/daily_in_situ_co2_mlo.csv'
      )
    csvfile = open('data/co2-ppm-daily.csv', 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(['date', 'value'])
    for row in resource.readlines():
        usable_row = row.decode('utf-8').replace('\n', '')
        parts = usable_row.split(',')
        if not usable_row.startswith('%'):
            header = False
        if not header:
            date = parts[0].strip()+'-'+parts[1].strip()+'-'+parts[2].strip()
            value = parts[3].strip()

            if 'NaN' not in value:
                writer.writerow([date, value])
    csvfile.close()

if __name__ == '__main__':
    get_all_data()
