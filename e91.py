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


def do_one_iteration(bA, bB):

        qA = cirq.NamedQubit("Alice")
        qB = cirq.NamedQubit("Bob")

        circuit = cirq.Circuit()
        circuit.append(singlet(qA, qB))

        bases_coincided = basis_comparison(bA, bB)
        if not bases_coincided:
                print("Different bases are chosen:")
                print("Value is discarded.")

                return

        circuit.append(alice_basis_construction(bA, qA))
        circuit.append(bob_basis_construction(bB, qB))

        circuit.append(cirq.X(qB))
        circuit.append(cirq.measure(qA, qB))

        print(circuit)
        simulator = cirq.Simulator()
        result = simulator.run(circuit, repetitions=1)

        print(result)

def key_generation(length):

        qA = cirq.NamedQubit("Alice")
        qB = cirq.NamedQubit("Bob")

        basesA = [random() for i in range(length)]
        basesB = [random() for i in range(length)]

        keyA = []
        keyB = []
        clean_keyA = []
        clean_keyB = []
        discarded_keyA = []
        discarded_keyB = []
        
        for b in range(length):

                circuit = cirq.Circuit()
                circuit.append(singlet(qA, qB))

                circuit.append(alice_basis_construction(basesA[b], qA))
                circuit.append(bob_basis_construction(basesB[b], qB))

                circuit.append(cirq.X(qB))
                circuit.append(cirq.measure(qA, qB, key='result'))

                simulator = cirq.Simulator()
                result = simulator.run(circuit, repetitions=1)

                keyA.append(int(result.measurements['result'][0][0]))
                keyB.append(int(result.measurements['result'][0][1]))


        # Установление индексов совпавших базисов и формирование Алисой и Бобом своих чистых и отброшенных ключей
        for b in range(length):
                
                if basis_comparison(basesA[b], basesB[b]):
                        clean_keyA.append(keyA[b])
                        clean_keyB.append(keyB[b])
                else:
                        discarded_keyA.append(keyA[b])
                        discarded_keyB.append(keyB[b])
        
        # Вывод чистых ключей
        print("Alice key (" + str(len(clean_keyA)) + " bits):")
        print(clean_keyA)
        print("Bob key (" + str(len(clean_keyB)) + " bits):")
        print(clean_keyB)

        return


def main():

        # do_one_iteration(random(), random())
        # do_one_iteration(1, 0)
        # do_one_iteration(2, 1)

        key_generation(100)

        return


if __name__ == "__main__":
        
        main()
