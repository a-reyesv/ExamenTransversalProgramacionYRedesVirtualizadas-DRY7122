#Tipos de ACL IPV4

print("-----------------------------------------------------------------------")
print("TIPOS DE ACL IPV4\n")

while True:
    print("-----------------------------------------------------------------------")
    acl_input = input("por favor, ingrese un numero de ACL (presione 'q' para salir): ")
    if acl_input.lower() == 'q':
        print("Saliendo del programa...")
        break
    
    try:
        aclnumero = int(acl_input)
        if 1 <= aclnumero <= 99:
            print("Esta es una ACL de tipo Estandar")
        elif 100 <= aclnumero <= 199:
            print("Esta es una ACL de tipo Extendida")
        else:
            print("Esta NO es una ACL de tipo Estandar ni Extendida")
    except ValueError:
        print("Error. Por favor ingrese un número de ACL válido o 'q' para salir")
