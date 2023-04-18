import esp
import gc
from nettools import start_access_point

esp.osdebug(None)
gc.collect()
start_access_point()
