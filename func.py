import cirq
import math
import time


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


# Функции вывода

def __prefix():

       return '[' + time.strftime('%H:%M:%S') + '] ' + PREFIX

def __print_key(name, key):

        str_s = ' ' + name + ' KEY (' + str(len(key)) + ' bits) '
        str_e = ' END OF ' + name + ' KEY '

        key_str = INDENT
        for b in range(len(key)):
                key_str += str(key[b])
                
                if (b + 1) % WIDTH == 0 and (b + 1) != len(key):
                        key_str += "\n" + INDENT

        print()        
        print(INDENT + str_s.center(WIDTH, '-'), key_str, INDENT + str_e.center(WIDTH, '-'), sep='\n')
        print()

        return


# Функции формирования элементов квантовой схемы

def __singlet(q0, q1):
        
        m1 = cirq.Moment([cirq.X(q0), cirq.X(q1)])
        m2 = cirq.H(q0)
        m3 = cirq.CNOT(q0, q1)

        return [m1, m2, m3]

def __alice_basis_construction(basis, q):

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

def __bob_basis_construction(basis, q):

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

def __eve_basis_construction(basis, q):

        moments = []

        # Если базис 0 (basis == 0), то только измерение.
        if basis == 1:
                moments.append(cirq.rz(math.pi/2).on(q))
                moments.append(cirq.H(q))
                moments.append(cirq.rz(math.pi/4).on(q))
                moments.append(cirq.H(q))

        return moments

def __basis_comparison(b0, b1):

        if (b0 == 1 and b1 == 0) or (b0 == 2 and b1 == 1):
                return True
        else:
                return False


# Функции рассчета статистики клочей

def __key_statistic_calc(keyA, keyB, clean_key, discarded_keyA, discarded_keyB):
        
        print()

        if len(keyA) == 0 or len(clean_key) == 0 or len(discarded_keyA) == 0:
                print(INDENT, 'Ошибка: не удалось рассчитать статистику --')
                print(INDENT, '\tслишком мало значений')
                print()

                return 0

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
        print(INDENT, 'Вероятность совпадения значений бит')
        print(INDENT, 'полного ключа Алисы и Боба:\t\t' + str(p_coinc) + '%', '(теор. 72.89% без Евы)')

        print(INDENT)
        print(INDENT, 'Вероятность совпадения значений бит')
        print(INDENT, 'отброшенного ключа Алисы и Боба:\t' + str(p_discarded_coinc) + '%', '(теор. 65.14%)')

        print()

        return 1

def __eva_key_statistic(keyA, keyE, clean_keyA, clean_keyB, clean_keyE):

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

        print(INDENT, 'Процент угадываний значений бит Евой:')
        print(INDENT, '\tв полном ключе:\t\t\t', p, '%', '(теор. 84.34%)')
        print(INDENT, '\tв чистом ключе:\t\t\t', p_clean, '%', '(теор. 92.67%)')
        print(INDENT)
        print(INDENT, 'Количество ошибок в ключе Боба:\t', difference)
        print()

        return

# Функция обнаружения криптоаналитика 

def __eva_detection(basesA, basesB, discarded_bases, discarded_keyA, discarded_keyB):

        print()

        num_of_values_A0B0 = [0, 0, 0, 0]
        num_of_values_A0B2 = [0, 0, 0, 0]
        num_of_values_A2B0 = [0, 0, 0, 0]
        num_of_values_A2B2 = [0, 0, 0, 0]

        for b in range(len(discarded_bases)):

                if basesA[discarded_bases[b]] == 0 and basesB[discarded_bases[b]] == 0:
                        num_of_values_A0B0[int(str(discarded_keyA[b]) + str(discarded_keyB[b]), 2)] += 1
                
                elif basesA[discarded_bases[b]] == 0 and basesB[discarded_bases[b]] == 2:
                        num_of_values_A0B2[int(str(discarded_keyA[b]) + str(discarded_keyB[b]), 2)] += 1
                
                elif basesA[discarded_bases[b]] == 2 and basesB[discarded_bases[b]] == 0:
                        num_of_values_A2B0[int(str(discarded_keyA[b]) + str(discarded_keyB[b]), 2)] += 1

                elif basesA[discarded_bases[b]] == 2 and basesB[discarded_bases[b]] == 2:
                        num_of_values_A2B2[int(str(discarded_keyA[b]) + str(discarded_keyB[b]), 2)] += 1

        if sum(num_of_values_A0B0) == 0 or sum(num_of_values_A0B2) == 0 or sum(num_of_values_A2B0) == 0 or sum(num_of_values_A2B2) == 0:
                print(INDENT, 'Ошибка: не удалось рассчитать значение CHSH --')
                print(INDENT, '\tотброшенный ключ слишком мал.')
                print()

                return

        expect_A1B1 = (num_of_values_A0B0[0] - num_of_values_A0B0[1] - num_of_values_A0B0[2] + num_of_values_A0B0[3]) / sum(num_of_values_A0B0)
        expect_A1B3 = (num_of_values_A0B2[0] - num_of_values_A0B2[1] - num_of_values_A0B2[2] + num_of_values_A0B2[3]) / sum(num_of_values_A0B2)
        expect_A3B1 = (num_of_values_A2B0[0] - num_of_values_A2B0[1] - num_of_values_A2B0[2] + num_of_values_A2B0[3]) / sum(num_of_values_A2B0)
        expect_A3B3 = (num_of_values_A2B2[0] - num_of_values_A2B2[1] - num_of_values_A2B2[2] + num_of_values_A2B2[3]) / sum(num_of_values_A2B2)

        result = round(abs(expect_A1B1 - expect_A1B3 + expect_A3B1 + expect_A3B3), 4)

        print(INDENT, 'Корреляционное значение CHSH:' + '\t\t', result)

        if result <= 2:
                print(INDENT, 'Неравенство Белла выполняется:' + '\t\t', str(result) + ' <= 2')
                print(INDENT)
                print(INDENT, 'Наличие криптоаналитика (Евы):' + '\t\t', 'обнаружено.')

        else:
                print(INDENT, 'Неравенство Белла не выполняется:' + '\t', str(result) + ' > 2')
                print(INDENT)
                print(INDENT, 'Наличие криптоаналитика (Евы):' + '\t\t', 'не обнаружено.')

        print()

        return


