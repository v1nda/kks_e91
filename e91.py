import func
import sys, argparse


def do_one_iteration(bA, bB, eva=False, circ=True):

        qA = func.cirq.NamedQubit("Alice")
        qB = func.cirq.NamedQubit("Bob")

        circuit = func.cirq.Circuit()
        circuit.append(func.singlet(qA, qB))

        bases_coincided = func.basis_comparison(bA, bB)
        if not bases_coincided:
                print("Different bases are chosen:")
                print("Value is discarded.")

                return

        circuit.append(func.alice_basis_construction(bA, qA))
        circuit.append(func.bob_basis_construction(bB, qB))

        circuit.append(func.cirq.X(qB))
        circuit.append(func.cirq.measure(qA, qB))

        if circ:
                print(circuit)
        simulator = func.cirq.Simulator()
        result = simulator.run(circuit, repetitions=1)

        print(result)

def key_generation(length, stat=False):

        qA = func.cirq.NamedQubit("Alice")
        qB = func.cirq.NamedQubit("Bob")

        basesA = [func.random() for i in range(length)]
        basesB = [func.random() for i in range(length)]

        keyA = []
        keyB = []
        clean_keyA = []
        clean_keyB = []
        discarded_keyA = []
        discarded_keyB = []
        
        for b in range(length):

                circuit = func.cirq.Circuit()
                circuit.append(func.singlet(qA, qB))

                circuit.append(func.alice_basis_construction(basesA[b], qA))
                circuit.append(func.bob_basis_construction(basesB[b], qB))

                circuit.append(func.cirq.X(qB))
                circuit.append(func.cirq.measure(qA, qB, key='result'))

                simulator = func.cirq.Simulator()
                result = simulator.run(circuit, repetitions=1)

                keyA.append(int(result.measurements['result'][0][0]))
                keyB.append(int(result.measurements['result'][0][1]))


        # Установление индексов совпавших базисов и формирование Алисой и Бобом своих чистых и отброшенных ключей
        for b in range(length):
                
                if func.basis_comparison(basesA[b], basesB[b]):
                        clean_keyA.append(keyA[b])
                        clean_keyB.append(keyB[b])
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
        print(clean_keyA_str)
        print("Bob key (" + str(len(clean_keyB)) + " bits):")
        print(clean_keyB_str)

        if stat:
                func.key_statistic_calc(keyA, keyB, clean_keyA)

        return


def create_parser ():

        parser = argparse.ArgumentParser(
                prog='e91.py',
                description='Реализация квантового протокола распределения ключей E91.',
                epilog='(c) Виноградов Д.А. ККСО-01-18'
        )

        # parser.add_argument('-h', '--help', help='Вывести это сообщение и выйти')
        subparsers = parser.add_subparsers(title='Режимы', description='возможные режимы работы')

        gen_parser = subparsers.add_parser('generate_key', help='режим генерации ключа')
        gen_parser.add_argument('-l', '--length', default=1000, type=int, help='количество передаваемых бит')
        gen_parser.add_argument('-s', '--stat', action='store_true', help='вывод статистики по ключу')
        gen_parser.set_defaults(func=parse_generate_key)

        bit_parser = subparsers.add_parser('one_bit', help='передача одного бита')
        bit_parser.add_argument('-b', '--basis', choices=['pi/4', 'pi/2', 'random'], default='random', help='установка базисов Алисы и Боба')
        bit_parser.add_argument('-c', '--circuit', action='store_true', help='отрисовка схемы')
        bit_parser.add_argument('-e', '--eva', action='store_true', help='передача с участием злоумышленника')
        bit_parser.set_defaults(func=parse_one_bit)

        return parser

def parse_generate_key(args):

        key_generation(args.length, stat=args.stat)

def parse_one_bit(args):

        if args.basis == 'pi/4':
                do_one_iteration(1, 0, eva=args.eva, circ=args.circuit)
        elif args.basis == 'pi/2':
                do_one_iteration(2, 1, eva=args.eva, circ=args.circuit)
        else:
                do_one_iteration(func.random(), func.random(), eva=args.eva, circ=args.circuit)


def main():

        parser = create_parser()
        args = parser.parse_args(sys.argv[1:])

        if not vars(args):
                parser.print_usage()
        else:
                args.func(args)

        return


if __name__ == "__main__":
        
        main()
