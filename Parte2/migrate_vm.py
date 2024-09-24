import libvirt
import subprocess
import time

def list_vms():
    conn = libvirt.open('qemu:///system')
    if conn is None:
        print('Failed to open connection to qemu:///system')
        return

    print("List of available VMs:")
    vms = conn.listAllDomains()
    for vm in vms:
        print(vm.name())

def start_vm(vm_name):
    conn = libvirt.open('qemu:///system')
    if conn is None:
        print('Failed to open connection to qemu:///system')
        return

    try:
        vm = conn.lookupByName(vm_name)
        vm.create()
        print(f"VM {vm_name} started successfully.")
    except libvirt.libvirtError as e:
        print(f"Failed to start VM {vm_name}: {e}")

def shutdown_vm(vm_name):
    conn = libvirt.open('qemu:///system')
    if conn is None:
        print('Failed to open connection to qemu:///system')
        return

    try:
        vm = conn.lookupByName(vm_name)
        vm.shutdown()
        print(f"Shutting down VM {vm_name}...")
    except libvirt.libvirtError as e:
        print(f"Failed to shutdown VM {vm_name}: {e}")

def monitor_vm_info(vm_name):
    conn = libvirt.open('qemu:///system')
    if conn is None:
        print('Failed to open connection to qemu:///system')
        return

    try:
        vm = conn.lookupByName(vm_name)
        info = vm.info()
        memoria_vm = vm.memoryStats()
        print(f"VM Name: {vm_name}")
        print(f"State: {info[0]}")
        print(f"Max memory: {info[1]} KB")
        print(f"Number of virtual CPUs: {info[3]}")
        print(f"CPU time: {info[2]} ms")
        print(f"RAM Usage: {memoria_vm['rss'] / 1048576:.2f} MB")
    except libvirt.libvirtError as e:
        print(f"Failed to get information for VM {vm_name}: {e}")

def set_cpu_percentage(vm_name, user, ip, percentage):
    cmd = ["ssh", f"{user}@{ip}", "stress-ng", "--cpu", "2", "--cpu-load", str(percentage), "--timeout", "30s"]

    try:
        result = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(15)
        print(f"CPU percentage set to {percentage}% for VM {vm_name}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set CPU percentage for VM {vm_name}: {e}")

def live_migrate_vm(vm_name_source, user, ip):
    try:
        src_conn = libvirt.open('qemu:///system')
        dest_conn = libvirt.open(f'qemu+ssh://{user}@{ip}/system')

        dom = src_conn.lookupByName(vm_name_source)
        new_dom = dom.migrate(dest_conn, libvirt.VIR_MIGRATE_LIVE, None, None, 0)

        print('Migration complete')
    except Exception as e:
        print('Error occurred during migration:', e)
    finally:
        if src_conn is not None:
            src_conn.close()
        if dest_conn is not None:
            dest_conn.close()

def main():
    while True:
        print("\nMenu:")
        print("1. List all VMs")
        print("2. Start a VM")
        print("3. Shut down a VM")
        print("4. Monitor VM information")
        print("5. Set CPU percentage for a VM")
        print("6. Live migrate VM")
        print("7. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            list_vms()
        elif choice == '2':
            vm_name = input("Enter the name of the VM to start: ")
            start_vm(vm_name)
        elif choice == '3':
            vm_name = input("Enter the name of the VM to shut down: ")
            shutdown_vm(vm_name)
        elif choice == '4':
            vm_name = input("Enter the name of the VM to monitor: ")
            monitor_vm_info(vm_name)
        elif choice == '5':
            vm_name = input("Enter the name of the VM: ")
            user = input("Enter the SSH user: ")
            ip = input("Enter the IP Address: ")
            percentage = int(input("Enter the CPU percentage (1-100): "))
            set_cpu_percentage(vm_name, user, ip, percentage)
        elif choice == '6':
            vm_name_source = input("Enter the name of the source VM: ")
            user = input("Enter the SSH user for destination: ")
            ip = input("Enter the IP Address of destination: ")
            live_migrate_vm(vm_name_source, user, ip)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
