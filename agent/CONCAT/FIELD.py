# -*- coding: utf-8 -*-

DISK_STATS=['reads','reads_merge','reads_sector','read_time','writes','write_merge','write_sector','write_time','io_curr','io_ms','io_weight']


CPU_STAT_2_6_11 = ['cpu_user','cpu_nice','cpu_system','cpu_idle','cpu_iowait','cpu_irq','cpu_softirq']
CPU_STAT_2_6_24 = ['cpu_user','cpu_nice','cpu_system','cpu_idle','cpu_iowait','cpu_irq','cpu_softirq','cpu_steal','cpu_guest']
CPU_STAT_2_6_33 = ['cpu_user','cpu_nice','cpu_system','cpu_idle','cpu_iowait','cpu_irq','cpu_softirq','cpu_steal','cpu_guest','cpu_guest_nice']
OTHER_PROC = ['ctxt','btime','processes','procs_running','procs_blocked']


NET_STAT=['recv_bytes','recv_packets','recv_error','recv_drop','recv_fifo','recv_frame','recv_compressed','recv_multicast','send_bytes','send_packets','send_error','send_drop','send_fifo','send_frame','send_compressed','send_multicast']

NINETY_FIVE_PERCENT=0.95