# Функция передачи одного бита

def do_one_iteration(bA, bB, eva=False, circ=True):

        # Инициализация кубитов, формирование схемы

        qA = cirq.NamedQubit('Алиса')
        qB = cirq.NamedQubit('Боб')

        print(__prefix(), 'Формирование квантовой схемы.')
        circuit = cirq.Circuit()
        circuit.append(__singlet(qA, qB))


        # Передача бита

        print(__prefix(), 'Передача.')
        circuit.append(__alice_basis_construction(bA, qA))

        if eva:
                circuit.append(__eve_basis_construction(random(mod=2), qB))
                circuit.append(cirq.measure(qB, key='Ева'))

        circuit.append(__bob_basis_construction(bB, qB))

        circuit.append(cirq.X(qB))
        circuit.append(cirq.measure(qA, qB, key='result'))

        if circ:
                print()
                print(circuit)
                print()

        simulator = cirq.Simulator()
        result = simulator.run(circuit, repetitions=1)

        
        # Вывод результата передачи
        
        print(__prefix(), 'Результат передачи:')
        print()
        print(INDENT, 'бит Алисы:\t', int(result.measurements['result'][0][0]))
        print(INDENT, 'бит Боба:\t', int(result.measurements['result'][0][1]))
        
        if eva:
                print(INDENT, 'бит Евы:\t', (int(result.measurements['Ева'][0][0]) + 1) % 2)

        print()
        

        #  Сравнение базисов

        bases_coincided = __basis_comparison(bA, bB)

        if not bases_coincided:
                print(__prefix(), 'Сравнение базисов Алисы и Боба: бит отброшен.')
        else:
                print(__prefix(), 'Сравнение базисов Алисы и Боба.')

        print(__prefix(), 'Завершено.\n')

        return

# Функция распределения ключа

def key_generation(length, eva=False, stat=False):

        # Генерация последовательностей базисов
        
        print(__prefix(), 'Генерация последовательности базисов Алисы.')
        basesA = [random() for i in range(length)]
        print(__prefix(), 'Генерация последовательности базисов Боба.')
        basesB = [random() for i in range(length)]
        discarded_bases = []

        keyA = []
        keyB = []
        clean_keyA = []
        clean_keyB = []
        discarded_keyA = []
        discarded_keyB = []

        if eva:
                print(__prefix(), 'Генерация последовательности базисов Евы.')
                basesE = [random(mod=2) for i in range(length)]
                keyE = []
                clean_keyE = []


        # Формирование квантовых схем и передача битов
        
        print(__prefix(), 'Передача.')
        for b in range(length):

                qA = cirq.NamedQubit('Alice')
                qB = cirq.NamedQubit('Bob')

                circuit = cirq.Circuit()
                circuit.append(__singlet(qA, qB))

                circuit.append(__alice_basis_construction(basesA[b], qA))

                if eva:
                        circuit.append(__eve_basis_construction(basesE[b], qB))
                        circuit.append(cirq.measure(qB, key='Eva'))

                circuit.append(__bob_basis_construction(basesB[b], qB))

                circuit.append(cirq.X(qB))
                circuit.append(cirq.measure(qA, qB, key='result'))

                simulator = cirq.Simulator()
                result = simulator.run(circuit, repetitions=1)

                keyA.append(int(result.measurements['result'][0][0]))
                keyB.append(int(result.measurements['result'][0][1]))

                if eva:
                        keyE.append((int(result.measurements['Eva'][0][0]) + 1) % 2)


        # Установление индексов совпавших базисов и формирование Алисой и Бобом чистых и отброшенных ключей
        
        print(__prefix(), 'Проверка совпадения базисов, формирование чистых ключей.')
        for b in range(length):
                
                if __basis_comparison(basesA[b], basesB[b]):
                        clean_keyA.append(keyA[b])
                        clean_keyB.append(keyB[b])
                        if eva:
                                clean_keyE.append(keyE[b])
                else:
                        discarded_bases.append(b)
                        discarded_keyA.append(keyA[b])
                        discarded_keyB.append(keyB[b])


        # Вывод чистых ключей
        
        __print_key('ALICE', clean_keyA)
        __print_key('BOB', clean_keyB)

        if eva:
                __print_key('EVA', clean_keyE)
        

        # Рассчет статистики
        
        if stat:
                print(__prefix(), 'Расчет статистики.')
                __key_statistic_calc(keyA, keyB, clean_keyA, discarded_keyA, discarded_keyB)

                if eva:
                        __eva_key_statistic(keyA, keyE, clean_keyA, clean_keyB, clean_keyE)
        

        # Обнаружение Евы
        
        print(__prefix(), 'Обнаружение криптоаналитика.')
        __eva_detection(basesA, basesB, discarded_bases, discarded_keyA, discarded_keyB)

        print(__prefix(), 'Завершено.\n')

        return
