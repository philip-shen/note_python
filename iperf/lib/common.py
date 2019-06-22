#!/usr/bin/env python3

import os
import time
import iperf3

from logger import logger

def server_siteone(parms):
    server = iperf3.Server()
    server.port = parms['port']
    server.protocol = parms['protocol']

    #print('Running server: {0}:{1}'.format(server.bind_address, server.port))
    logger.info('Running server: {0}:{1}:{2}'.format(server.bind_address, server.port, server.protocol))

    while True:
        result = server.run()

        if result.error:
            #print(result.error)
            logger.info(result.error)
        else:
            print('')
            #print('Test results from {0}:{1}'.format(result.remote_host,
            #                                     result.remote_port))
            logger.info('Test results from {0}:{1} to {2}'.format(result.remote_host,
                                                result.remote_port,result.local_port))
            #print('  started at         {0}'.format(result.time))
            #print('  bytes received     {0}'.format(result.received_bytes))
            logger.info('  started at         {0}'.format(result.time))
            logger.info('  bytes received     {0}'.format(result.received_bytes))

            #print('Average transmitted received in all sorts of networky formats:')
            logger.info('Average transmitted received in all sorts of networky formats:')

            #print('  bits per second      (bps)   {0}'.format(result.received_bps))
            #print('  Kilobits per second  (kbps)  {0}'.format(result.received_kbps))
            #print('  Megabits per second  (Mbps)  {0}'.format(result.received_Mbps))
            #print('  KiloBytes per second (kB/s)  {0}'.format(result.received_kB_s))
            #print('  MegaBytes per second (MB/s)  {0}'.format(result.received_MB_s))
            logger.info('  bits per second      (bps)   {0}'.format(result.received_bps))
            logger.info('  Kilobits per second  (kbps)  {0}'.format(result.received_kbps))
            logger.info('  Megabits per second  (Mbps)  {0}'.format(result.received_Mbps))
            logger.info('  KiloBytes per second (kB/s)  {0}'.format(result.received_kB_s))
            logger.info('  MegaBytes per second (MB/s)  {0}'.format(result.received_MB_s))

def client_siteone(parms):
    client = iperf3.Client()
    client.duration = 1
    client.server_hostname = parms['remote_server_ip']
    client.port = parms['port']
    client.protocol = parms['protocol']

    logger.info('Connecting to {0}:{1}:{2}'.format(client.server_hostname, client.port, client.protocol))
    result = client.run()

    if result.error:
        logger.info(result.error)
    else:
        print('')
        logger.info('Test completed:')
        logger.info('  started at         {0}'.format(result.time))
        logger.info('  bytes transmitted  {0}'.format(result.sent_bytes))
        logger.info('  retransmits        {0}'.format(result.retransmits))
        logger.info('  avg cpu load       {0}%\n'.format(result.local_cpu_total))

        logger.info('Average transmitted data in all sorts of networky formats:')
        logger.info('  bits per second      (bps)   {0}'.format(result.sent_bps))
        logger.info('  Kilobits per second  (kbps)  {0}'.format(result.sent_kbps))
        logger.info('  Megabits per second  (Mbps)  {0}'.format(result.sent_Mbps))
        logger.info('  KiloBytes per second (kB/s)  {0}'.format(result.sent_kB_s))
        logger.info('  MegaBytes per second (MB/s)  {0}'.format(result.sent_MB_s))

def client_siteone_udp(parms):
    client = iperf3.Client()
    client.duration = 1
    client.server_hostname = parms['remote_server_ip']
    client.port = parms['port']
    client.protocol = parms['protocol']

    logger.info('Connecting to {0}:{1}:{2}'.format(client.server_hostname, client.port, client.protocol))
    result = client.run()

    if result.error:
        logger.info(result.error)
    else:
        print('')
        logger.info('Test completed:')
        logger.info('  started at         {0}'.format(result.time))
        logger.info('  bytes transmitted  {0}'.format(result.bytes))
        logger.info('  jitter (ms)        {0}'.format(result.jitter_ms))
        logger.info('  avg cpu load       {0}%\n'.format(result.local_cpu_total))

        logger.info('Average transmitted data in all sorts of networky formats:')
        logger.info('  bits per second      (bps)   {0}'.format(result.bps))
        logger.info('  Kilobits per second  (kbps)  {0}'.format(result.kbps))
        logger.info('  Megabits per second  (Mbps)  {0}'.format(result.Mbps))
        logger.info('  KiloBytes per second (kB/s)  {0}'.format(result.kB_s))
        logger.info('  MegaBytes per second (MB/s)  {0}'.format(result.MB_s))        