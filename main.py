import numpy as np
import cirq


def random():

        res = 5

        qubit_1 = cirq.NamedQubit("1")
        qubit_2 = cirq.NamedQubit("2")
        
        while res >= 4:

                moment = cirq.Moment([cirq.H(qubit_1), cirq.H(qubit_2)])
                circuit = cirq.Circuit((moment))
                circuit.append(cirq.measure(qubit_1, qubit_2, key='result'))
                result = cirq.Simulator().run(circuit)

                a = result.measurements['result'][0][0]
                b = result.measurements['result'][0][1]

                if a == 0 and b == 0:
                        res = 0
                elif a == 0 and b == 1:
                        res = 1
                elif a == 1 and b == 0:
                        res = 2
                elif a == 1 and b == 1:
                        res = 4
                else:
                        res = 5

        return res


def basis_A0(qubit):

        moment = cirq.Moment([cirq.H(qubit)])

        return [moment]

def basis_A1(qubit):

        moment1 = cirq.Moment([cirq.rz(rads=np.pi/2).on(qubit)])
        moment2 = cirq.Moment([cirq.H(qubit)])
        moment3 = cirq.Moment([cirq.rz(rads=np.pi/4).on(qubit)])
        moment4 = cirq.Moment([cirq.H(qubit)])

        return [moment1, moment2, moment3, moment4]

def basis_B0(qubit):

        moment1 = cirq.Moment([cirq.rz(rads=np.pi/2).on(qubit)])
        moment2 = cirq.Moment([cirq.H(qubit)])
        moment3 = cirq.Moment([cirq.rz(rads=np.pi/4).on(qubit)])
        moment4 = cirq.Moment([cirq.H(qubit)])

        return [moment1, moment2, moment3, moment4]

def basis_B2(qubit):

        moment1 = cirq.Moment([cirq.rz(rads=np.pi/2).on(qubit)])
        moment2 = cirq.Moment([cirq.H(qubit)])
        moment3 = cirq.Moment([cirq.rz(rads=(0-np.pi)/4).on(qubit)])
        moment4 = cirq.Moment([cirq.H(qubit)])

        return [moment1, moment2, moment3, moment4]

def basis_compare(basis_A, basis_B):

        res = False

        if basis_A == 1 and basis_B == 0 or basis_A == 2 and basis_B == 1:
                res = True
        else:
                res = False

        return res

def basis_A_circuit(basis, qubit):

        if basis == 0:
                return basis_A0(qubit)
        elif basis == 1:
                return basis_A1(qubit)
        else:
                return []

def basis_B_circuit(basis, qubit):

        if basis == 0:
                return basis_B0(qubit)
        elif basis == 2:
                return basis_B2(qubit)
        else:
                return []

def singlet(qubit_A, qubit_B):

        moment1 = cirq.Moment([cirq.X(qubit_A), cirq.X(qubit_B)])
        moment2 = cirq.Moment([cirq.H(qubit_A)])
        moment3 = cirq.Moment([cirq.CNOT(qubit_A, qubit_B)])

        return [moment1, moment2, moment3]


def transmission():

        qubit_A = cirq.NamedQubit("Alice")
        qubit_B = cirq.NamedQubit("Bob")
        circuit = cirq.Circuit()

        circuit.append(singlet(qubit_A, qubit_B))

        basis_A = random()
        basis_B = random()

        bases_eq = basis_compare(basis_A, basis_B)

        if not bases_eq:
                print("Different bases are chosen:")
                print("\tValue is discarded.")
                
                return
        
        circuit.append(basis_A_circuit(basis_A, qubit_A))
        circuit.append(basis_B_circuit(basis_B, qubit_B))

        circuit.append(cirq.X(qubit_B))

        circuit.append(cirq.measure(qubit_A, qubit_B, key='result'))

        print(circuit)

        result = cirq.Simulator().simulate(circuit)

        A = int(result.measurements['result'][0])
        B = int(result.measurements['result'][1])

        print("(", A, ",", B, ")")

        return



def key_generator(length):

        A_bases = []
        B_bases = []

        A_key = []
        B_key = []

        for j in range(length):

                A_bases.append(random())
                B_bases.append(random())

        for i in range(length):

                bases_eq = basis_compare(A_bases[i], B_bases[i])

                if not bases_eq:
                        continue


                qubit_A = cirq.NamedQubit("Alice")
                qubit_B = cirq.NamedQubit("Bob")
                circuit = cirq.Circuit()

                circuit.append(singlet(qubit_A, qubit_B))
                
                circuit.append(basis_A_circuit(A_bases[i], qubit_A))
                circuit.append(basis_B_circuit(B_bases[i], qubit_B))

                circuit.append(cirq.X(qubit_B))

                circuit.append(cirq.measure(qubit_A, qubit_B, key='result'))

                result = cirq.Simulator().run(circuit)

                A_key.append(int(result.measurements['result'][0][0]))
                B_key.append(int(result.measurements['result'][0][1]))


        print("Alice key:")
        for bit in A_key:
                print(bit, end='')
        print("\n")

        print("Bob key:")
        for bit in B_key:
                print(bit, end='')
        print()
        
        return

# key_generator(10000)
transmission()
