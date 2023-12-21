import threading
import time
import os
import logging

import P2Pro.video
import P2Pro.P2Pro_cmd as P2Pro_CMD
import P2Pro.recorder

logging.basicConfig()
logging.getLogger('P2Pro.P2Pro_cmd').setLevel(logging.DEBUG)
logging.getLogger('P2Pro.video').setLevel(logging.DEBUG)

try:
    vid = P2Pro.video.Video()
    video_thread = threading.Thread(target=vid.open, args=(1,))
    video_thread.start()

    while not vid.video_running:
        time.sleep(0.01)

    rec = P2Pro.recorder.VideoRecorder(vid.frame_queue[1], "test", audio=False)
    rec.start()

    cam_cmd = P2Pro_CMD.P2Pro()

    # print (cam_cmd._dev)
    # cam_cmd._standard_cmd_write(P2Pro_CMD.CmdCode.sys_reset_to_rom)
    # print(cam_cmd._standard_cmd_read(P2Pro_CMD.CmdCode.cur_vtemp, 0, 2))
    # print(cam_cmd._standard_cmd_read(P2Pro_CMD.CmdCode.shutter_vtemp, 0, 2))

    time.sleep(1)
    cam_cmd.pseudo_color_set(0, P2Pro_CMD.PseudoColorTypes.PSEUDO_IRON_RED)
    time.sleep(1)
    for prop in P2Pro_CMD.AutoShutterParams:
        print(f"param {prop.name}: {cam_cmd.get_auto_shutter_params(prop)}")

    #time.sleep(3)
    #print("=== shutter test ===")
    #cam_cmd.get_shutter_status()
    #cam_cmd.set_shutter(1)
    #cam_cmd.set_shutter_control(0)
    #cam_cmd.get_shutter_status()
    #time.sleep(2)
    #cam_cmd.set_shutter_control(1)
    #cam_cmd.set_shutter(0)
    #cam_cmd.get_shutter_status()
    #print("=====================")

    time.sleep(3)
    rec.stop()
    os._exit(1)

except KeyboardInterrupt:
    print("Killing...")
    os._exit(1)
    pass
os._exit(0)