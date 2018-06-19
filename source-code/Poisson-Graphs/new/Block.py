from copy import *
from random import *
from time import *
import unittest


class Block(object):
    def __init__(self, inp):
        if "block ID" in inp:
            if inp["block ID"] is None:
                self.block_id = hash(time() + random())
            else:
                self.block_id = deepcopy(inp["block ID"])
        else:
            self.block_id = hash(time() + random())
        self.timestamp = deepcopy(inp["timestamp"])
        self.parents = deepcopy(inp["parents"]) # list of block IDs
        self.difficulty = deepcopy(inp["difficulty"])


class TestBlock(unittest.TestCase):
    def test_block(self):
        # All the creation of a block does is establish some data for that block.
        b = Block({"block ID": None, "timestamp": 1.0, "parents": ["rachel", "ethel"], "difficulty": 1.0})
        c = Block({"block ID": "alice", "timestamp": 2.0, "parents": [b.block_id], "difficulty": 1.0})
        self.assertEqual(c.block_id, "alice")
        self.assertEqual(b.parents, ["rachel", "ethel"])
        self.assertEqual(b.timestamp, 1.0)
        self.assertEqual(c.timestamp, 2.0)
        self.assertEqual(c.parents, [b.block_id])

    def test_rudimentary_blockdag(self):
        real_inter_arrival_time = 100.0
        blocks = {}

        genesis_params = {"block ID": None, "timestamp": 0.0, "parents": None, "difficulty": 1.0}
        g = Block(genesis_params)
        blocks.update({g.block_id: g})

        next_block_params = {"block ID": None, "timestamp": real_inter_arrival_time, "parents": [g.block_id], "difficulty": 1.0}
        b = Block(next_block_params)
        blocks.update({b.block_id: b})

        next_block_params["timestamp"] += real_inter_arrival_time
        next_block_params["parents"][0] = b.block_id
        c = Block(next_block_params)
        blocks.update({c.block_id: c})

        next_block_params["timestamp"] += real_inter_arrival_time
        next_block_params["parents"][0] = c.block_id
        d = Block(next_block_params)
        e = Block(next_block_params)
        blocks.update({d.block_id: d, e.block_id: e})

        next_block_params["timestamp"] += real_inter_arrival_time
        next_block_params["parents"] = [d.block_id, e.block_id]
        f = Block(next_block_params)
        blocks.update({f.block_id: f})

        next_block_params["timestamp"] += real_inter_arrival_time
        next_block_params["parents"] = [f.block_id]
        h = Block(next_block_params)
        blocks.update({h.block_id: h})

        next_block_params["timestamp"] += real_inter_arrival_time
        next_block_params["parents"][0] = h.block_id
        i = Block(next_block_params)
        blocks.update({i.block_id: i})

        this_block = i
        self.assertEqual(len(this_block.parents),1)
        parent_id = this_block.parents[0]
        this_block = blocks[parent_id] # Should be h
        self.assertEqual(len(this_block.parents), 1)
        parent_id = this_block.parents[0]
        this_block = blocks[parent_id] # should be f

        self.assertEqual(len(this_block.parents),2)
        # One should be d and one should be e.
        parent_id_x = this_block.parents[0]
        parent_id_y = this_block.parents[1]
        x = blocks[parent_id_x]
        y = blocks[parent_id_y]

        self.assertEqual(x.parents,y.parents)
        self.assertEqual(len(x.parents),1)
        parent_id = x.parents[0]
        self.assertEqual(parent_id, y.parents[0])
        this_block = blocks[parent_id] # should be c

        self.assertEqual(len(this_block.parents),1)
        this_block = blocks[this_block.parents[0]] # Should be b

        self.assertEqual(len(this_block.parents), 1)
        this_block = blocks[this_block.parents[0]]  # Should be g


        self.assertTrue(this_block.parents is None)


#suite = unittest.TestLoader().loadTestsFromTestCase(TestBlock)
#unittest.TextTestRunner(verbosity=1).run(suite)