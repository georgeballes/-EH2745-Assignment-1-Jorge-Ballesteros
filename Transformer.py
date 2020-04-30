class Transformer:

    def __init__(self, the_id, name, hv_kv, lv_kv, s_kva, r, x, z, terminal):
        self.the_id = the_id
        self.name = name
        self.s_kva = s_kva
        self.hv_kv = hv_kv
        self.lv_kv = lv_kv
        self.r = r
        self.x = x
        self.z = z
        self.terminal = terminal