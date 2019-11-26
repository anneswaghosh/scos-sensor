import matplotlib.pyplot as plt
import numpy as np

def plot_psd (psd, freq):
       #plt.semilogy(freq, psd)
       #plt.ylim([0.5e-3, 1])
       plt.plot (freq, psd)
       plt.ylim(-130, -105)
       #plt.yscale('symlog')
       plt.xlabel('frequency [Hz]')
       plt.ylabel('PSD [V**2/Hz]')
       plt.grid(True)
       plt.show()



psd = np.array([-121.827805, -121.80466 , -121.69081 , -121.56268 , -121.502075,
       -121.4286  , -121.29037 , -121.17303 , -121.042694, -120.94995 ,
       -120.876205, -120.726364, -120.67719 , -120.701004, -120.67868 ,
       -120.69862 , -120.70882 , -120.775665, -120.850525, -120.94349 ,
       -121.04936 , -121.175674, -121.26861 , -121.39088 , -121.500854,
       -121.65457 , -121.78417 , -121.89022 , -121.99899 , -122.13553 ,
       -122.23122 , -122.36073 , -122.49046 , -122.65904 , -122.77928 ,
       -122.854195, -122.96555 , -123.08236 , -123.161476, -123.291466,
       -123.378815, -123.469635, -123.541855, -123.66836 , -123.79675 ,
       -123.894165, -123.99071 , -124.049866, -124.1068  , -124.25338 ,
       -124.19636 , -123.596924, -124.1529  , -124.568985, -124.4952  ,
       -124.40742 , -124.28109 , -124.17076 , -124.12446 , -124.0621  ,
       -124.076836, -124.09073 , -124.16992 , -124.2183  , -124.331856,
       -124.354935, -124.31336 , -124.228294, -124.264206, -124.40215 ,
       -124.55928 , -124.5647  , -124.4921  , -124.53253 , -124.5453  ,
       -124.5591  , -124.6012  , -124.65813 , -124.79058 , -124.817276,
       -124.77149 , -124.67309 , -124.66308 , -124.80055 , -124.87964 ,
       -124.88925 , -124.810745, -124.87923 , -124.93546 , -124.83016 ,
       -124.84635 , -125.017426, -125.28594 , -125.3429  , -117.041695,
       -110.02295 , -108.24684 , -109.88519 , -111.67365 , -111.1124  ,
       -110.882965, -110.85686 , -111.357834, -111.81477 , -110.03536 ,
       -108.03704 , -107.42585 , -108.21573 , -110.05878 , -111.88542 ,
       -111.66962 , -112.45853 , -112.87713 , -113.580284, -114.055176,
       -111.50839 , -111.36071 , -112.520386, -113.677025, -113.169464,
       -113.901855, -115.63972 , -117.14043 , -115.6275  , -114.200554,
       -113.079666, -111.94115 , -111.85437 , -110.898735, -111.84185 ,
       -114.5779  , -113.359314, -112.993576, -113.37105 , -112.925964,
       -113.335655, -117.78138 , -125.85185 , -126.30065 , -126.0402  ,
       -125.93708 , -125.963356, -126.01002 , -126.11233 , -126.101166,
       -126.14137 , -126.12418 , -126.14046 , -125.98388 , -125.91877 ,
       -125.86606 , -125.83306 , -125.766174, -125.62164 , -125.56248 ,
       -125.62366 , -125.607315, -125.63354 , -125.51602 , -125.530975,
       -125.61737 , -125.57522 , -125.45445 , -125.35182 , -125.363464,
       -125.26466 , -125.24057 , -125.35829 , -125.364975, -125.3188  ,
       -125.22884 , -125.135254, -125.214966, -125.48773 , -125.65055 ,
       -125.898964, -126.24772 , -126.59532 , -126.748886, -126.7238  ,
       -126.404175, -125.94173 , -125.65234 , -125.57864 , -125.484024,
       -125.31524 , -125.27047 , -125.18065 , -125.115814, -125.048294,
       -124.829445, -124.58523 , -124.77049 , -124.94117 , -124.83992 ,
       -124.71347 , -124.65904 , -125.06321 , -125.79274 , -125.53653 ,
       -124.54601 , -124.12512 , -124.01132 , -123.86379 , -123.82674 ,
       -123.74573 , -123.7741  , -123.63443 , -123.70194 , -123.77807 ,
       -123.743866, -123.85925 , -123.98425 , -124.08258 , -124.09297 ,
       -124.1475  , -124.4321  , -118.83913 , -113.19861 , -112.36821 ,
       -113.47096 , -111.628235, -109.931175, -111.45395 , -112.324844,
       -112.3248  , -112.08389 , -111.656334, -110.023125, -107.64206 ,
       -108.75671 , -112.276985, -111.35631 , -110.35165 , -109.58172 ,
       -111.14933 , -111.845695, -109.83631 , -108.769424, -110.882965,
       -113.6904  , -111.647675, -109.42291 , -111.09803 , -113.0244  ,
       -112.79179 , -110.70267 , -109.198395, -110.24522 , -112.289185,
       -111.99609 , -110.41118 , -109.4537  , -108.270584, -108.957   ,
       -112.029175, -114.36997 , -108.78015 , -107.3197  , -107.98425 ,
       -108.951614, -110.046814, -110.15366 , -110.357925, -110.95132 ,
       -111.82395 , -109.050766, -107.95581 , -108.11692 , -110.8221  ,
       -120.285866, -123.80562 , -123.64476 , -123.43655 , -123.41705 ,
       -123.35107 , -123.3232  , -123.3319  , -123.38692 , -123.318665,
       -123.33902 , -123.31085 , -123.41063 , -123.50933 , -123.643105,
       -123.683846, -123.950516, -124.4215  , -124.564354, -123.7769  ,
       -122.86801 , -122.502174, -122.34315 , -122.46769 , -122.62564 ,
       -122.47895 , -122.25243 , -122.15056 , -122.24689 , -122.488174,
       -122.52318 , -122.58622 , -122.748   , -122.91194 , -123.178215,
       -123.593216, -124.42901 , -125.204956, -125.386444, -125.412964,
       -125.499   , -125.44942 , -125.514595, -125.51891 , -125.51138 ,
       -125.579185, -125.59188 , -125.60344 , -125.657234, -125.67235 ,
       -125.712746, -125.76053 , -125.7396  , -125.76954 , -125.785614,
       -125.80133 , -125.81387 , -125.77709 , -125.807816, -125.87035 ,
       -125.89879 , -125.88881 , -125.94425 , -125.97729 , -125.9338  ,
       -125.96112 , -126.036255, -126.02371 , -126.0721  , -126.15576 ,
       -126.095566, -126.05683 , -126.08255 , -126.099335, -126.15846 ,
       -126.2744  , -126.286476, -126.25032 , -126.37204 , -126.40712 ,
       -126.37764 , -126.37404 , -126.36717 , -126.39289 , -126.47637 ,
       -126.48202 , -126.54875 , -126.56908 , -126.306946, -126.3675  ,
       -126.50755 , -126.538345, -126.17139 , -120.08115 , -115.62252 ,
       -114.86489 , -114.89183 , -115.59884 , -116.31054 , -116.3113  ,
       -115.7911  , -115.519455, -115.802376, -116.35033 , -115.97067 ,
       -115.8287  , -116.25263 , -116.94313 , -117.04555 , -116.51078 ,
       -116.34068 , -116.805374, -116.99237 , -116.0659  , -115.81879 ,
       -116.01813 , -116.30429 , -116.56018 , -116.30971 , -116.25914 ,
       -116.895584, -117.73105 , -117.74304 , -116.715385, -115.93141 ,
       -116.37132 , -116.66504 , -116.44184 , -116.22772 , -116.42806 ,
       -116.9033  , -117.20429 , -117.31014 , -117.471535, -117.37229 ,
       -116.69244 , -116.37785 , -116.45015 , -116.51431 , -116.94782 ,
       -116.560455, -116.05378 , -116.95518 , -117.20044 , -116.66329 ,
       -116.585014, -116.825645, -117.20378 , -117.2929  , -117.18056 ,
       -117.30053 , -117.008194, -116.92238 , -117.39285 , -117.378914,
       -117.67086 , -118.14526 , -118.395164, -118.328476, -117.92996 ,
       -117.744   , -118.02963 , -118.16186 , -117.79243 , -117.37413 ,
       -116.641815, -115.86133 , -116.01479 , -116.28651 , -116.63421 ,
       -117.036865, -117.149895, -117.41708 , -117.35043 , -117.17012 ,
       -117.369576, -117.47621 , -117.47883 , -117.45242 , -117.519516,
       -117.45835 , -117.65281 , -117.9247  , -117.87055 , -117.97209 ,
       -118.64015 , -121.65033 , -124.49002 , -124.598076, -124.45072 ,
       -124.27848 , -124.06024 , -124.15778 , -124.07844 , -123.98187 ,
       -123.87727 , -123.81731 , -123.67352 , -123.58138 , -123.51848 ,
       -123.44028 , -123.35675 , -123.22919 , -123.13102 , -123.07428 ,
       -122.97352 , -122.83969 , -122.742294, -122.642586, -122.523796,
       -122.39592 , -122.26851 , -122.14427 , -122.07307 , -121.97651 ,
       -121.79581 , -121.67198 , -121.56117 , -121.443474, -121.32262 ,
       -121.14679 , -121.11457 , -121.00717 , -120.93039 , -120.83576 ,
       -120.78025 , -120.68858 , -120.63719 , -120.62672 , -120.60566 ,
       -120.62468 , -120.68493 , -120.796234, -120.92187 , -121.0189  ,
       -121.10849 , -121.223175, -121.38324 , -121.59324 , -121.60305 ,
       -121.669785, -121.796295])



