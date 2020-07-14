import numpy as np

def calc_snr(qam_order, ber):
    from scipy.special import erfcinv
    def qfunc_inc(y):
        return np.sqrt(2) * erfcinv(2 * y)

    symbol_error = ber * np.log2(qam_order)
    x = 1 - np.sqrt(1 - symbol_error)

    return 10 * np.log10((qam_order - 1) / 3 * qfunc_inc(x / (2 * (1 - np.sqrt(1 / qam_order)))) ** 2)




def gn_results(signal_power,signal_index):
    import matplotlib.pyplot as plt
    from library.gn_model import Signal,Span,Edfa
    snr = []

    space = 50e9
    baud_rate = 33e9

    power_lin = (10 ** (signal_power / 10)) * 0.001
    # print(power_lin)

    sigs = [
        Signal(signal=power_lin, nli=0, ase=0, carri=193.1e12 + j * space, baudrate=baud_rate, number=j,
               mf='dp-16qam')

        for j in signal_index]
    spans = []
    edfas = []
    for length in [50, 75.7, 80, 48.8, 73.2, 80, 75.7, 40, 50.5, 40, 68.8, 48.8, 60, 48.8, 73.2, 73.2, 48.8]:
        spans.append(Span(length=length, D=16.7, gamma=1.3, lam=1550e-9, alpha=0.2))
        edfas.append(Edfa(gain=length * 0.2, nf=5))
    for under_test_channel in sigs:
        for idx, span in enumerate(spans):
            span.prop(under_test_channel, sigs)
            edfas[idx].prop(under_test_channel)
        snr.append(under_test_channel.signal / (under_test_channel.nli + under_test_channel.ase))
    snr = np.array(snr)

    return 10 * np.log10(np.array(snr))


def main(signal_index,bers):
    import matlab
    import matlab.engine as eng
    engine = eng.connect_matlab()
    qam_order = 4
    # bers = [0.00223,0.00264,0.00262,0.00275,0.00294,0.00206,0.00566]
    signal_power = 1
    # signal_index = [2,3,4,5,6,7,8]

    gn_snr = gn_results(signal_power,signal_index)
    snrs = []
    for ber in bers:
        snrs.append(calc_snr(qam_order,ber))

    error = matlab.double((np.array(gn_snr) - np.array(snrs)).tolist())
    return error





def calc_error(signal_index,ber_established,unestablished_signal_index,real_ber_established,error_gpr_fitted):
    import copy
    error = main(signal_index, ber_established)
    print(error)
    gn_snr = []
    for unestablished_channel in unestablished_signal_index:
        signal_index_temp = copy.deepcopy(signal_index)
        signal_index_temp.append(unestablished_channel)
        gn_snr.append(gn_results(1, signal_index_temp)[-1])
    #
    gn_snr_modification = np.array(gn_snr) - np.array(error_gpr_fitted)

    real_snr = []
    for ber in real_ber_established:
        real_snr.append(calc_snr(4, ber))
    print(real_snr)
    print(gn_snr_modification)
    print(gn_snr_modification - np.array(real_snr))


if __name__ == '__main__':
    # signal_index = [2,5,8,11,14,17,20]
    # bers = [0.00271,0.00388,0.00257,0.00223,0.00107,0.000688,0.00227]
    # error = main(signal_index,bers)
    # print(error)
    #
    # gn_snr = []
    # for unestablished_channel in [6,18,22,24]:
    #     signal_index = [2,5,8,11,14,17,20]
    #     signal_index.append(unestablished_channel)
    #     gn_snr.append(gn_results(1,signal_index)[-1])
    #
    # gn_snr_modification = np.array(gn_snr) - np.array([ 10.6418   , 9.5502  , 10.8185  , 10.5874])
    #
    # real_ber = [0.0052,0.00165,0.00256,0.0011]
    # real_snr = []
    #
    # for ber in real_ber:
    #     real_snr.append(calc_snr(4,ber))
    #
    # print(real_snr)
    # print(gn_snr_modification)
    # print(gn_snr_modification - np.array(real_snr))
############################################################################################################################################
############################################################################################################################################

    # 11
    # calc_error(signal_index=[2,7,12,17,22,27,32],ber_established=[0.00305,0.00213,0.00136,0.00084,0.000884,0.000571,0.00239],
    #            unestablished_signal_index=[5,15,24,37],real_ber_established=[0.00362,0.00129,0.00115,0.0013],error_gpr_fitted=[ 10.7005  ,  9.9262,    9.7454,   10.6459])

############################################################################################################################################
############################################################################################################################################

    #21
    # calc_error(signal_index=[40,41,42,43,44,45,46],ber_established=[0.000672,0.00109,0.000854,0.00113,0.00106,0.000939,0.00476],
    #            unestablished_signal_index=[47,48,50,52],real_ber_established=[0.00115,0.000713,0.000503,0.000407],error_gpr_fitted=[8.2440,8.1768,8.1768,8.1768])
    #
    # #26
    #
    # calc_error(signal_index=[40, 43, 46, 49, 62, 65, 68],
    #            ber_established=[0.000521, 0.00094, 0.00103, 0.00148, 0.00465, 0.00407, 0.0105],
    #            unestablished_signal_index=[44, 67, 70, 72],
    #            real_ber_established=[0.00165, 0.00967, 0.00652, 0.0052],
    #            error_gpr_fitted=[9.5811 ,11.7332 ,11.9740  , 12.1096])
    #31
    calc_error(signal_index=[40, 45, 50, 55, 60, 65, 70],
               ber_established=[0.000447, 0.00117, 0.00127, 0.00236, 0.00259, 0.00413, 0.0106],
               unestablished_signal_index=[43, 53, 63, 75],
               real_ber_established=[0.000883, 0.00234, 0.00559, 0.0096],
               error_gpr_fitted=[ 9.7174  , 10.2993  , 11.1243 ,  13.0497])
