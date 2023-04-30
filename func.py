import cirq
import math


INDENT = "  |\t"
WIDTH = 50
PREFIX = "-->"


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
        # Если базис 2 (basis == 2), то только измерение.
        
        return moments

def bob_basis_construction(basis, q):

        moments = []

        if basis == 0:
                moments.append(cirq.rz(math.pi/2).on(q))
                moments.append(cirq.H(q))
                moments.append(cirq.rz(math.pi/4).on(q))
                moments.append(cirq.H(q))
        # Если базис 1 (basis == 1), то только измерение.
        elif basis == 2:
                moments.append(cirq.rz(rads=math.pi/2).on(q))
                moments.append(cirq.H(q))
                moments.append(cirq.rz(rads=(0-math.pi)/4).on(q))
                moments.append(cirq.H(q))
        
        return moments

def eve_basis_construction(basis, q):

        moments = []

        # Если базис 0 (basis == 0), то только измерение.
        if basis == 1:
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


def key_statistic_calc(keyA, keyB, clean_key, discarded_keyA, discarded_keyB):
        
        p0_keyA = 0
        p0_keyB = 0
        p0_clean_key = 0

        p_coinc = 0
        p_discarded_coinc = 0

        for b in range(len(keyA)):
                
                if keyA[b] == 0:
                        p0_keyA += 1
                if keyB[b] == 0:
                        p0_keyB += 1
                if keyA[b] == keyB[b]:
                        p_coinc += 1
                
                if b < len(clean_key) and clean_key[b] == 0:
                        p0_clean_key += 1
                if b < len(discarded_keyA) and discarded_keyA[b] == discarded_keyB[b]:
                        p_discarded_coinc += 1

        p0_keyA = round(p0_keyA / len(keyA) * 100, 4)
        p0_keyB = round(p0_keyB / len(keyB) * 100, 4)
        p0_clean_key = round(p0_clean_key / len(clean_key) * 100, 4)
        p_coinc = round(p_coinc / len(keyA) * 100, 4)
        p_discarded_coinc = round(p_discarded_coinc / len(discarded_keyA) * 100, 4)

        print(INDENT, 'Статистика по полному ключу Алисы:')
        print(INDENT, '\tдлина ключа: \t\t\t' + str(len(keyA)))
        print(INDENT, '\tвероятность появления 0: \t' + str(p0_keyA) + '%', '(теор. 50%)')
        
        print(INDENT)
        print(INDENT, 'Статистика по полному ключу Боба:')
        print(INDENT, '\tдлина ключа: \t\t\t' + str(len(keyB)))
        print(INDENT, '\tвероятность появления 0: \t' + str(p0_keyB) + '%', '(теор. 50%)')
        
        print(INDENT)
        print(INDENT, 'Статистика по чистому ключу:')
        print(INDENT, '\tдлина ключа: \t\t\t' + str(len(clean_key)))
        print(INDENT, '\tвероятность появления 0: \t' + str(p0_clean_key) + '%', '(теор. 50%)')

        print(INDENT)
        print(INDENT, 'Вероятность совпадения значений')
        print(INDENT, 'полного ключа Алисы и Боба:\t\t' + str(p_coinc) + '%', '(теор. 72.89% без Евы)')

        print(INDENT)
        print(INDENT, 'Вероятность совпадения значений')
        print(INDENT, 'отброшенного ключа Алисы и Боба:\t' + str(p_discarded_coinc) + '%', '(теор. 65.14%)')

        return

def eva_key_statistic(keyA, keyE, clean_keyA, clean_keyB, clean_keyE):

        p = 0
        p_clean = 0
        difference = 0

        for b in range(len(keyA)):
                
                if keyA[b] == keyE[b]:
                        p += 1

                if b < len(clean_keyA):

                        if clean_keyA[b] == clean_keyE[b]:
                                p_clean += 1
                        if clean_keyA[b] != clean_keyB[b]:
                                difference += 1
                
        p = round((p / len(keyA)) * 100, 4)
        p_clean = round((p_clean / len(clean_keyA)) * 100, 4)

        print(INDENT)
        print(INDENT + ''.center(WIDTH, '-'))
        print(INDENT)
        print(INDENT, 'Процент угадываний Евой:')
        print(INDENT, '\tв полном ключе: \t', p, '%', '(теор. 84.34%)')
        print(INDENT, '\tв чистом ключе: \t', p_clean, '%', '(теор. 92.67%)')
        print(INDENT)
        print(INDENT, 'Количество ошибок в ключе Боба:')
        print(INDENT, '\t\t\t\t', difference)

        return



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

        if eva:
                circuit.append(eve_basis_construction(random(mod=2), qB))
                circuit.append(cirq.measure(qB, key='Eva'))

        circuit.append(bob_basis_construction(bB, qB))

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
        
        return

