def lfsr(register, taps):
  
    xor_result = int(register[taps[0]]) ^ int(register[taps[1]])

    register = str(xor_result) + register[:-1]

    return register, register[-1]

def add_modulo(popped_bits1, popped_bits2, modulo=256):
    
    result = (int(popped_bits1, 2) + int(popped_bits2, 2)) % modulo

    return bin(result)[2:].zfill(8)

def perform_operations(register1, register2, taps1, taps2,  iterations, input_byte):

    popped_bits1 = ""
    popped_bits2 = ""
    for ji in range(iterations):
        for _ in range(8):
            register1, popped_bit1 = lfsr(register1, taps1)
            popped_bits1 += popped_bit1

            register2, popped_bit2 = lfsr(register2, taps2)
            popped_bits2 += popped_bit2

        added_result = add_modulo(popped_bits1, popped_bits2)

        xored_result = bin(int(added_result, 2) ^ int(input_byte, 2) )[2:].zfill(8)

    return xored_result

def main():
   
    register1 = "101010100001"
    register2 = "1110101000011001110"
    register1o = "101010100001"
    register2o = "1110101000011001110" 
    taps1 = [2, 7]
    taps2 = [5, 11]
    key = "01100000"

    iteration_counter = 0
    while True:
        popped_bits1 = ""
        popped_bits2 = ""

        for _ in range(8):
            register1, popped_bit1 = lfsr(register1, taps1)
            popped_bits1 += popped_bit1

            register2, popped_bit2 = lfsr(register2, taps2)
            popped_bits2 += popped_bit2

        added_result = add_modulo(popped_bits1, popped_bits2)
        xored_result = bin(int(added_result, 2) ^ int(key, 2))[2:].zfill(8)

        iteration_counter += 1
        if xored_result == "10001001":
            break

    print(f"Number of iterations: {iteration_counter}")

    input_filename = "flag.enc"
    output_filename = "Decryptflag.png"

    with open(input_filename, "rb") as input_file, open(output_filename, "wb") as output_file:
        while True:
            input_byte = input_file.read(1)
            if not input_byte:
                break

      
            input_byte_bin = bin(int.from_bytes(input_byte, byteorder='big'))[2:].zfill(8)
            print(f"Input(Binary): {input_byte_bin}")


            result_byte = perform_operations(register1o, register2o, taps1, taps2,  iteration_counter, input_byte_bin)

            result_byte_bin = bin(int(result_byte, 2))[2:].zfill(8)
            print(f"Output(Binary): {result_byte_bin}")
            output_file.write(bytes([int(result_byte, 2)]))


if __name__ == "__main__":
    main()