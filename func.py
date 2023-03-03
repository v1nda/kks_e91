import cirq
import math

def random():

        q0 = cirq.LineQubit.range(1)[0]
        circuit = cirq.Circuit(
                cirq.H(q0),
                cirq.MeasurementGate(1).on(q0),
        )

        res = 3

        while res == 3:

                simulator = cirq.Simulator()
                result = simulator.run(circuit, repetitions=2)

                bits = result.data.to_dict()['']

                res = cirq.big_endian_bits_to_int([bits[0], bits[1]])

        # print(res)
        return(res)


def singlet(q0, q1):
        
        m1 = cirq.Moment([cirq.X(q0), cirq.X(q1)])
        m2 = cirq.H(q0)
        m3 = cirq.CNOT(q0, q1)

        return([m1, m2, m3])

def alice_basis_construction(basis, q):

        moments = []

        if basis == 0:
                moments.append(cirq.H(q))
        elif basis == 1:
                moments.append(cirq.rz(math.pi/2).on(q))
                moments.append(cirq.H(q))
                moments.append(cirq.rz(math.pi/4).on(q))
                moments.append(cirq.H(q))
        # elif basis == 2:
        #         moments.append(cirq.measure(q))
        
        return moments

def bob_basis_construction(basis, q):

        moments = []

        if basis == 0:
                moments.append(cirq.rz(math.pi/2).on(q))
                moments.append(cirq.H(q))
                moments.append(cirq.rz(math.pi/4).on(q))
                moments.append(cirq.H(q))
        elif basis == 2:
                moments.append(cirq.rz(rads=math.pi/2).on(q))
                moments.append(cirq.H(q))
                moments.append(cirq.rz(rads=(0-math.pi)/4).on(q))
                moments.append(cirq.H(q))
        # elif basis == 1:
        #         moments.append(cirq.measure(q))
        
        return moments

def basis_comparison(b0, b1):

        if (b0 == 1 and b1 == 0) or (b0 == 2 and b1 == 1):
                return True
        else:
                return False


def key_statistic_calc(key0, key1, clean_key):
        
        p0_key0 = 0
        p0_key1 = 0
        p0_clean_key = 0
        for i in range(len(key0)):
                
                if key0[i] == 0:
                        p0_key0 += 1
                if key1[i] == 0:
                        p0_key1 += 1
                
                if i < len(clean_key) and clean_key[i] == 0:
                        p0_clean_key += 1

        p0_key0 = round(p0_key0 / len(key0) * 100, 4)
        p0_key1 = round(p0_key1 / len(key1) * 100, 4)
        p0_clean_key = round(p0_clean_key / len(clean_key) * 100, 4)

        print('Статистика по ключу Алисы:')
        print('\tдлина ключа: \t\t\t' + str(len(key0)))
        print('\tвероятность появления 0: \t' + str(p0_key0) + '%')
        
        print()
        print('Статистика по ключу Боба:')
        print('\tдлина ключа: \t\t\t' + str(len(key1)))
        print('\tвероятность появления 0: \t' + str(p0_key1) + '%')
        
        print()
        print('Статистика по чистому ключу:')
        print('\tдлина ключа: \t\t\t' + str(len(clean_key)))
        print('\tвероятность появления 0: \t' + str(p0_clean_key) + '%')

        return