def key_generation(length, eva=False, stat=False):

        print(PREFIX, 'Генерация последовательности базисов Алисы')
        basesA = [random() for i in range(length)]
        print(PREFIX, 'Генерация последовательности базисов Боба')
        basesB = [random() for i in range(length)]
        
        keyA = []
        keyB = []
        clean_keyA = []
        clean_keyB = []
        discarded_keyA = []
        discarded_keyB = []

        if eva:
                print(PREFIX, 'Генерация последовательности базисов Евы')
                basesE = [random(mod=2) for i in range(length)]
                keyE = []
                clean_keyE = []

        print(PREFIX, 'Передача')
        for b in range(length):

                qA = cirq.NamedQubit("Alice")
                qB = cirq.NamedQubit("Bob")

                circuit = cirq.Circuit()
                circuit.append(singlet(qA, qB))

                circuit.append(alice_basis_construction(basesA[b], qA))

                if eva:
                        circuit.append(eve_basis_construction(basesE[b], qB))
                        circuit.append(cirq.measure(qB, key='Eva'))

                circuit.append(bob_basis_construction(basesB[b], qB))

                circuit.append(cirq.X(qB))
                circuit.append(cirq.measure(qA, qB, key='result'))

                simulator = cirq.Simulator()
                result = simulator.run(circuit, repetitions=1)

                keyA.append(int(result.measurements['result'][0][0]))
                keyB.append(int(result.measurements['result'][0][1]))

                if eva:
                        keyE.append((int(result.measurements['Eva'][0][0]) + 1) % 2)


        # Установление индексов совпавших базисов и формирование Алисой и Бобом своих чистых и отброшенных ключей
        print(PREFIX, 'Проверка совпадения базисов, формирование чистых ключей\n')
        for b in range(length):
                
                if basis_comparison(basesA[b], basesB[b]):
                        clean_keyA.append(keyA[b])
                        clean_keyB.append(keyB[b])
                        if eva:
                                clean_keyE.append(keyE[b])
                else:
                        discarded_keyA.append(keyA[b])
                        discarded_keyB.append(keyB[b])


        # Вывод чистых ключей
        strA_s = " ALICE KEY (" + str(len(clean_keyA)) + " bits) "
        strA_e = " END OF ALICE KEY "
        strB_s = " BOB KEY (" + str(len(clean_keyB)) + " bits) "
        strB_e = " END OF BOB KEY "

        clean_keyA_str = INDENT
        clean_keyB_str = INDENT
        for b in range(len(clean_keyA)):
                clean_keyA_str += str(clean_keyA[b])
                clean_keyB_str += str(clean_keyB[b])
                
                if (b + 1) % WIDTH == 0 and (b + 1) != len(clean_keyA):
                        clean_keyA_str += "\n" + INDENT
                        clean_keyB_str += "\n" + INDENT
                
        print(INDENT + strA_s.center(WIDTH, '-'), clean_keyA_str, INDENT + strA_e.center(WIDTH, '-'), INDENT, sep='\n')
        print(INDENT + strB_s.center(WIDTH, '-'), clean_keyB_str, INDENT + strB_e.center(WIDTH, '-'), sep='\n')


        # Рассчет статистики
        if stat:
                print('\n' + PREFIX, 'Расчет статистики\n')
                key_statistic_calc(keyA, keyB, clean_keyA, discarded_keyA, discarded_keyB)
                if eva:
                        eva_key_statistic(keyA, keyE, clean_keyA, clean_keyB, clean_keyE)
        
        return
