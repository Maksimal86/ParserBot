
def main(rigs_hashrate,name_of_coin):
    if  rigs_hashrate < 1000:
        hashrate = (name_of_coin + " " + str(round(rigs_hashrate, 2)) + 'H(Sol)')
    elif rigs_hashrate < 1000000:
        hashrate = (name_of_coin + " " + str(round(rigs_hashrate / 1000, 1)) + 'KH')
    elif rigs_hashrate < 1000000000:
        hashrate = (name_of_coin + " " + str(round(rigs_hashrate / 1000000, 2)) + 'MH')
    elif rigs_hashrate < 1000000000000:
        hashrate = (name_of_coin + " " + str(round(rigs_hashrate / 1000000000, 2)) + 'GH')
    else:
        return rigs_hashrate
    return main


