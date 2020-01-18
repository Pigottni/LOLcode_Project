def convert_LMAOcode_to_ROFLcode(lmaocode_str):
    """
    For each line of LMAO,
    output the needed ROFL.
    """
    roflcode_lines = ['STORE 10000 0 # Start heap at 10000']
    roflcode_lines.append("VAL_COPY 20000 regH # Start Call Stack at 20000")
    ar_copy_loops = 1
    for lmaocode_line in lmaocode_str.splitlines():
        roflcode_lines.append("")
        roflcode_line = "# Converting -> " + lmaocode_line
        roflcode_lines.append(roflcode_line)
    
        # More work
        parts = lmaocode_line.split()
        roflcode_lines.append("# parts = " + str(parts))

        if not parts:
            continue
        
        elif parts[0] == 'VAL_COPY':
            if parts[1][0] == 's':
                value = parts[1]
                value_mem = value[1:]
                dest = parts[2]
                dest_mem = dest[1:]
                roflcode_lines.append(f"LOAD {value_mem} regA")
            
            else:
                if (parts[1] == "'") and (parts[2] == "'"):
                    value = "' '"
                    dest = parts[3]
                else:
                    value = parts[1]
                    dest = parts[2]
                dest_mem = dest[1:]
                roflcode_lines.append(f"VAL_COPY {value} regA")
                
            roflcode_lines.append("VAL_COPY regA regB")
            roflcode_lines.append(f"STORE regB {dest_mem}")
            
        elif parts[0] == 'OUT_NUM':
            source = parts[1]
            source_memory = source[1:]
            roflcode_lines.append(f"LOAD {source_memory} regA ")
            roflcode_lines.append("OUT_NUM regA")
            
        elif parts[0] == 'OUT_CHAR':
            source = parts[1]
            if source == "'\\n'":
                roflcode_lines.append(f"VAL_COPY {source} regA ")
            else:
                source_memory = source[1:]
                roflcode_lines.append(f"LOAD {source_memory} regA ")
            roflcode_lines.append("OUT_CHAR regA")
            
        elif parts[0] == 'RANDOM':
            dest = parts[1]
            dest_mem = dest[1:]
            roflcode_lines.append("RANDOM regA")
            roflcode_lines.append(f"STORE regA {dest_mem}")
            
        elif parts[0] == 'IN_CHAR':
            dest = parts[1]
            dest_mem = dest[1:]
            roflcode_lines.append("IN_CHAR regA")
            roflcode_lines.append(f"STORE regA {dest_mem}")
            
        elif parts[0] in ['ADD', 'SUB', 'MULT', 'DIV',
                            'TEST_NEQU', 'TEST_EQU', 'TEST_LESS', 'TEST_GTR', 'TEST_GTE']:
            if parts[1][0] == 's':
                math_one = parts[1]
                math_one_mem = math_one[1:]
                roflcode_lines.append(f"LOAD {math_one_mem} regA")
            else:
                roflcode_lines.append(f"VAL_COPY {parts[1]} regA")
            if parts[2][0] == 's':
                math_two = parts[2]
                math_two_mem = math_two[1:]
                roflcode_lines.append(f"LOAD {math_two_mem} regB")
            else:
                roflcode_lines.append(f"VAL_COPY {parts[2]} regB")
            dest = parts[3]
            dest_mem = dest[1:]
            roflcode_lines.append(f"{parts[0]} regA regB regC")
            roflcode_lines.append(f"STORE regC {dest_mem}")
            
        elif parts[0] == "AR_SET_SIZE":
            array = parts[1]
            ar_mem = array[1:]
            size = parts[2]
            size_mem = size[1:]
            
            if size[0] == 's':
                roflcode_lines.append(f"LOAD {size_mem} regA")
            else:
                roflcode_lines.append(f"VAL_COPY {size} regA")
                
            roflcode_lines.append("LOAD 0 regB")
            roflcode_lines.append(f"STORE regB {ar_mem}")
            roflcode_lines.append("STORE regA regB")
            roflcode_lines.append("ADD regA regB regC")
            roflcode_lines.append("ADD 1 regC regC")
            roflcode_lines.append("STORE regC 0")
            
        elif parts[0] == "AR_GET_SIZE":
            array = parts[1]
            ar_mem = array[1:]
            dest = parts[2]
            dest_mem = dest[1:]
            roflcode_lines.append(f"LOAD {ar_mem} regA")
            roflcode_lines.append("LOAD regA regB")
            roflcode_lines.append(f"STORE regB {dest_mem}")
            
        elif parts[0] == 'AR_GET_IDX':
            ar_source = parts[1]
            ar_source_mem = ar_source[1:]
            index = parts[2]
            index_mem = index[1:]
            dest = parts[3]
            dest_mem = dest[1:]
            roflcode_lines.append(f"LOAD {ar_source_mem} regA")
            
            if index[0] == 's':
                roflcode_lines.append(f"LOAD {index_mem} regB")
            else:
                roflcode_lines.append(f"VAL_COPY {index} regB")
                
            roflcode_lines.append("ADD regA 1 regD")
            roflcode_lines.append("ADD regD regB regD")
            roflcode_lines.append("LOAD regD regC")
            roflcode_lines.append(f"STORE regC {dest_mem}")
            
        elif parts[0] == 'AR_SET_IDX':
            ar_source = parts[1]
            ar_source_mem = ar_source[1:]
            index = parts[2]
            index_mem = index[1:]
            value = parts[3]
            value_mem = value[1:]
            roflcode_lines.append(f"LOAD {ar_source_mem} regA")
            
            if index[0] == 's':
                roflcode_lines.append(f"LOAD {index_mem} regB")
            else:
                roflcode_lines.append(f"VAL_COPY {index} regB")
                
            if value[0] == 's':
                roflcode_lines.append(f"LOAD {value_mem} regC")
            else:
                if parts[3] == "'":
                    roflcode_lines.append("VAL_COPY ' ' regC")
                else:
                    roflcode_lines.append(f"VAL_COPY {value} regC")
            
            roflcode_lines.append("ADD regA 1 regD")
            roflcode_lines.append("ADD regD regB regD")
            roflcode_lines.append("STORE regC regD")
            
        elif parts[0] == 'AR_COPY':
            ar_source = parts[1]
            ar_source_mem = ar_source[1:]
            ar_dest = parts[2]
            ar_dest_mem = ar_dest[1:]
            
            # Set array size
            roflcode_lines.append(f"LOAD {ar_source_mem} regA")
            roflcode_lines.append("LOAD regA regB")
            roflcode_lines.append("LOAD 0 regC")
            roflcode_lines.append("LOAD 0 regE")
            roflcode_lines.append(f"STORE regC {ar_dest_mem}")
            roflcode_lines.append("STORE regB regC")
            roflcode_lines.append("ADD regB regC regD")
            roflcode_lines.append("ADD 1 regD regD") # next free mem slot
            roflcode_lines.append("STORE regD 0")
            
            # Copy over each element
            roflcode_lines.append(f"ar_copy_start_{ar_copy_loops}:")
            roflcode_lines.append("ADD 1 regA regA") # source index
            roflcode_lines.append("ADD 1 regE regE") # destination index
            roflcode_lines.append(f"TEST_EQU regE regD regF")
            roflcode_lines.append(f"VAL_COPY ar_copy_end_{ar_copy_loops+1} regG")
            roflcode_lines.append("JUMP_IF_N0 regF regG")
            roflcode_lines.append("MEM_COPY regA regE")
            roflcode_lines.append(f"JUMP ar_copy_start_{ar_copy_loops}")
            roflcode_lines.append(f"ar_copy_end_{ar_copy_loops+1}:")
            ar_copy_loops += 2
            
            
        elif parts[0] in ['JUMP_IF_0', 'JUMP_IF_N0']:
            dest = parts[1]
            dest_mem = dest[1:]
            roflcode_lines.append(f"LOAD {dest_mem} regA")
            roflcode_lines.append(f"VAL_COPY {parts[2]} regB")
            roflcode_lines.append(f"{parts[0]} regA regB")
            
        elif parts[0] == 'JUMP':
            if parts[1][0] == 's':
                roflcode_lines.append(f"LOAD {parts[1][1:]} regA")
            else:
                roflcode_lines.append(f"VAL_COPY {parts[1]} regA")
            roflcode_lines.append("JUMP regA")
            
        elif parts[0][-1] == ":":
            roflcode_lines.append(parts[0])
            
        elif "loop_start" in parts[0]:
            roflcode_lines.append(parts[0])
            
        elif parts[0] == 'POP':
            dest = parts[1]
            dest_mem = dest[1:]
            roflcode_lines.append("SUB regH 1 regH")
            roflcode_lines.append("LOAD regH regA")
            roflcode_lines.append(f"STORE regA {dest_mem}")
            
        elif parts[0] == 'PUSH':
            dest = parts[1]
            dest_mem = dest[1:]
            if "function_call" in parts[1]:
                roflcode_lines.append(f"VAL_COPY {dest} regA")
            else:
                roflcode_lines.append(f"LOAD {dest_mem} regA")
            roflcode_lines.append("STORE regA regH")
            roflcode_lines.append("ADD 1 regH regH")

    return "\n".join(roflcode_lines) + '\n'


if __name__ == "__main__":
    lmaocode_str = """
    VAL_COPY 5 s8
    OUT_NUM s8 
    """
    print(convert_LMAOcode_to_ROFLcode(lmaocode_str))
    
    
    