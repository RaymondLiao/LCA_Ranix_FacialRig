import sys

is_lca_machine = True

lcrig_lv3chr_facialsys_dir = "D:/Raymond/Programming/LCA/LCA_Ranix_FacialRig/lv3chr_facialsys"
if is_lca_machine:
    lcrig_lv3chr_facialsys_dir = 'D:/liaosheng/Light Chaser Animation Studios/' \
                                    'Proj_Lv3Char_Facial_System/Codes/LCA_Ranix_FacialRig/lv3chr_facialsys'

if lcrig_lv3chr_facialsys_dir not in sys.path:
    sys.path.append(lcrig_lv3chr_facialsys_dir)

from demo import lv3chr_facialsys_demo; reload(lv3chr_facialsys_demo)
lv3chr_facialsys_demo.lc3chr_facialsys_construct()