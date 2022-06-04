class des():
    def __init__(self):
        # initializing DES encryption
        self.ip = [
            58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7,
        ]  # ip replacement

        self.ip1 = [
            40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25,
        ]  # ip replacement

        self.E = [
            32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1,
        ]  # E replacement

        self.P = [
            16, 7, 20, 21, 29, 12, 28, 17,
            1, 15, 23, 26, 5, 18, 31, 10,
            2, 8, 24, 14, 32, 27, 3, 9,
            19, 13, 30, 6, 22, 11, 4, 25,
        ]  # P replacement

        self.K = '0100100101001100010011110101011001000101010110010100111101010101'  # default key
        self.k1 = [
            57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4,
        ]  # key K! initial replacement

        self.K2 = [
            14, 17, 11, 24, 1, 5, 3, 28,
            15, 6, 21, 10, 23, 19, 12, 4,
            26, 8, 16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55, 30, 40,
            51, 45, 33, 48, 44, 49, 39, 56,
            34, 53, 46, 42, 50, 36, 29, 32,
        ]  # key smaller replacement

        self.K0 = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2,
                   2, 2, 1, ]  # loop change position's number

        self.S = [
            [
                0xe, 0x4, 0xd, 0x1, 0x2, 0xf, 0xb, 0x8, 0x3, 0xa, 0x6, 0xc, 0x5, 0x9, 0x0, 0x7,
                0x0, 0xf, 0x7, 0x4, 0xe, 0x2, 0xd, 0x1, 0xa, 0x6, 0xc, 0xb, 0x9, 0x5, 0x3, 0x8,
                0x4, 0x1, 0xe, 0x8, 0xd, 0x6, 0x2, 0xb, 0xf, 0xc, 0x9, 0x7, 0x3, 0xa, 0x5, 0x0,
                0xf, 0xc, 0x8, 0x2, 0x4, 0x9, 0x1, 0x7, 0x5, 0xb, 0x3, 0xe, 0xa, 0x0, 0x6, 0xd,
            ],
            [
                0xf, 0x1, 0x8, 0xe, 0x6, 0xb, 0x3, 0x4, 0x9, 0x7, 0x2, 0xd, 0xc, 0x0, 0x5, 0xa,
                0x3, 0xd, 0x4, 0x7, 0xf, 0x2, 0x8, 0xe, 0xc, 0x0, 0x1, 0xa, 0x6, 0x9, 0xb, 0x5,
                0x0, 0xe, 0x7, 0xb, 0xa, 0x4, 0xd, 0x1, 0x5, 0x8, 0xc, 0x6, 0x9, 0x3, 0x2, 0xf,
                0xd, 0x8, 0xa, 0x1, 0x3, 0xf, 0x4, 0x2, 0xb, 0x6, 0x7, 0xc, 0x0, 0x5, 0xe, 0x9,
            ],
            [
                0xa, 0x0, 0x9, 0xe, 0x6, 0x3, 0xf, 0x5, 0x1, 0xd, 0xc, 0x7, 0xb, 0x4, 0x2, 0x8,
                0xd, 0x7, 0x0, 0x9, 0x3, 0x4, 0x6, 0xa, 0x2, 0x8, 0x5, 0xe, 0xc, 0xb, 0xf, 0x1,
                0xd, 0x6, 0x4, 0x9, 0x8, 0xf, 0x3, 0x0, 0xb, 0x1, 0x2, 0xc, 0x5, 0xa, 0xe, 0x7,
                0x1, 0xa, 0xd, 0x0, 0x6, 0x9, 0x8, 0x7, 0x4, 0xf, 0xe, 0x3, 0xb, 0x5, 0x2, 0xc,
            ],
            [
                0x7, 0xd, 0xe, 0x3, 0x0, 0x6, 0x9, 0xa, 0x1, 0x2, 0x8, 0x5, 0xb, 0xc, 0x4, 0xf,
                0xd, 0x8, 0xb, 0x5, 0x6, 0xf, 0x0, 0x3, 0x4, 0x7, 0x2, 0xc, 0x1, 0xa, 0xe, 0x9,
                0xa, 0x6, 0x9, 0x0, 0xc, 0xb, 0x7, 0xd, 0xf, 0x1, 0x3, 0xe, 0x5, 0x2, 0x8, 0x4,
                0x3, 0xf, 0x0, 0x6, 0xa, 0x1, 0xd, 0x8, 0x9, 0x4, 0x5, 0xb, 0xc, 0x7, 0x2, 0xe,
            ],
            [
                0x2, 0xc, 0x4, 0x1, 0x7, 0xa, 0xb, 0x6, 0x8, 0x5, 0x3, 0xf, 0xd, 0x0, 0xe, 0x9,
                0xe, 0xb, 0x2, 0xc, 0x4, 0x7, 0xd, 0x1, 0x5, 0x0, 0xf, 0xa, 0x3, 0x9, 0x8, 0x6,
                0x4, 0x2, 0x1, 0xb, 0xa, 0xd, 0x7, 0x8, 0xf, 0x9, 0xc, 0x5, 0x6, 0x3, 0x0, 0xe,
                0xb, 0x8, 0xc, 0x7, 0x1, 0xe, 0x2, 0xd, 0x6, 0xf, 0x0, 0x9, 0xa, 0x4, 0x5, 0x3,
            ],
            [
                0xc, 0x1, 0xa, 0xf, 0x9, 0x2, 0x6, 0x8, 0x0, 0xd, 0x3, 0x4, 0xe, 0x7, 0x5, 0xb,
                0xa, 0xf, 0x4, 0x2, 0x7, 0xc, 0x9, 0x5, 0x6, 0x1, 0xd, 0xe, 0x0, 0xb, 0x3, 0x8,
                0x9, 0xe, 0xf, 0x5, 0x2, 0x8, 0xc, 0x3, 0x7, 0x0, 0x4, 0xa, 0x1, 0xd, 0xb, 0x6,
                0x4, 0x3, 0x2, 0xc, 0x9, 0x5, 0xf, 0xa, 0xb, 0xe, 0x1, 0x7, 0x6, 0x0, 0x8, 0xd,
            ],
            [
                0x4, 0xb, 0x2, 0xe, 0xf, 0x0, 0x8, 0xd, 0x3, 0xc, 0x9, 0x7, 0x5, 0xa, 0x6, 0x1,
                0xd, 0x0, 0xb, 0x7, 0x4, 0x9, 0x1, 0xa, 0xe, 0x3, 0x5, 0xc, 0x2, 0xf, 0x8, 0x6,
                0x1, 0x4, 0xb, 0xd, 0xc, 0x3, 0x7, 0xe, 0xa, 0xf, 0x6, 0x8, 0x0, 0x5, 0x9, 0x2,
                0x6, 0xb, 0xd, 0x8, 0x1, 0x4, 0xa, 0x7, 0x9, 0x5, 0x0, 0xf, 0xe, 0x2, 0x3, 0xc,
            ],
            [
                0xd, 0x2, 0x8, 0x4, 0x6, 0xf, 0xb, 0x1, 0xa, 0x9, 0x3, 0xe, 0x5, 0x0, 0xc, 0x7,
                0x1, 0xf, 0xd, 0x8, 0xa, 0x3, 0x7, 0x4, 0xc, 0x5, 0x6, 0xb, 0x0, 0xe, 0x9, 0x2,
                0x7, 0xb, 0x4, 0x1, 0x9, 0xc, 0xe, 0x2, 0x0, 0x6, 0xa, 0xd, 0xf, 0x3, 0x5, 0x8,
                0x2, 0x1, 0xe, 0x7, 0x4, 0xa, 0x8, 0xd, 0xf, 0xc, 0x9, 0x0, 0x3, 0x5, 0x6, 0xb,
            ],
        ]  # 18boxes, 48bits to 32bits

    def substitute(self, table: str, self_table: list) -> str:
        return "".join(table[i - 1] for i in self_table)

    def msg_bin(self, msg: str, n) -> list:

        bin_result = []
        binary_msg = ""
        for s in msg:
            decimal_s = ord(s)
            binary_s = bin(decimal_s)[2:]
            binary_s = '0'*(n-decimal_s.bit_length()) + binary_s  # n bits
            binary_msg += binary_s
        len_binary_msg = len(binary_msg)
        if len_binary_msg % 64 != 0:
            binary_msg += '0'*(64-(len_binary_msg % 64))
        for i in range(0, len_binary_msg, 64):
            bin_result.append(binary_msg[i:i+64])
        return bin_result

    def bin_to_char(self, bin_str, n) -> str:

        str_result = ""
        for i in range(0, len(bin_str), n):
            bin_str_bit = bin_str[i:i+n]
            str_result += chr(int(bin_str_bit, 2))
        return str_result

    def f_function(self, right: str, key: str) -> str:
        '''
        :param right: encrypt Right part
        :param key: current key
        :return: E expand,xor with key, box s to get 32 bits
        '''
        # E expand to R0
        e_result = self.substitute(right, self.E)
        # xor with key
        xor_result = self.x_or_function(e_result, key)
        # get into box s
        s_result = self.s_box_substitute(xor_result)
        # p replacement
        p_result = self.substitute(s_result, self.P)
        return p_result

    def getkey_list(self):
        '''
        :return: sub keys for each round
        '''
        key = self.substitute(self.K, self.k1)
        left_key = key[0:28]
        right_key = key[28:56]
        keys = []
        for i in range(1, 17):
            move = self.K0[i - 1]
            move_left = left_key[move:28] + left_key[0:move]
            move_right = right_key[move:28] + right_key[0:move]
            left_key = move_left
            right_key = move_right
            move_key = left_key + right_key
            ki = self.substitute(move_key, self.K2)
            keys.append(ki)
        return keys

    def x_or_function(self, xor1: str, xor2: str):

        size = len(xor1)
        result = ""
        for i in range(0, size):
            result += '0' if xor1[i] == xor2[i] else '1'
        return result

    def s_box_substitute(self, xor_result: str):
        '''
        :param xor_result: 48 bit
        :return: 32 bit
        '''
        result = ""
        for i in range(0, 8):
            # 48 bits data to 6 groups
            block = xor_result[i * 6:(i + 1) * 6]
            line = int(block[0] + block[5], 2)
            colmn = int(block[1:4], 2)
            res = bin(self.S[i][line * colmn])[2:]
            if len(res) < 4:
                res = '0' * (4 - len(res)) + res
            result += res
        return result

    def iterate(self, bin_msg: str, key_list: list):
        '''
        :param bin_plaintext: 64 bit
        :param key_list: list of 16 keys
        :return: F function & Left xor
        '''
        left = bin_msg[0:32]
        right = bin_msg[32:64]
        for i in range(0, 16):
            next_lift = right
            f_result = self.f_function(right, key_list[i])
            next_right = self.x_or_function(left, f_result)
            left = next_lift
            right = next_right
        bin_msg_result = left + right
        return bin_msg_result[32:] + bin_msg_result[:32]

    def encryption(self, msg, display=0):

        bin_msg_lists = self.msg_bin(msg, 16)
        demsg = ""
        key_list = self.getkey_list()
        for bin_msg in bin_msg_lists:
            # first ip replacement
            sub_ip = self.substitute(bin_msg, self.ip)
            ite_result = self.iterate(sub_ip, key_list)
            # inverse IP replacement
            sub_ip1 = self.substitute(ite_result, self.ip1)
            if display == 0:
                cip = str(hex(int(sub_ip1.encode(), 2)))[2:]
                if len(cip) < 16:
                    cip = '0'*(16-len(cip)) + cip
                demsg += cip
            else:
                demsg += self.bin_to_char(sub_ip1, 16)
        return demsg

    def decryption(self, demsg):

        msg = ""
        key_list = self.getkey_list()
        key_list = key_list[::-1]
        bin_demsg_list = []
        demsg_list = []
        for i in range(0, len(demsg), 16):
            demsg_list.append(demsg[i:i + 16])
        int_demsg = [int('0x'+a, 16) for a in demsg_list]
        for i in int_demsg:
            bin_cip = bin(i)[2:]
            if len(bin_cip) != 64:
                bin_cip = '0'*(64-len(bin_cip)) + bin_cip
            bin_demsg_list.append(bin_cip)
        for bin_demsg in bin_demsg_list:
            sub_ip = self.substitute(bin_demsg, self.ip)
            ite = self.iterate(sub_ip, key_list)
            sub_ip1 = self.substitute(ite, self.ip1)
            bin_sub_ip1 = ''
            for k in range(0, 64, 16):
                if sub_ip1[k:k+16] != "0000000000000000":
                    bin_sub_ip1 += sub_ip1[k:k+16]
            msg += self.bin_to_char(bin_sub_ip1, 16)
        return msg
