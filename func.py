import cirq
import math

def random(mod=3):

        q0 = cirq.LineQubit.range(1)[0]
        circuit = cirq.Circuit(
                cirq.H(q0),
                cirq.MeasurementGate(1).on(q0),
        )

        res = mod

        while res >= mod:

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

def eve_basis_construction(q):

        moments = []
        basis = random(mod=2)

        if basis == 0:
                moments.append(cirq.rz(math.pi/2).on(q))
                moments.append(cirq.H(q))
                moments.append(cirq.rz(math.pi/4).on(q))
                moments.append(cirq.H(q))

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

def eva_key_statistic(key, keyE):

        pT = 0
        for i in range(len(key)):
                
                if key[i] == keyE[i]:
                        pT += 1
                
        pT = round(pT / len(key) * 100, 4)

        print()
        print('Статистика угадывания Евой: \t', pT)



def do_one_iteration(bA, bB, eva=False, circ=True):

        qA = cirq.NamedQubit("Alice")
        qB = cirq.NamedQubit("Bob")

        circuit = cirq.Circuit()
        circuit.append(singlet(qA, qB))

        bases_coincided = basis_comparison(bA, bB)
        if not bases_coincided:
                print("Алисой и Бобом выбраны различные базисы:")
                print("\tзначение отброшено.")

                return

        circuit.append(alice_basis_construction(bA, qA))
        circuit.append(bob_basis_construction(bB, qB))

        if eva:
                circuit.append(eve_basis_construction(qB))
                circuit.append(cirq.measure(qB, key='Eva'))

        circuit.append(cirq.X(qB))
        circuit.append(cirq.measure(qA, qB, key='result'))

        if circ:
                print(circuit)
        simulator = cirq.Simulator()
        result = simulator.run(circuit, repetitions=1)

        print('Результат передачи:')
        print('\tАлиса: \t', int(result.measurements['result'][0][0]))
        print('\tБоб: \t', int(result.measurements['result'][0][1]))
        if eva:
                print('Результат перехвата:')
                print('\tЕва: \t', (int(result.measurements['Eva'][0][0]) + 1) % 2)

def key_generation(length, eva=False, stat=False):

        qA = cirq.NamedQubit("Alice")
        qB = cirq.NamedQubit("Bob")

        basesA = [random() for i in range(length)]
        basesB = [random() for i in range(length)]

        keyA = []
        keyB = []
        keyE = []
        clean_keyA = []
        clean_keyB = []
        clean_keyE = []
        discarded_keyA = []
        discarded_keyB = []
        
        for b in range(length):

                circuit = cirq.Circuit()
                circuit.append(singlet(qA, qB))

                circuit.append(alice_basis_construction(basesA[b], qA))
                circuit.append(bob_basis_construction(basesB[b], qB))

                if eva:
                        circuit.append(eve_basis_construction(qB))
                        circuit.append(cirq.measure(qB, key='Eva'))

                circuit.append(cirq.X(qB))
                circuit.append(cirq.measure(qA, qB, key='result'))

                simulator = cirq.Simulator()
                result = simulator.run(circuit, repetitions=1)

                keyA.append(int(result.measurements['result'][0][0]))
                keyB.append(int(result.measurements['result'][0][1]))

                if eva:
                        keyE.append((int(result.measurements['Eva'][0][0]) + 1) % 2)


        # Установление индексов совпавших базисов и формирование Алисой и Бобом своих чистых и отброшенных ключей
        for b in range(length):
                
                if basis_comparison(basesA[b], basesB[b]):
                        clean_keyA.append(keyA[b])
                        clean_keyB.append(keyB[b])
                        clean_keyE.append(keyE[b])
                else:
                        discarded_keyA.append(keyA[b])
                        discarded_keyB.append(keyB[b])
        
        # Вывод чистых ключей
        clean_keyA_str = ""
        clean_keyB_str = ""
        for b in range(len(clean_keyA)):
                clean_keyA_str += str(clean_keyA[b])
                clean_keyB_str += str(clean_keyB[b])

        print("Alice key (" + str(len(clean_keyA)) + " bits):")
        print('<' + clean_keyA_str + '>')
        print("Bob key (" + str(len(clean_keyB)) + " bits):")
        print('<' + clean_keyB_str + '>')

        if stat:
                key_statistic_calc(keyA, keyB, clean_keyA)
                if eva:
                        eva_key_statistic(clean_keyA, clean_keyE)

        return
