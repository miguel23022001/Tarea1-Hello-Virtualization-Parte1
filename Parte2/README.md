# Live Migration con Libvirt

## Requisitos
- **Libvirt**: Para gestionar las VMs.
- **psutil**: Librería de Python para monitorear el uso de CPU.
- **stress-ng**: Herramienta para generar carga en la VM.
- **Conexión SSH**: Necesaria entre el host de origen y el host de destino para la migración en vivo.

## Archivos Incluidos
- `script.py`: Script en Python que incluye varias funciones para gestionar las VMs y realizar la migración en vivo.
- `create_vm.sh`: Script en Bash para crear una nueva VM con configuración de red y disco.
- `README.md`: Documentación del proyecto.

## Instalación y Configuración
1. **Instala libvirt**:
   ```bash
   sudo apt-get install libvirt-bin
   ```

2. **Instala psutil para Python**:
   ```bash
   pip install psutil
   ```

3. **Instala stress-ng** para generar carga de CPU:
   ```bash
   sudo apt-get install stress-ng
   ```

4. **Configura SSH sin contraseña** entre el host de origen y el destino:
   ```bash
   ssh-keygen -t rsa -b 2048
   ssh-copy-id usuario@direccion_ip_destino
   ```

## Uso de los Scripts

### Ejecución de `migrate_vm.py`
1. Ejecuta `migrate_vm.py`:
   ```bash
   python migrate_vm.py
   ```
2. Usa el menú para seleccionar la operación deseada:
   - **Opción 1**: Lista todas las VMs.
   - **Opción 2**: Inicia una VM especificando su nombre.
   - **Opción 3**: Apaga una VM especificando su nombre.
   - **Opción 4**: Monitorea el estado y uso de recursos de una VM.
   - **Opción 5**: Ajusta el porcentaje de carga de CPU para una VM.
   - **Opción 6**: Realiza la migración en vivo de una VM.

### Ejecución de `migrate.sh`
Para crear una nueva VM, ejecuta:
```bash
./migrate.sh
```

## Generación de Carga en la VM

Para simular una carga de CPU y activar la migración en vivo, ejecuta:
```bash
stress-ng --cpu 1 --cpu-load 80 --timeout 60s
```