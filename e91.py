import func
import sys, argparse


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
        gen_parser.add_argument('-e', '--eva', action='store_true', help='передача с участием злоумышленника')
        gen_parser.set_defaults(func=parse_generate_key)

        bit_parser = subparsers.add_parser('one_bit', help='передача одного бита')
        bit_parser.add_argument('-b', '--basis', choices=['0', 'pi/8', 'random'], default='random', help='установка базисов Алисы и Боба')
        bit_parser.add_argument('-c', '--circuit', action='store_true', help='отрисовка схемы')
        bit_parser.add_argument('-e', '--eva', action='store_true', help='передача с участием злоумышленника')
        bit_parser.set_defaults(func=parse_one_bit)

        return parser

def parse_generate_key(args):

        func.key_generation(args.length, stat=args.stat, eva=args.eva)

        return

def parse_one_bit(args):

        if args.basis == 'pi/8':
                func.do_one_iteration(1, 0, eva=args.eva, circ=args.circuit)
        elif args.basis == '0':
                func.do_one_iteration(2, 1, eva=args.eva, circ=args.circuit)
        else:
                func.do_one_iteration(func.random(), func.random(), eva=args.eva, circ=args.circuit)

        return


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
