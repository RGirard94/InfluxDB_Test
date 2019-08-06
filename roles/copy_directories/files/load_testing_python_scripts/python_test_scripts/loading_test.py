import os
import datetime
import time
import configparser
from influxdb import InfluxDBClient
import logging


logging.basicConfig(
    filename='/opt/docker-data/tests/personal_logs/injection_logs.log',
    filemode='a',
    format='%(message)s',
    level=logging.INFO
)


def get_number_output_rrinterval(client):
    r = client.query('select count(*) from RrInterval')
    return list(r.get_points(measurement='RrInterval'))[0]


def get_number_output_motionaccelerometer(client):
    r = client.query('select count(*) from MotionAccelerometer')
    return list(r.get_points(measurement='MotionAccelerometer'))[0]


def get_number_output_motiongyroscope(client):
    r = client.query('select count(*) from MotionGyroscope')
    return list(r.get_points(measurement='MotionGyroscope'))[0]


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('/opt/docker-data/tests/load_testing_python_scripts/output_requests/config.conf')

    influxdb_client_constants = config["Influxdb Client"]

    DB_NAME = influxdb_client_constants["database_name"]
    HOST = influxdb_client_constants["host"]
    PORT = int(influxdb_client_constants["port"])
    USER = influxdb_client_constants["user"]
    PASSWORD = influxdb_client_constants["password"]

    CLIENT = InfluxDBClient(host=HOST, port=PORT, username=USER, password=PASSWORD,
                            database=DB_NAME)

    for i in range(10):

        os.system("sudo python3.6 /opt/docker-data/tests/load_testing_python_scripts/random_data_generator/source/random_data_generator.py -nbu 10 -hr 8")
        #os.system("sudo python3.6 /opt/docker-data/tests/load_testing_python_scripts/random_data_generator/source/random_data_generator_2.py -rr 10 -mg 10 -ma 10")

        t1 = datetime.datetime.now()

        logging.info('injection begin at : {}'.format(t1))

        os.system("sudo python3.6 /opt/docker-data/tests/load_testing_python_scripts/manual_data_injection/manual_data_injection.py --directory /opt/docker-data/data/aura_generated_data")

        t2 = datetime.datetime.now()

        logging.info('injection {} duration : {}'.format(i, t2-t1))

        logging.info('monitoring-RrInterval-output : {}'.format(get_number_output_rrinterval(CLIENT)['count_RrInterval']))

        logging.info('monitoring-MotionAccelerometer-output count_x_acm : {}'.format(
            get_number_output_motionaccelerometer(CLIENT)['count_x_acm']))
        logging.info('monitoring-MotionAccelerometer-output count_y_acm : {}'.format(
            get_number_output_motionaccelerometer(CLIENT)['count_y_acm']))
        logging.info('monitoring-MotionAccelerometer-output count_z_acm : {}'.format(
            get_number_output_motionaccelerometer(CLIENT)['count_z_acm']))


        logging.info(
            'monitoring-MotionGyroscope-output count_x_gyro : {}'.format(get_number_output_motiongyroscope(CLIENT)['count_x_gyro']))
        logging.info(
            'monitoring-MotionGyroscope-output count_y_gyro : {}'.format(get_number_output_motiongyroscope(CLIENT)['count_y_gyro']))
        logging.info(
            'monitoring-MotionGyroscope-output count_z_gyro : {}'.format(get_number_output_motiongyroscope(CLIENT)['count_z_gyro']))

        logging.info('--------------------------------------------')

        logging.info('{}'.format(i))

        if i != 9:
            time.sleep(1800)
