import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from worlddb import MemoryGraph, Node

class TestWorldDB(unittest.TestCase):
    
    def test_immutability_and_merkle_cascade(self):
        """
        Test that modifying a child creates a new hash, and that parent
        can be cascaded to reflect the new child hash.
        """
        graph = MemoryGraph()
        
        # 1. Create a child node
        child1 = graph.insert_node({"name": "Agent Sub-Core", "version": "1.0"})
        # 2. Create a parent node containing the child
        parent1 = graph.insert_node({"name": "Agent Core"}, children=[child1.id])
        
        # 3. 'Update' the child (Creates a new node)
        child2 = graph.update_node(child1.id, {"name": "Agent Sub-Core", "version": "1.1"})
        
        # The IDs must be completely different due to SHA-256 content addressing
        self.assertNotEqual(child1.id, child2.id)
        self.assertEqual(graph.get_node(child2.id).content["version"], "1.1")
        
        # 4. Cascade the update to the parent
        parent2 = graph.cascade_update(parent1.id, child1.id, child2.id)
        
        # Parent ID must change because its children list changed
        self.assertNotEqual(parent1.id, parent2.id)
        self.assertIn(child2.id, parent2.children)
        self.assertNotIn(child1.id, parent2.children)

    def test_supersession_edge_hook(self):
        """
        Test that write-time edge hooks can process logical replacements without deleting old data.
        """
        graph = MemoryGraph()
        
        # Fact 1: User is a Guest
        fact1 = graph.insert_node({"user_role": "Guest"})
        
        # Edge Hook: Programmable logic executed at write-time
        log = []
        def log_supersede(g, edge):
            log.append(f"Fact {edge.target_id[:8]} logically replaced by {edge.source_id[:8]}")
            
        # Fact 2: User is upgraded to Admin
        fact2 = graph.update_node(fact1.id, {"user_role": "Admin"}, on_supersede=log_supersede)
        
        # Verify the programmable hook ran
        self.assertEqual(len(log), 1)
        self.assertTrue("logically replaced by" in log[0])
        
        # Active Fact Resolution
        active_admin = graph.get_active_fact("user_role", "Admin")
        self.assertIsNotNone(active_admin)
        self.assertEqual(active_admin.id, fact2.id)
        
        # The old fact is physically in the DB, but logically superseded
        old_fact = graph.get_node(fact1.id)
        self.assertIsNotNone(old_fact) # Immutability holds
        
        # But it should NOT be returned as an active fact
        inactive_guest = graph.get_active_fact("user_role", "Guest")
        self.assertIsNone(inactive_guest)

if __name__ == '__main__':
    unittest.main()
