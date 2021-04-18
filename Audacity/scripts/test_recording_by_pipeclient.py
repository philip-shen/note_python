# Adapte from recording_test.py
import os,sys,time
import json

sys.path.append('.')
from pipeclient import *
from logger import logger

client = PipeClient()   
def do_command(command, timeout):
    start = time.time()
    #client = PipeClient()

    #while True:
    reply = ''
    start = time.time()

    client.write(command, timer=True)

    while reply == '':
        time.sleep(0.1)  # allow time for reply
        if time.time() - start > timeout:
            reply = 'PipeClient: Reply timed-out.'
        else:
            reply = client.read()

    msg = '{}'
    logger.info(msg.format(reply))
    
    return reply

def play_record(filename, timeout):
    """Import track and record to new track.
    Note that a stop command is not required as playback will stop at end of selection.
    """
    
    do_command("Import2: Filename={}".format(os.path.join(PATH, filename + '.wav').replace('\\','/')), timeout); #OK    
    do_command("Select: Track=0", timeout)
    do_command("SelTrackStartToEnd", timeout)
    # Our imported file has one clip. Find the length of it.
    clipsinfo = do_command("GetInfo: Type=Clips", timeout)
    clipsinfo = clipsinfo[:clipsinfo.rfind('BatchCommand finished: OK')]
    clips = json.loads(clipsinfo)
    duration = clips[0]['end'] - clips[0]['start']
    # Now we can start recording.
    msg = 'Sleeping until recording is complete...'
    logger.info(msg)
    do_command("Record2ndChoice", duration)
    
    #time.sleep(duration + 0.1)
    
def export(filename, timeout):
    """Export the new track, and deleted both tracks."""
    do_command("Select: Track=1 mode=Set", timeout)
    do_command("SelTrackStartToEnd", timeout)
    do_command("Export2: Filename={} NumChannels=1.0".format(os.path.join(PATH, filename + '.wav').replace('\\','/') ), \
                timeout)
    do_command("SelectAll", timeout)
    do_command("RemoveTracks", timeout)

def do_one_file(name, timeout):
    """Run test with one input file only."""
    play_record(name, timeout)
    export(name+"-out.wav", timeout)

def quick_test(timeout):
    """Quick test to ensure pipe is working."""
    do_command('Help: CommandName=Help', timeout)

if __name__ == '__main__':
    t0 = time.time()
    local_time = time.localtime(t0)
    msg = 'Start Time is {}/{}/{} {}:{}:{}'
    logger.info(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
                        local_time.tm_hour,local_time.tm_min,local_time.tm_sec))

    quick_test(10)

    PATH = ""
    while not os.path.isdir(PATH):
        PATH = os.path.realpath(input('Path to test folder: '))
        if not os.path.isdir(PATH):
            #print('Invalid path. Try again.')
            msg = 'Invalid path. Try again.'
            logger.info(msg)

    msg = 'Test folder:{}'
    logger.info(msg.format(PATH))

    INFILE = ""
    while not os.path.isfile(os.path.join(PATH, INFILE)):
        INFILE = input('Name of input WAV file: ')
        # Ensure we have the .wav extension.
        INFILE = os.path.splitext(INFILE)[0] + '.wav'
        if not os.path.isfile(os.path.join(PATH, INFILE)):
            #print(f"{os.path.join(PATH, INFILE)} not found. Try again.")
            msg = '{} not found. Try again.'
            logger.info(msg.format(os.path.join(PATH, INFILE) ))
        else:
            #print(f"Input file: {os.path.join(PATH, INFILE)}")
            msg = 'Input file:{}.'
            logger.info(msg.format(os.path.join(PATH, INFILE) ))
    # Remove file extension.
    INFILE = os.path.splitext(INFILE)[0]

    do_one_file(INFILE, 10)

    msg = 'Time duration: {:.2f} seconds.'
    logger.info(msg.format( time.time() - t0))