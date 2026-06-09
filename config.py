CARD_USERS        = 10_000         
CARD_POSTS        = 1_000_000       
LENGTH_USER       = 100             
LENGTH_POST       = 200             
LENGTH_UID        = 4               

# Selectivity: fraction of Posts that match a given User set
SELECTIVITY       = CARD_USERS / CARD_POSTS   # 0.01

# --- Cost coefficients (Özsu & Valduriez standard values) ---
C_CPU  = 0.000001   
C_IO   = 0.0001    
C_MSG  = 0.02       
C_TR   = 0.000001   

# --- Simulated network parameters ---
NETWORK_BANDWIDTH_BPS  = 100_000_000   # 100 Mbps
NETWORK_LATENCY_S      = 0.005         # 5 ms base latency per message
DISK_IO_TIME_S         = 0.00001       # 10 µs per I/O
CPU_INST_TIME_S        = 0.000000001   # 1 ns per CPU instruction
