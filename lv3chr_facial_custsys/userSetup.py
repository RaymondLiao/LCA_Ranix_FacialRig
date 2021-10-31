import sys

lcrig_lv3chr_facialsys_dir = "D:/Maya Projects/LCA_Ranix_FacialRig/lv3chr_facial_custsys"
if lcrig_lv3chr_facialsys_dir not in sys.path:
    sys.path.append(lcrig_lv3chr_facialsys_dir)

from demo import lv3chr_facial_custsys_demo; reload(lv3chr_facial_custsys_demo)