labels = np.array([2.31500000e+09, 2.31509766e+09, 2.31519531e+09, 2.31529297e+09,
       2.31539062e+09, 2.31548828e+09, 2.31558594e+09, 2.31568359e+09,
       2.31578125e+09, 2.31587891e+09, 2.31597656e+09, 2.31607422e+09,
       2.31617188e+09, 2.31626953e+09, 2.31636719e+09, 2.31646484e+09,
       2.31656250e+09, 2.31666016e+09, 2.31675781e+09, 2.31685547e+09,
       2.31695312e+09, 2.31705078e+09, 2.31714844e+09, 2.31724609e+09,
       2.31734375e+09, 2.31744141e+09, 2.31753906e+09, 2.31763672e+09,
       2.31773438e+09, 2.31783203e+09, 2.31792969e+09, 2.31802734e+09,
       2.31812500e+09, 2.31822266e+09, 2.31832031e+09, 2.31841797e+09,
       2.31851562e+09, 2.31861328e+09, 2.31871094e+09, 2.31880859e+09,
       2.31890625e+09, 2.31900391e+09, 2.31910156e+09, 2.31919922e+09,
       2.31929688e+09, 2.31939453e+09, 2.31949219e+09, 2.31958984e+09,
       2.31968750e+09, 2.31978516e+09, 2.31988281e+09, 2.31998047e+09,
       2.32007812e+09, 2.32017578e+09, 2.32027344e+09, 2.32037109e+09,
       2.32046875e+09, 2.32056641e+09, 2.32066406e+09, 2.32076172e+09,
       2.32085938e+09, 2.32095703e+09, 2.32105469e+09, 2.32115234e+09,
       2.32125000e+09, 2.32134766e+09, 2.32144531e+09, 2.32154297e+09,
       2.32164062e+09, 2.32173828e+09, 2.32183594e+09, 2.32193359e+09,
       2.32203125e+09, 2.32212891e+09, 2.32222656e+09, 2.32232422e+09,
       2.32242188e+09, 2.32251953e+09, 2.32261719e+09, 2.32271484e+09,
       2.32281250e+09, 2.32291016e+09, 2.32300781e+09, 2.32310547e+09,
       2.32320312e+09, 2.32330078e+09, 2.32339844e+09, 2.32349609e+09,
       2.32359375e+09, 2.32369141e+09, 2.32378906e+09, 2.32388672e+09,
       2.32398438e+09, 2.32408203e+09, 2.32417969e+09, 2.32427734e+09,
       2.32437500e+09, 2.32447266e+09, 2.32457031e+09, 2.32466797e+09,
       2.32476562e+09, 2.32486328e+09, 2.32496094e+09, 2.32505859e+09,
       2.32515625e+09, 2.32525391e+09, 2.32535156e+09, 2.32544922e+09,
       2.32554688e+09, 2.32564453e+09, 2.32574219e+09, 2.32583984e+09,
       2.32593750e+09, 2.32603516e+09, 2.32613281e+09, 2.32623047e+09,
       2.32632812e+09, 2.32642578e+09, 2.32652344e+09, 2.32662109e+09,
       2.32671875e+09, 2.32681641e+09, 2.32691406e+09, 2.32701172e+09,
       2.32710938e+09, 2.32720703e+09, 2.32730469e+09, 2.32740234e+09,
       2.32750000e+09, 2.32759766e+09, 2.32769531e+09, 2.32779297e+09,
       2.32789062e+09, 2.32798828e+09, 2.32808594e+09, 2.32818359e+09,
       2.32828125e+09, 2.32837891e+09, 2.32847656e+09, 2.32857422e+09,
       2.32867188e+09, 2.32876953e+09, 2.32886719e+09, 2.32896484e+09,
       2.32906250e+09, 2.32916016e+09, 2.32925781e+09, 2.32935547e+09,
       2.32945312e+09, 2.32955078e+09, 2.32964844e+09, 2.32974609e+09,
       2.32984375e+09, 2.32994141e+09, 2.33003906e+09, 2.33013672e+09,
       2.33023438e+09, 2.33033203e+09, 2.33042969e+09, 2.33052734e+09,
       2.33062500e+09, 2.33072266e+09, 2.33082031e+09, 2.33091797e+09,
       2.33101562e+09, 2.33111328e+09, 2.33121094e+09, 2.33130859e+09,
       2.33140625e+09, 2.33150391e+09, 2.33160156e+09, 2.33169922e+09,
       2.33179688e+09, 2.33189453e+09, 2.33199219e+09, 2.33208984e+09,
       2.33218750e+09, 2.33228516e+09, 2.33238281e+09, 2.33248047e+09,
       2.33257812e+09, 2.33267578e+09, 2.33277344e+09, 2.33287109e+09,
       2.33296875e+09, 2.33306641e+09, 2.33316406e+09, 2.33326172e+09,
       2.33335938e+09, 2.33345703e+09, 2.33355469e+09, 2.33365234e+09,
       2.33375000e+09, 2.33384766e+09, 2.33394531e+09, 2.33404297e+09,
       2.33414062e+09, 2.33423828e+09, 2.33433594e+09, 2.33443359e+09,
       2.33453125e+09, 2.33462891e+09, 2.33472656e+09, 2.33482422e+09,
       2.33492188e+09, 2.33501953e+09, 2.33511719e+09, 2.33521484e+09,
       2.33531250e+09, 2.33541016e+09, 2.33550781e+09, 2.33560547e+09,
       2.33570312e+09, 2.33580078e+09, 2.33589844e+09, 2.33599609e+09,
       2.33609375e+09, 2.33619141e+09, 2.33628906e+09, 2.33638672e+09,
       2.33648438e+09, 2.33658203e+09, 2.33667969e+09, 2.33677734e+09,
       2.33687500e+09, 2.33697266e+09, 2.33707031e+09, 2.33716797e+09,
       2.33726562e+09, 2.33736328e+09, 2.33746094e+09, 2.33755859e+09,
       2.33765625e+09, 2.33775391e+09, 2.33785156e+09, 2.33794922e+09,
       2.33804688e+09, 2.33814453e+09, 2.33824219e+09, 2.33833984e+09,
       2.33843750e+09, 2.33853516e+09, 2.33863281e+09, 2.33873047e+09,
       2.33882812e+09, 2.33892578e+09, 2.33902344e+09, 2.33912109e+09,
       2.33921875e+09, 2.33931641e+09, 2.33941406e+09, 2.33951172e+09,
       2.33960938e+09, 2.33970703e+09, 2.33980469e+09, 2.33990234e+09,
       2.34000000e+09, 2.34009766e+09, 2.34019531e+09, 2.34029297e+09,
       2.34039062e+09, 2.34048828e+09, 2.34058594e+09, 2.34068359e+09,
       2.34078125e+09, 2.34087891e+09, 2.34097656e+09, 2.34107422e+09,
       2.34117188e+09, 2.34126953e+09, 2.34136719e+09, 2.34146484e+09,
       2.34156250e+09, 2.34166016e+09, 2.34175781e+09, 2.34185547e+09,
       2.34195312e+09, 2.34205078e+09, 2.34214844e+09, 2.34224609e+09,
       2.34234375e+09, 2.34244141e+09, 2.34253906e+09, 2.34263672e+09,
       2.34273438e+09, 2.34283203e+09, 2.34292969e+09, 2.34302734e+09,
       2.34312500e+09, 2.34322266e+09, 2.34332031e+09, 2.34341797e+09,
       2.34351562e+09, 2.34361328e+09, 2.34371094e+09, 2.34380859e+09,
       2.34390625e+09, 2.34400391e+09, 2.34410156e+09, 2.34419922e+09,
       2.34429688e+09, 2.34439453e+09, 2.34449219e+09, 2.34458984e+09,
       2.34468750e+09, 2.34478516e+09, 2.34488281e+09, 2.34498047e+09,
       2.34507812e+09, 2.34517578e+09, 2.34527344e+09, 2.34537109e+09,
       2.34546875e+09, 2.34556641e+09, 2.34566406e+09, 2.34576172e+09,
       2.34585938e+09, 2.34595703e+09, 2.34605469e+09, 2.34615234e+09,
       2.34625000e+09, 2.34634766e+09, 2.34644531e+09, 2.34654297e+09,
       2.34664062e+09, 2.34673828e+09, 2.34683594e+09, 2.34693359e+09,
       2.34703125e+09, 2.34712891e+09, 2.34722656e+09, 2.34732422e+09,
       2.34742188e+09, 2.34751953e+09, 2.34761719e+09, 2.34771484e+09,
       2.34781250e+09, 2.34791016e+09, 2.34800781e+09, 2.34810547e+09,
       2.34820312e+09, 2.34830078e+09, 2.34839844e+09, 2.34849609e+09,
       2.34859375e+09, 2.34869141e+09, 2.34878906e+09, 2.34888672e+09,
       2.34898438e+09, 2.34908203e+09, 2.34917969e+09, 2.34927734e+09,
       2.34937500e+09, 2.34947266e+09, 2.34957031e+09, 2.34966797e+09,
       2.34976562e+09, 2.34986328e+09, 2.34996094e+09, 2.35005859e+09,
       2.35015625e+09, 2.35025391e+09, 2.35035156e+09, 2.35044922e+09,
       2.35054688e+09, 2.35064453e+09, 2.35074219e+09, 2.35083984e+09,
       2.35093750e+09, 2.35103516e+09, 2.35113281e+09, 2.35123047e+09,
       2.35132812e+09, 2.35142578e+09, 2.35152344e+09, 2.35162109e+09,
       2.35171875e+09, 2.35181641e+09, 2.35191406e+09, 2.35201172e+09,
       2.35210938e+09, 2.35220703e+09, 2.35230469e+09, 2.35240234e+09,
       2.35250000e+09, 2.35259766e+09, 2.35269531e+09, 2.35279297e+09,
       2.35289062e+09, 2.35298828e+09, 2.35308594e+09, 2.35318359e+09,
       2.35328125e+09, 2.35337891e+09, 2.35347656e+09, 2.35357422e+09,
       2.35367188e+09, 2.35376953e+09, 2.35386719e+09, 2.35396484e+09,
       2.35406250e+09, 2.35416016e+09, 2.35425781e+09, 2.35435547e+09,
       2.35445312e+09, 2.35455078e+09, 2.35464844e+09, 2.35474609e+09,
       2.35484375e+09, 2.35494141e+09, 2.35503906e+09, 2.35513672e+09,
       2.35523438e+09, 2.35533203e+09, 2.35542969e+09, 2.35552734e+09,
       2.35562500e+09, 2.35572266e+09, 2.35582031e+09, 2.35591797e+09,
       2.35601562e+09, 2.35611328e+09, 2.35621094e+09, 2.35630859e+09,
       2.35640625e+09, 2.35650391e+09, 2.35660156e+09, 2.35669922e+09,
       2.35679688e+09, 2.35689453e+09, 2.35699219e+09, 2.35708984e+09,
       2.35718750e+09, 2.35728516e+09, 2.35738281e+09, 2.35748047e+09,
       2.35757812e+09, 2.35767578e+09, 2.35777344e+09, 2.35787109e+09,
       2.35796875e+09, 2.35806641e+09, 2.35816406e+09, 2.35826172e+09,
       2.35835938e+09, 2.35845703e+09, 2.35855469e+09, 2.35865234e+09,
       2.35875000e+09, 2.35884766e+09, 2.35894531e+09, 2.35904297e+09,
       2.35914062e+09, 2.35923828e+09, 2.35933594e+09, 2.35943359e+09,
       2.35953125e+09, 2.35962891e+09, 2.35972656e+09, 2.35982422e+09,
       2.35992188e+09, 2.36001953e+09, 2.36011719e+09, 2.36021484e+09,
       2.36031250e+09, 2.36041016e+09, 2.36050781e+09, 2.36060547e+09,
       2.36070312e+09, 2.36080078e+09, 2.36089844e+09, 2.36099609e+09,
       2.36109375e+09, 2.36119141e+09, 2.36128906e+09, 2.36138672e+09,
       2.36148438e+09, 2.36158203e+09, 2.36167969e+09, 2.36177734e+09,
       2.36187500e+09, 2.36197266e+09, 2.36207031e+09, 2.36216797e+09,
       2.36226562e+09, 2.36236328e+09, 2.36246094e+09, 2.36255859e+09,
       2.36265625e+09, 2.36275391e+09, 2.36285156e+09, 2.36294922e+09,
       2.36304688e+09, 2.36314453e+09, 2.36324219e+09, 2.36333984e+09,
       2.36343750e+09, 2.36353516e+09, 2.36363281e+09, 2.36373047e+09,
       2.36382812e+09, 2.36392578e+09, 2.36402344e+09, 2.36412109e+09,
       2.36421875e+09, 2.36431641e+09, 2.36441406e+09, 2.36451172e+09,
       2.36460938e+09, 2.36470703e+09, 2.36480469e+09, 2.36490234e+09])
  
plot_psd (psd, labels)
